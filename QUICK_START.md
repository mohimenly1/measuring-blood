# 🚀 دليل البدء السريع

## الأوامر الأساسية

### 1. تشغيل Backend

**الطريقة الأسهل (موصى به):**

```bash
# من مجلد المشروع الرئيسي
./start_backend.sh
```

أو مع IP محدد:

```bash
./start_backend.sh 172.20.10.2
```

**الطريقة اليدوية:**

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**ملاحظة:** 
- `0.0.0.0` يسمح بالاتصال من أي IP (للاختبار على الهاتف)
- `172.20.10.2` IP محدد (استخدم IP الكمبيوتر الخاص بك)

### 2. تشغيل Flutter App

```bash
cd blood_pressure_app
flutter pub get
flutter run
```

## 📋 التحقق قبل التشغيل

### ✅ 1. قاعدة البيانات

```bash
# في MySQL
mysql -u root -p
USE blood_pressure_db;
SHOW TABLES;
# يجب أن ترى: users, measurements, training_data, alembic_version
```

### ✅ 2. ملف .env

```bash
cd backend
cat .env
# يجب أن يحتوي على:
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=blood_pressure_db
# DB_PORT=3308
# SECRET_KEY=your-secret-key
```

### ✅ 3. المكتبات

```bash
cd backend
pip install -r requirements.txt
```

### ✅ 4. عنوان API في Flutter

افتح `blood_pressure_app/lib/services/api_service.dart`:

```dart
static const String baseUrl = 'http://YOUR_IP:8000/api';
```

**للاختبار على الهاتف:**
- استخدم IP الكمبيوتر (ليس localhost)
- مثال: `http://172.20.10.2:8000/api`

## 🎯 الأوامر الكاملة (نسخ ولصق)

### Terminal 1 - Backend:

```bash
cd /Users/sulimangzllal/Development/measuring-blood/backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Flutter:

```bash
cd /Users/sulimangzllal/Development/measuring-blood/blood_pressure_app
flutter pub get
flutter run
```

## 🔍 التحقق من أن كل شيء يعمل

### 1. Backend:

افتح المتصفح:
- ✅ `http://localhost:8000/` → يجب أن ترى: `{"message": "Blood Pressure Measurement API", "version": "1.0.0"}`
- ✅ `http://localhost:8000/docs` → Swagger UI

### 2. Flutter:

- ✅ التطبيق يفتح
- ✅ يمكن تسجيل حساب جديد
- ✅ يمكن التقاط صورة

## ⚠️ استكشاف الأخطاء

### خطأ: "Address already in use"

```bash
# استخدم منفذ آخر
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### خطأ: "Can't connect to database"

1. تحقق من تشغيل MySQL
2. تحقق من ملف `.env`
3. تحقق من المنفذ (3308)

### خطأ: "Connection refused" في Flutter

1. تأكد من IP الصحيح في `api_service.dart`
2. تأكد من أن Backend يعمل
3. تأكد من أن الهاتف والكمبيوتر على نفس الشبكة

## 📱 للاختبار على الهاتف

### 1. العثور على IP:

**macOS:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Windows:**
```bash
ipconfig
```

### 2. تحديث Flutter:

```dart
// في api_service.dart
static const String baseUrl = 'http://YOUR_IP:8000/api';
```

### 3. تشغيل Backend:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ✅ الخلاصة

**الأمر الأساسي لتشغيل Backend:**

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**أو:**

```bash
./start_backend.sh
```

**الأمر الأساسي لتشغيل Flutter:**

```bash
cd blood_pressure_app
flutter run
```

---

**ملاحظة:** استخدم `0.0.0.0` بدلاً من IP محدد لتسهيل الاتصال من أي جهاز على نفس الشبكة.

