# دليل سريع لـ Migration

## الخطوات السريعة

### 1. تثبيت Alembic

```bash
cd backend
pip install -r requirements.txt
```

### 2. إنشاء Migration الأولي

```bash
cd backend
alembic revision --autogenerate -m "Initial migration"
```

### 3. تطبيق Migration على قاعدة البيانات

```bash
alembic upgrade head
```

## الأوامر الأساسية

```bash
# إنشاء migration جديد
alembic revision --autogenerate -m "وصف التغييرات"

# تطبيق جميع migrations
alembic upgrade head

# التراجع عن آخر migration
alembic downgrade -1

# عرض الحالة الحالية
alembic current

# عرض تاريخ migrations
alembic history
```

## استخدام السكريبت المساعد

```bash
cd backend

# إنشاء migration
python migrate.py create "وصف التغييرات"

# تطبيق migrations
python migrate.py upgrade

# عرض الحالة
python migrate.py current
```

## مثال كامل

```bash
# 1. تأكد من أن قاعدة البيانات موجودة
mysql -u root -p
CREATE DATABASE IF NOT EXISTS blood_pressure_db;

# 2. عدّل النماذج في database.py إذا لزم الأمر

# 3. أنشئ migration
cd backend
alembic revision --autogenerate -m "Create initial tables"

# 4. راجع ملف migration في alembic/versions/

# 5. طبّق migration
alembic upgrade head

# 6. تحقق من النتيجة
alembic current
```

## ملاحظات

- تأكد من تحديث ملف `.env` ببيانات قاعدة البيانات الصحيحة
- راجع ملفات migration قبل تطبيقها
- احفظ نسخة احتياطية قبل migrations على الإنتاج

