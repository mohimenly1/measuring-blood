# دليل الإعداد والتشغيل

## المتطلبات الأساسية

1. **Flutter SDK** - أحدث إصدار
2. **Python 3.8+**
3. **MySQL Server** مع phpMyAdmin
4. **pip** (مدير حزم Python)

## خطوات الإعداد

### 1. إعداد قاعدة البيانات

1. افتح phpMyAdmin
2. أنشئ قاعدة بيانات جديدة باسم `blood_pressure_db`
3. استورد ملف `database/schema.sql` أو قم بتشغيله مباشرة

أو استخدم MySQL CLI:
```bash
mysql -u root -p < database/schema.sql
```

### 2. إعداد Backend

```bash
cd backend

# إنشاء بيئة افتراضية (اختياري لكن موصى به)
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate

# تثبيت الحزم
pip install -r requirements.txt

# إعداد ملف البيئة
# قم بنسخ .env.example إلى .env وتعديل القيم
cp .env.example .env

# عدّل ملف .env مع بيانات قاعدة البيانات الخاصة بك:
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=blood_pressure_db
# DB_PORT=3306
# SECRET_KEY=your-random-secret-key-here
```

### 3. تشغيل Backend

```bash
cd backend
python main.py
```

أو باستخدام uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

الخادم سيعمل على: `http://localhost:8000`

### 4. إعداد تطبيق Flutter

```bash
cd blood_pressure_app

# تثبيت الحزم
flutter pub get

# تحديث عنوان API
# افتح lib/services/api_service.dart
# غيّر baseUrl إلى عنوان السيرفر الخاص بك
# مثال: static const String baseUrl = 'http://192.168.1.100:8000/api';
# (استخدم IP جهازك بدلاً من localhost للاختبار على الهاتف)
```

### 5. تشغيل تطبيق Flutter

```bash
# على Android/iOS
flutter run

# أو حدد الجهاز
flutter devices
flutter run -d <device_id>
```

## ملاحظات مهمة

### للاختبار على الهاتف الحقيقي:

1. تأكد أن الهاتف والكمبيوتر على نفس الشبكة
2. استخدم IP الكمبيوتر بدلاً من `localhost` في Flutter app
3. تأكد أن Firewall يسمح بالاتصال على المنفذ 8000

### للعثور على IP الكمبيوتر:

**macOS/Linux:**
```bash
ifconfig | grep "inet "
```

**Windows:**
```bash
ipconfig
```

ابحث عن IPv4 Address في قسم Wi-Fi أو Ethernet

### تحديث baseUrl في Flutter:

افتح `blood_pressure_app/lib/services/api_service.dart` وغيّر:
```dart
static const String baseUrl = 'http://YOUR_IP_ADDRESS:8000/api';
```

## اختبار النظام

1. شغّل Backend على المنفذ 8000
2. شغّل تطبيق Flutter
3. سجّل حساب جديد
4. التقط صورة باستخدام الكاميرا
5. تحقق من النتائج والتوصيات

## استكشاف الأخطاء

### مشكلة الاتصال بقاعدة البيانات:
- تأكد من تشغيل MySQL
- تحقق من بيانات الاتصال في ملف `.env`
- تأكد من إنشاء قاعدة البيانات والجداول

### مشكلة في Flutter:
- تأكد من تثبيت جميع الحزم: `flutter pub get`
- تحقق من عنوان API في `api_service.dart`
- تأكد من صلاحيات الكاميرا في `Info.plist` (iOS) و `AndroidManifest.xml` (Android)

### مشكلة في Backend:
- تحقق من تثبيت جميع الحزم: `pip install -r requirements.txt`
- تأكد من وجود ملف `.env` مع البيانات الصحيحة
- تحقق من السجلات (logs) للأخطاء

## تدريب النموذج (اختياري)

النموذج الحالي هو placeholder. لتدريبه على بيانات حقيقية:

1. جهّز مجموعة بيانات من الصور وقياسات ضغط الدم المقابلة
2. عدّل `backend/train_model.py` لتحميل بياناتك
3. شغّل التدريب:
```bash
cd backend
python train_model.py
```

## الإنتاج

قبل النشر في الإنتاج:

1. غيّر `SECRET_KEY` في `.env` إلى قيمة عشوائية قوية
2. حدّث `CORS origins` في `backend/main.py` لعناوينك فقط
3. استخدم قاعدة بيانات آمنة مع كلمات مرور قوية
4. فعّل HTTPS
5. استخدم خادم إنتاج مثل Gunicorn مع Nginx

