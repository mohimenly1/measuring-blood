from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timedelta
import os
import shutil
import logging
from pathlib import Path

# إعداد logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from database import get_db, init_db, User, Measurement, TrainingData
from models.blood_pressure_model import BloodPressureCNN
from models.health_recommendations import HealthRecommendationsAI

# Initialize FastAPI
app = FastAPI(title="Blood Pressure Measurement API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing using bcrypt directly
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Middleware للـ logging
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    if request.headers.get("authorization"):
        auth_header = request.headers.get("authorization")
        logger.info(f"Authorization header present: {auth_header[:30]}...")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Initialize models
bp_model = BloodPressureCNN()
recommendations_ai = HealthRecommendationsAI()

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize database
init_db()


# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class MeasurementResponse(BaseModel):
    id: int
    systolic: float
    diastolic: float
    created_at: datetime
    recommendations: list


# Helper functions
def verify_password(plain_password, hashed_password):
    """Verify a password against a hash"""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False


def get_password_hash(password):
    """Hash a password"""
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    # تحويل sub إلى string إذا كان integer (JWT يتطلب string)
    if "sub" in to_encode and isinstance(to_encode["sub"], int):
        to_encode["sub"] = str(to_encode["sub"])
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    import logging
    logger = logging.getLogger(__name__)
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="غير مصرح لك - يرجى تسجيل الدخول",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Logging للـ token المستلم
    logger.info(f"Received token (first 20 chars): {token[:20] if token else 'None'}...")
    logger.info(f"Token length: {len(token) if token else 0}")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # sub هو string في JWT، نحتاج لتحويله إلى int
        sub_value = payload.get("sub")
        logger.info(f"Decoded token successfully. Sub value: {sub_value} (type: {type(sub_value).__name__})")
        
        if sub_value is None:
            logger.error("Sub is None in token payload")
            raise credentials_exception
        
        # تحويل sub من string إلى int
        try:
            user_id: int = int(sub_value)
        except (ValueError, TypeError):
            logger.error(f"Cannot convert sub to int: {sub_value}")
            raise credentials_exception
    except JWTError as e:
        # تحسين رسالة الخطأ مع logging
        logger.error(f"JWT Error: {str(e)}")
        logger.error(f"Token that failed: {token[:50] if token else 'None'}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"الـ token غير صحيح أو منتهي الصلاحية: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.error(f"User with ID {user_id} not found in database")
        raise credentials_exception
    
    logger.info(f"User authenticated successfully: {user.email}")
    return user


# Routes
@app.post("/api/auth/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مستخدم بالفعل")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(db_user),
    }


@app.post("/api/auth/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
    }


@app.post("/api/measure")
async def measure_blood_pressure(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Measure request received from user: {current_user.email} (ID: {current_user.id})")
    # Save uploaded image
    file_path = UPLOAD_DIR / f"{current_user.id}_{datetime.now().timestamp()}.jpg"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    try:
        # Predict blood pressure using CNN
        result = bp_model.predict(str(file_path))
        
        # Get health recommendations
        recommendations_data = recommendations_ai.get_recommendations(
            result['systolic'], result['diastolic']
        )
        
        # Save measurement to database
        measurement = Measurement(
            user_id=current_user.id,
            systolic=result['systolic'],
            diastolic=result['diastolic'],
            image_path=str(file_path),
        )
        db.add(measurement)
        db.commit()
        db.refresh(measurement)
        
        return {
            "id": measurement.id,
            "systolic": result['systolic'],
            "diastolic": result['diastolic'],
            "created_at": measurement.created_at.isoformat(),
            "recommendations": recommendations_data['recommendations'],
            "category": recommendations_data['category'],
            "severity": recommendations_data['severity'],
        }
    except Exception as e:
        # Clean up file on error
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"خطأ في معالجة الصورة: {str(e)}")


@app.get("/api/history")
async def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    measurements = (
        db.query(Measurement)
        .filter(Measurement.user_id == current_user.id)
        .order_by(Measurement.created_at.desc())
        .limit(50)
        .all()
    )
    
    history = []
    for m in measurements:
        recommendations_data = recommendations_ai.get_recommendations(
            m.systolic, m.diastolic
        )
        history.append({
            "id": m.id,
            "systolic": m.systolic,
            "diastolic": m.diastolic,
            "created_at": m.created_at.isoformat(),
            "recommendations": recommendations_data['recommendations'],
        })
    
    return {"history": history}


@app.post("/api/recommendations")
async def get_recommendations(
    systolic: float,
    diastolic: float,
    current_user: User = Depends(get_current_user),
):
    recommendations_data = recommendations_ai.get_recommendations(systolic, diastolic)
    return recommendations_data


@app.post("/api/training-data")
async def save_training_data(
    image: UploadFile = File(...),
    systolic: str = Form(...),
    diastolic: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    حفظ بيانات التدريب (صورة + قياسات حقيقية)
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        systolic_float = float(systolic)
        diastolic_float = float(diastolic)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="القياسات يجب أن تكون أرقام صحيحة"
        )
    
    # حفظ الصورة
    file_path = UPLOAD_DIR / f"training_{current_user.id}_{datetime.now().timestamp()}.jpg"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    try:
        # حفظ في قاعدة البيانات
        training_data = TrainingData(
            user_id=current_user.id,
            image_path=str(file_path),
            systolic=systolic_float,
            diastolic=diastolic_float,
            is_verified=1,  # تم التحقق من المستخدم
        )
        db.add(training_data)
        db.commit()
        db.refresh(training_data)
        
        logger.info(f"تم حفظ بيانات تدريب: user_id={current_user.id}, bp={systolic_float}/{diastolic_float}")
        
        return {
            "id": training_data.id,
            "message": "تم حفظ بيانات التدريب بنجاح",
            "total_training_data": db.query(TrainingData).filter(
                TrainingData.is_verified == 1
            ).count()
        }
    except Exception as e:
        # حذف الصورة في حالة الخطأ
        if file_path.exists():
            file_path.unlink()
        logger.error(f"خطأ في حفظ بيانات التدريب: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"خطأ في حفظ البيانات: {str(e)}"
        )


@app.get("/api/training-data/export")
async def export_training_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    تصدير بيانات التدريب بصيغة CSV للتدريب
    """
    training_data = db.query(TrainingData).filter(
        TrainingData.is_verified == 1
    ).all()
    
    if not training_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="لا توجد بيانات تدريب"
        )
    
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['image_name', 'systolic', 'diastolic'])
    
    for data in training_data:
        image_name = os.path.basename(data.image_path)
        writer.writerow([image_name, data.systolic, data.diastolic])
    
    return {
        "csv": output.getvalue(),
        "count": len(training_data),
        "message": "استخدم هذا CSV مع سكريبت التدريب"
    }


@app.get("/api/training-data/stats")
async def get_training_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """إحصائيات بيانات التدريب"""
    total = db.query(TrainingData).filter(
        TrainingData.is_verified == 1
    ).count()
    
    return {
        "total_training_data": total,
        "minimum_required": 50,
        "status": "ready" if total >= 50 else "collecting",
        "message": "جاهز للتدريب" if total >= 50 else f"تحتاج {50 - total} صورة أخرى"
    }


@app.get("/")
async def root():
    return {"message": "Blood Pressure Measurement API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

