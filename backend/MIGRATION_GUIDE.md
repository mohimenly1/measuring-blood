# دليل Migration لقاعدة البيانات

## الإعداد الأولي

### 1. تثبيت Alembic

```bash
cd backend
pip install -r requirements.txt
```

### 2. تهيئة Alembic (للمرة الأولى فقط)

```bash
cd backend
alembic init alembic
```

**ملاحظة:** إذا كان مجلد `alembic` موجود بالفعل، يمكنك تخطي هذه الخطوة.

## استخدام Migration

### إنشاء Migration جديد

عندما تقوم بتعديل النماذج (Models) في `database.py`، قم بإنشاء migration جديد:

```bash
cd backend
alembic revision --autogenerate -m "وصف التغييرات"
```

مثال:
```bash
alembic revision --autogenerate -m "إضافة حقل جديد للمستخدمين"
```

### تطبيق Migrations

لتطبيق جميع التغييرات على قاعدة البيانات:

```bash
cd backend
alembic upgrade head
```

### التراجع عن Migration

للتراجع عن آخر migration:

```bash
cd backend
alembic downgrade -1
```

للتراجع إلى revision محدد:

```bash
cd backend
alembic downgrade <revision_id>
```

### عرض الحالة الحالية

لعرض revision الحالي لقاعدة البيانات:

```bash
cd backend
alembic current
```

### عرض تاريخ Migrations

لعرض جميع migrations:

```bash
cd backend
alembic history
```

## استخدام سكريبت المساعد (migrate.py)

يمكنك استخدام السكريبت المساعد لتسهيل العملية:

```bash
# من مجلد المشروع الرئيسي
python backend/migrate.py init              # تهيئة Alembic
python backend/migrate.py create "وصف"     # إنشاء migration جديد
python backend/migrate.py upgrade          # تطبيق migrations
python backend/migrate.py downgrade        # التراجع عن آخر migration
python backend/migrate.py current          # عرض الحالة الحالية
python backend/migrate.py history          # عرض التاريخ
```

## سيناريوهات شائعة

### 1. إعداد جديد للمشروع

```bash
# 1. أنشئ قاعدة البيانات في MySQL
mysql -u root -p
CREATE DATABASE blood_pressure_db;

# 2. شغّل migration الأولي
cd backend
alembic upgrade head
```

### 2. إضافة حقل جديد إلى جدول موجود

1. عدّل النموذج في `database.py`:
```python
class User(Base):
    # ... الحقول الموجودة
    phone = Column(String(20))  # حقل جديد
```

2. أنشئ migration:
```bash
alembic revision --autogenerate -m "إضافة رقم الهاتف للمستخدمين"
```

3. راجع ملف migration في `alembic/versions/`

4. طبّق التغييرات:
```bash
alembic upgrade head
```

### 3. إعادة إنشاء قاعدة البيانات من الصفر

⚠️ **تحذير:** هذا سيحذف جميع البيانات!

```bash
# 1. احذف قاعدة البيانات
mysql -u root -p
DROP DATABASE blood_pressure_db;
CREATE DATABASE blood_pressure_db;

# 2. طبّق جميع migrations
cd backend
alembic upgrade head
```

## هيكل الملفات

```
backend/
├── alembic/
│   ├── versions/          # ملفات migrations
│   ├── env.py            # إعدادات Alembic
│   └── script.py.mako    # قالب ملفات migration
├── alembic.ini           # ملف التكوين
├── database.py           # النماذج (Models)
└── migrate.py            # سكريبت مساعد
```

## نصائح مهمة

1. **راجع ملفات Migration دائماً:** قبل تطبيق migration، راجع الملف المُنشأ في `alembic/versions/` للتأكد من صحة التغييرات.

2. **استخدم وصف واضح:** استخدم رسائل وصفية عند إنشاء migrations لتسهيل التتبع.

3. **احفظ نسخة احتياطية:** قبل تطبيق migrations على قاعدة بيانات الإنتاج، احفظ نسخة احتياطية.

4. **اختبر على Development أولاً:** اختبر جميع migrations على بيئة التطوير قبل تطبيقها على الإنتاج.

## استكشاف الأخطاء

### خطأ: "Target database is not up to date"

```bash
# حدّث قاعدة البيانات
alembic upgrade head
```

### خطأ: "Can't locate revision identified by"

```bash
# اعرض التاريخ
alembic history

# حدّث إلى revision محدد
alembic upgrade <revision_id>
```

### خطأ في الاتصال بقاعدة البيانات

تأكد من:
- إعدادات `.env` صحيحة
- MySQL يعمل
- قاعدة البيانات موجودة

