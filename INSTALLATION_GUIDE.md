# 📦 دليل التنصيب الكامل - نظام قياس ضغط الدم الذكي

## 🎯 نظرة عامة

هذا الدليل يشرح كيفية تنصيب وتشغيل نظام قياس ضغط الدم الذكي على جهاز جديد من الصفر.

---

## 📋 جدول المحتويات

1. [متطلبات النظام](#متطلبات-النظام)
2. [تثبيت Python والمكتبات](#تثبيت-python-والمكتبات)
3. [إعداد قاعدة البيانات MySQL](#إعداد-قاعدة-البيانات-mysql)
4. [إعداد Backend (Python/FastAPI)](#إعداد-backend-pythonfastapi)
5. [إعداد Flutter App](#إعداد-flutter-app)
6. [تشغيل المشروع](#تشغيل-المشروع)
7. [التحقق من العمل](#التحقق-من-العمل)
8. [استكشاف الأخطاء](#استكشاف-الأخطاء)

---

## 💻 متطلبات النظام

### 1. متطلبات البرمجيات:

- ✅ **Python 3.10 أو أحدث** (3.10, 3.11, 3.12)
- ✅ **Flutter SDK** (الإصدار 3.9.0 أو أحدث)
- ✅ **MySQL Server** (5.7 أو أحدث) أو **MariaDB**
- ✅ **phpMyAdmin** (اختياري - لإدارة قاعدة البيانات)
- ✅ **Git** (لتنزيل المشروع)

### 2. متطلبات الأجهزة:

- **RAM:** 8GB على الأقل (16GB موصى به للتدريب)
- **Storage:** 10GB مساحة فارغة على الأقل
- **CPU:** معالج حديث (Intel i5 أو AMD Ryzen 5 أو أفضل)

### 3. نظام التشغيل:

- ✅ **Windows 10/11**
- ✅ **macOS 10.15 أو أحدث**
- ✅ **Linux (Ubuntu 20.04+ أو توزيعات مشابهة)**

---

## 🐍 تثبيت Python والمكتبات

### الخطوة 1: تثبيت Python

#### على Windows:

1. **تنزيل Python:**
   - اذهب إلى: https://www.python.org/downloads/
   - حمّل أحدث إصدار (3.10 أو أحدث)
   - شغّل المثبت

2. **خلال التثبيت:**
   - ✅ تأكد من تحديد "Add Python to PATH"
   - ✅ اختر "Install Now"

3. **التحقق من التثبيت:**
   ```bash
   python --version
   # يجب أن يظهر: Python 3.10.x أو أحدث
   
   pip --version
   # يجب أن يظهر: pip 23.x.x أو أحدث
   ```

#### على macOS:

```bash
# استخدام Homebrew (موصى به)
brew install python@3.11

# أو تنزيل من python.org
# ثم التحقق:
python3 --version
pip3 --version
```

#### على Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# التحقق:
python3 --version
pip3 --version
```

### الخطوة 2: إنشاء Virtual Environment (موصى به)

**لماذا؟** لعزل مكتبات المشروع عن النظام.

#### على Windows:

```bash
# الانتقال إلى مجلد المشروع
cd measuring-blood

# إنشاء virtual environment
python -m venv venv

# تفعيل virtual environment
venv\Scripts\activate

# يجب أن يظهر (venv) في بداية السطر
```

#### على macOS/Linux:

```bash
# الانتقال إلى مجلد المشروع
cd measuring-blood

# إنشاء virtual environment
python3 -m venv venv

# تفعيل virtual environment
source venv/bin/activate

# يجب أن يظهر (venv) في بداية السطر
```

**ملاحظة:** يجب تفعيل `venv` في كل مرة تفتح فيها Terminal جديد.

---

## 🗄️ إعداد قاعدة البيانات MySQL

### الخطوة 1: تثبيت MySQL

#### على Windows:

1. **تنزيل MySQL:**
   - اذهب إلى: https://dev.mysql.com/downloads/installer/
   - حمّل MySQL Installer
   - شغّل المثبت واختر "Developer Default"

2. **خلال التثبيت:**
   - حدد Port: **3306** (أو 3308 إذا كان 3306 مستخدم)
   - احفظ كلمة مرور root
   - اختر "Start MySQL Server at System Startup"

#### على macOS:

```bash
# استخدام Homebrew
brew install mysql

# بدء MySQL
brew services start mysql

# أو بدون Homebrew:
# حمّل من: https://dev.mysql.com/downloads/mysql/
```

#### على Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install mysql-server

# بدء MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# إعداد أمان MySQL
sudo mysql_secure_installation
```

### الخطوة 2: تثبيت phpMyAdmin (اختياري)

#### على Windows:

1. **تثبيت XAMPP أو WAMP:**
   - XAMPP: https://www.apachefriends.org/
   - WAMP: https://www.wampserver.com/
   - يتضمن MySQL و phpMyAdmin

#### على macOS:

```bash
brew install phpmyadmin
```

#### على Linux:

```bash
sudo apt install phpmyadmin
```

### الخطوة 3: إنشاء قاعدة البيانات

#### الطريقة 1: باستخدام MySQL Command Line

```bash
# تسجيل الدخول إلى MySQL
mysql -u root -p
# أدخل كلمة مرور root

# إنشاء قاعدة البيانات
CREATE DATABASE IF NOT EXISTS blood_pressure_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# إنشاء مستخدم (اختياري - للأمان)
CREATE USER 'bp_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON blood_pressure_db.* TO 'bp_user'@'localhost';
FLUSH PRIVILEGES;

# الخروج
EXIT;
```

#### الطريقة 2: باستخدام phpMyAdmin

1. افتح phpMyAdmin في المتصفح: `http://localhost/phpmyadmin`
2. انقر على "New" لإنشاء قاعدة بيانات جديدة
3. أدخل اسم القاعدة: `blood_pressure_db`
4. اختر Collation: `utf8mb4_unicode_ci`
5. انقر "Create"

### الخطوة 4: استيراد الجداول

#### الطريقة 1: من ملفات SQL

```bash
# في MySQL Command Line
mysql -u root -p blood_pressure_db < database/schema.sql
mysql -u root -p blood_pressure_db < database/training_data_migration.sql
```

#### الطريقة 2: من phpMyAdmin

1. افتح phpMyAdmin
2. اختر قاعدة البيانات `blood_pressure_db`
3. انقر على "Import"
4. اختر ملف `database/schema.sql`
5. انقر "Go"
6. كرر العملية لملف `database/training_data_migration.sql`

#### الطريقة 3: نسخ ولصق SQL

افتح `database/schema.sql` وانسخ المحتوى، ثم الصقه في phpMyAdmin → SQL tab.

**التحقق من الجداول:**

```sql
USE blood_pressure_db;
SHOW TABLES;
-- يجب أن يظهر:
-- users
-- measurements
-- training_data
```

---

## 🔧 إعداد Backend (Python/FastAPI)

### الخطوة 1: الانتقال إلى مجلد Backend

```bash
cd backend
```

### الخطوة 2: تثبيت المكتبات

**تأكد من تفعيل virtual environment أولاً!**

```bash
# تثبيت جميع المكتبات المطلوبة
pip install -r requirements.txt
```

**الوقت المتوقع:** 5-15 دقيقة (حسب سرعة الإنترنت)

**ملاحظة:** تثبيت TensorFlow قد يستغرق وقتاً أطول.

### الخطوة 3: إنشاء ملف .env

أنشئ ملف `.env` في مجلد `backend/`:

```bash
# في Windows
cd backend
type nul > .env

# في macOS/Linux
cd backend
touch .env
```

**محتوى ملف `.env`:**

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=blood_pressure_db
DB_PORT=3306

# Security
SECRET_KEY=your-secret-key-change-in-production-make-it-long-and-random

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**⚠️ مهم:** استبدل:
- `your_mysql_password` بكلمة مرور MySQL الخاصة بك
- `your-secret-key-change-in-production-make-it-long-and-random` بمفتاح سري قوي

**إنشاء SECRET_KEY قوي:**

```python
# في Python
import secrets
print(secrets.token_urlsafe(32))
```

### الخطوة 4: إنشاء المجلدات المطلوبة

```bash
# في مجلد backend
mkdir -p uploads
mkdir -p uploads/training
mkdir -p data/train/images
mkdir -p models
```

**على Windows:**

```cmd
mkdir uploads
mkdir uploads\training
mkdir data\train\images
mkdir models
```

### الخطوة 5: التحقق من الإعداد

```bash
# التحقق من الاتصال بقاعدة البيانات
python -c "from database import engine; print('✅ Database connection OK')"
```

**إذا ظهر خطأ:**
- تحقق من بيانات `.env`
- تأكد من تشغيل MySQL
- تحقق من Port (3306 أو 3308)

### الخطوة 6: تهيئة قاعدة البيانات (اختياري)

```bash
# تهيئة الجداول (إذا لم تستوردها من SQL)
python -c "from database import init_db; init_db(); print('✅ Database initialized')"
```

---

## 📱 إعداد Flutter App

### الخطوة 1: تثبيت Flutter SDK

#### على Windows:

1. **تنزيل Flutter:**
   - اذهب إلى: https://flutter.dev/docs/get-started/install/windows
   - حمّل Flutter SDK
   - استخرج الملف في مكان مناسب (مثلاً: `C:\src\flutter`)

2. **إضافة Flutter إلى PATH:**
   - ابحث عن "Environment Variables" في Windows
   - أضف مسار Flutter إلى PATH:
     ```
     C:\src\flutter\bin
     ```

3. **التحقق:**
   ```bash
   flutter --version
   flutter doctor
   ```

#### على macOS:

```bash
# استخدام Homebrew
brew install --cask flutter

# أو تنزيل يدوياً
cd ~/development
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:`pwd`/flutter/bin"

# التحقق
flutter --version
flutter doctor
```

#### على Linux:

```bash
# تنزيل Flutter
cd ~/development
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:`pwd`/flutter/bin"

# إضافة إلى PATH بشكل دائم
echo 'export PATH="$PATH:$HOME/development/flutter/bin"' >> ~/.bashrc
source ~/.bashrc

# التحقق
flutter --version
flutter doctor
```

### الخطوة 2: تثبيت Android Studio (للتطوير على Android)

1. **تنزيل Android Studio:**
   - https://developer.android.com/studio

2. **خلال التثبيت:**
   - ✅ اختر "Standard" installation
   - ✅ قم بتثبيت Android SDK

3. **إعداد Flutter:**
   ```bash
   flutter doctor
   # اتبع التعليمات لإصلاح أي مشاكل
   ```

### الخطوة 3: تثبيت Xcode (للتطوير على iOS - macOS فقط)

```bash
# من App Store
# ابحث عن "Xcode" وقم بتثبيته

# بعد التثبيت
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
```

### الخطوة 4: تثبيت مكتبات Flutter

```bash
# الانتقال إلى مجلد التطبيق
cd blood_pressure_app

# تثبيت المكتبات
flutter pub get
```

**الوقت المتوقع:** 2-5 دقائق

### الخطوة 5: تحديث عنوان Backend

افتح ملف `lib/services/api_service.dart`:

```dart
// ابحث عن:
static const String baseUrl = 'http://172.20.10.2:8000/api';

// استبدله بعنوان Backend الخاص بك:

// للاختبار على نفس الجهاز:
static const String baseUrl = 'http://localhost:8000/api';

// للاختبار على جهاز آخر (Android Emulator):
static const String baseUrl = 'http://10.0.2.2:8000/api';

// للاختبار على جهاز حقيقي (استبدل IP):
static const String baseUrl = 'http://YOUR_IP_ADDRESS:8000/api';
```

**كيفية معرفة IP Address:**

```bash
# على Windows
ipconfig
# ابحث عن IPv4 Address

# على macOS/Linux
ifconfig
# أو
ip addr show
# ابحث عن inet
```

---

## 🚀 تشغيل المشروع

### الخطوة 1: تشغيل MySQL

#### على Windows:

```bash
# من Services
# ابحث عن "Services" في Windows
# ابحث عن "MySQL80" أو "MySQL"
# تأكد من أنه "Running"

# أو من Command Line
net start MySQL80
```

#### على macOS:

```bash
brew services start mysql
```

#### على Linux:

```bash
sudo systemctl start mysql
# أو
sudo service mysql start
```

**التحقق:**

```bash
mysql -u root -p
# إذا نجح تسجيل الدخول، MySQL يعمل ✅
EXIT;
```

### الخطوة 2: تشغيل Backend

```bash
# تأكد من تفعيل virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# الانتقال إلى مجلد backend
cd backend

# تشغيل السيرفر
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**النتيجة المتوقعة:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**التحقق من Backend:**

افتح المتصفح واذهب إلى:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

### الخطوة 3: تشغيل Flutter App

#### على Android Emulator:

```bash
# 1. افتح Android Studio
# 2. Tools → Device Manager
# 3. أنشئ Virtual Device أو استخدم موجود
# 4. شغّل Emulator

# 5. في Terminal
cd blood_pressure_app
flutter run
```

#### على iOS Simulator (macOS فقط):

```bash
# 1. افتح Simulator
open -a Simulator

# 2. في Terminal
cd blood_pressure_app
flutter run
```

#### على جهاز حقيقي:

```bash
# 1. فعّل Developer Mode على الجهاز
# 2. وصّل الجهاز بالكمبيوتر
# 3. في Terminal
cd blood_pressure_app
flutter devices  # للتحقق من الجهاز
flutter run
```

---

## ✅ التحقق من العمل

### 1. التحقق من Backend:

```bash
# اختبار API
curl http://localhost:8000/docs

# أو افتح المتصفح
# http://localhost:8000/docs
```

### 2. التحقق من قاعدة البيانات:

```bash
mysql -u root -p
USE blood_pressure_db;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM measurements;
SELECT COUNT(*) FROM training_data;
EXIT;
```

### 3. اختبار التطبيق:

1. **افتح التطبيق**
2. **سجّل حساب جديد:**
   - اسم
   - بريد إلكتروني
   - كلمة مرور
3. **سجّل الدخول**
4. **جرب قياس ضغط الدم:**
   - اضغط على "قياس ضغط الدم"
   - التقط صورة
   - انتظر النتائج

### 4. التحقق من Logs:

**Backend Logs:**
- يجب أن تظهر طلبات HTTP في Terminal
- يجب أن تظهر رسائل نجاح/خطأ

**Flutter Logs:**
- يجب أن تظهر في Terminal الذي شغّل `flutter run`
- ابحث عن أي أخطاء

---

## 🔍 استكشاف الأخطاء

### مشكلة: لا يمكن الاتصال بقاعدة البيانات

**الأعراض:**
```
Error: (2003, "Can't connect to MySQL server")
```

**الحلول:**

1. **تحقق من تشغيل MySQL:**
   ```bash
   # Windows
   net start MySQL80
   
   # macOS
   brew services start mysql
   
   # Linux
   sudo systemctl start mysql
   ```

2. **تحقق من Port:**
   - في `.env`: `DB_PORT=3306` (أو 3308)
   - في MySQL: `SHOW VARIABLES LIKE 'port';`

3. **تحقق من بيانات الاتصال:**
   - في `.env`: `DB_USER`, `DB_PASSWORD`, `DB_NAME`

### مشكلة: Backend لا يبدأ

**الأعراض:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**الحلول:**

1. **تأكد من تفعيل virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **أعد تثبيت المكتبات:**
   ```bash
   pip install -r requirements.txt
   ```

### مشكلة: Flutter لا يتصل بـ Backend

**الأعراض:**
```
Failed to connect to /172.20.10.2:8000
```

**الحلول:**

1. **تحقق من عنوان Backend:**
   - في `api_service.dart`: تأكد من IP Address صحيح
   - للـ Emulator: استخدم `10.0.2.2:8000`
   - للجهاز الحقيقي: استخدم IP Address الكمبيوتر

2. **تحقق من Firewall:**
   - على Windows: أضف Python إلى Firewall exceptions
   - على macOS/Linux: تحقق من Firewall settings

3. **تحقق من تشغيل Backend:**
   ```bash
   curl http://localhost:8000/docs
   ```

### مشكلة: TensorFlow لا يعمل

**الأعراض:**
```
ImportError: DLL load failed
```

**الحلول:**

1. **تأكد من Python 64-bit:**
   ```bash
   python -c "import platform; print(platform.architecture())"
   # يجب أن يظهر: ('64bit', ...)
   ```

2. **أعد تثبيت TensorFlow:**
   ```bash
   pip uninstall tensorflow
   pip install tensorflow==2.15.0
   ```

### مشكلة: Flutter pub get فشل

**الأعراض:**
```
Error: Could not find a file named "pubspec.yaml"
```

**الحلول:**

1. **تأكد من المسار:**
   ```bash
   cd blood_pressure_app
   flutter pub get
   ```

2. **امسح Cache:**
   ```bash
   flutter clean
   flutter pub get
   ```

---

## 📝 ملخص الأوامر السريعة

### إعداد Backend:

```bash
# 1. تفعيل virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 2. تثبيت المكتبات
cd backend
pip install -r requirements.txt

# 3. إنشاء .env وتعديله

# 4. تشغيل Backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### إعداد Flutter:

```bash
# 1. تثبيت المكتبات
cd blood_pressure_app
flutter pub get

# 2. تحديث baseUrl في api_service.dart

# 3. تشغيل التطبيق
flutter run
```

### إعداد قاعدة البيانات:

```bash
# 1. تشغيل MySQL
# Windows: net start MySQL80
# macOS: brew services start mysql
# Linux: sudo systemctl start mysql

# 2. إنشاء قاعدة البيانات
mysql -u root -p
CREATE DATABASE blood_pressure_db;
EXIT;

# 3. استيراد الجداول
mysql -u root -p blood_pressure_db < database/schema.sql
mysql -u root -p blood_pressure_db < database/training_data_migration.sql
```

---

## 🎯 الخطوات التالية

بعد التنصيب الناجح:

1. ✅ **جرب التطبيق:** سجّل حساب واختبر قياس ضغط الدم
2. ✅ **جمع البيانات:** اجمع صور وقياسات حقيقية
3. ✅ **تدريب النموذج:** بعد جمع 50+ صورة، درّب النموذج
4. ✅ **راجع التوثيق:**
   - `CNN_TRAINING_DOCUMENTATION.md` - آلية التدريب
   - `TRAINING_COMPLETE_GUIDE.md` - دليل التدريب
   - `README.md` - نظرة عامة

---

## 📞 الدعم

إذا واجهت مشاكل:

1. **راجع قسم "استكشاف الأخطاء"** أعلاه
2. **تحقق من Logs** في Backend و Flutter
3. **راجع التوثيق** في ملفات `.md` الأخرى

---

## ⚖️ حقوق النشر

**© 2025 - جميع الحقوق محفوظة**

**م.عبد المهيمن**

هذا الدليل والمشروع محمي بحقوق النشر. لا يُسمح بنسخ أو توزيع أو تعديل أي جزء من هذا المشروع دون إذن كتابي من المالك.

---

**تم إنشاء هذا الدليل بواسطة:**
- نظام قياس ضغط الدم الذكي
- Flutter + Python/FastAPI + MySQL

**آخر تحديث:** 2025

---

**شكراً لاستخدامك نظام قياس ضغط الدم الذكي! 🩺💙**

