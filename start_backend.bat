@echo off
REM سكريبت لتشغيل Backend على Windows
REM Usage: start_backend.bat [IP_ADDRESS]

cd backend

if "%1"=="" (
    echo استخدام 0.0.0.0 (يسمح بالاتصال من أي IP)
    set IP=0.0.0.0
) else (
    set IP=%1
    echo استخدام IP المحدد: %IP%
)

echo.
echo تشغيل Backend على: http://%IP%:8000
echo Swagger UI: http://%IP%:8000/docs
echo.
echo اضغط Ctrl+C لإيقاف السيرفر
echo.

REM التحقق من وجود ملف .env
if not exist .env (
    echo ⚠️  ملف .env غير موجود
    echo 📝 أنشئ ملف .env مع بيانات قاعدة البيانات
)

REM تشغيل uvicorn
uvicorn main:app --reload --host %IP% --port 8000

