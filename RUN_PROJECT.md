# دليل تشغيل المشروع

## 🚀 الأوامر الصحيحة لتشغيل المشروع

### الخطوة 1: إعداد قاعدة البيانات

#### أ) إنشاء قاعدة البيانات والجداول:

```bash
# في MySQL أو phpMyAdmin
mysql -u root -p

# أو استورد الملف مباشرة
mysql -u root -p < database/schema.sql
mysql -u root -p < database/training_data_migration.sql
```

#### ب) أو استخدم Migration:

```bash
cd backend
alembic upgrade head
```

### الخطوة 2: إعداد Backend

#### أ) تثبيت المكتبات:

```bash
cd backend
pip install -r requirements.txt
```

#### ب) إعداد ملف .env:

```bash
cd backend
# أنشئ ملف .env إذا لم يكن موجوداً
cat > .env << EOF
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=blood_pressure_db
DB_PORT=3308
SECRET_KEY=your-secret-key-change-in-production
EOF
```

#### ج) تشغيل Backend:

**الطريقة 1: استخدام uvicorn مباشرة (موصى به)**

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**الطريقة 2: استخدام Python مباشرة**

```bash
cd backend
python main.py
```

**الطريقة 3: مع IP محدد (للاختبار على الهاتف)**

```bash
cd backend
uvicorn main:app --reload --host 172.20.10.2 --port 8000
```

### الخطوة 3: تحديث عنوان API في Flutter

افتح `blood_pressure_app/lib/services/api_service.dart` وغيّر:

```dart
static const String baseUrl = 'http://172.20.10.2:8000/api';
```

**ملاحظة:** استخدم IP الكمبيوتر الخاص بك (ليس localhost)

### الخطوة 4: تشغيل تطبيق Flutter

```bash
cd blood_pressure_app
flutter pub get
flutter run
```

## 📋 الأوامر الكاملة خطوة بخطوة

### 1. إعداد قاعدة البيانات:

```bash
# في Terminal جديد
mysql -u root -p
# ثم في MySQL:
CREATE DATABASE IF NOT EXISTS blood_pressure_db;
USE blood_pressure_db;
SOURCE /Users/sulimangzllal/Development/measuring-blood/database/schema.sql;
SOURCE /Users/sulimangzllal/Development/measuring-blood/database/training_data_migration.sql;
```

### 2. إعداد Backend:

```bash
cd /Users/sulimangzllal/Development/measuring-blood/backend

# تثبيت المكتبات
pip install -r requirements.txt

# التحقق من ملف .env
cat .env  # تأكد من وجوده وصحة البيانات

# تشغيل Backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. تحديث Flutter:

```bash
cd /Users/sulimangzllal/Development/measuring-blood/blood_pressure_app

# تحديث baseUrl في api_service.dart
# غيّر: static const String baseUrl = 'http://YOUR_IP:8000/api';

# تثبيت الحزم
flutter pub get

# تشغيل التطبيق
flutter run
```

## 🔍 التحقق من أن كل شيء يعمل

### 1. التحقق من Backend:

افتح المتصفح:
- `http://localhost:8000/` - يجب أن ترى رسالة ترحيب
- `http://localhost:8000/docs` - Swagger UI

### 2. التحقق من قاعدة البيانات:

```bash
mysql -u root -p
USE blood_pressure_db;
SHOW TABLES;  # يجب أن ترى: users, measurements, training_data
```

### 3. التحقق من Flutter:

- التطبيق يجب أن يفتح
- يمكنك تسجيل حساب جديد
- يمكنك التقاط صورة

## 🛠️ استكشاف الأخطاء

### خطأ: "Module not found"

```bash
cd backend
pip install -r requirements.txt
```

### خطأ: "Can't connect to database"

- تحقق من ملف `.env`
- تأكد من تشغيل MySQL
- تحقق من المنفذ (3308)

### خطأ: "Connection refused" في Flutter

- تأكد من IP الكمبيوتر
- تأكد من أن Backend يعمل
- تحقق من Firewall

### خطأ: "Address already in use"

```bash
# غيّر المنفذ
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

## 📱 للاختبار على الهاتف الحقيقي

### 1. العثور على IP الكمبيوتر:

**macOS/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Windows:**
```bash
ipconfig
```

ابحث عن IPv4 Address في Wi-Fi أو Ethernet

### 2. تحديث Flutter:

```dart
// في api_service.dart
static const String baseUrl = 'http://YOUR_IP:8000/api';
```

### 3. تشغيل Backend:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**ملاحظة:** `0.0.0.0` يسمح بالاتصال من أي IP

## 🎯 الأوامر السريعة

### تشغيل كل شيء:

**Terminal 1 (Backend):**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Flutter):**
```bash
cd blood_pressure_app
flutter run
```

## ✅ التحقق النهائي

1. ✅ Backend يعمل على `http://localhost:8000`
2. ✅ قاعدة البيانات متصلة
3. ✅ Flutter app متصل بـ Backend
4. ✅ يمكن تسجيل حساب جديد
5. ✅ يمكن التقاط صورة وقياس الضغط

---

**ملاحظة:** إذا كنت تستخدم IP محدد (172.20.10.2)، تأكد من:
- تحديث `baseUrl` في Flutter
- استخدام `--host 0.0.0.0` أو `--host 172.20.10.2`
- التأكد من أن الهاتف والكمبيوتر على نفس الشبكة

