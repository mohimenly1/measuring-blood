# Blood Pressure Measurement Backend

Backend API for intelligent blood pressure measurement system using AI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create MySQL database:
```sql
CREATE DATABASE blood_pressure_db;
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Run the server:
```bash
python main.py
# Or using uvicorn:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/measure` - Measure blood pressure from image
- `GET /api/history` - Get measurement history
- `POST /api/recommendations` - Get health recommendations

## Model Training

To train the CNN model, you need to:
1. Prepare your dataset with images and corresponding blood pressure values
2. Update the training function in `models/blood_pressure_model.py`
3. Run training script (to be implemented)

## Notes

- The current CNN model is a placeholder. You need to train it with actual data.
- Update the model path in `blood_pressure_model.py` after training.
- Make sure to change the SECRET_KEY in production.

