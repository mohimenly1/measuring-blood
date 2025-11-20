#!/bin/bash

# سكريبت لتشغيل Backend
# Usage: ./start_backend.sh [IP_ADDRESS]

cd "$(dirname "$0")/backend"

# الحصول على IP تلقائياً إذا لم يتم تحديده
if [ -z "$1" ]; then
    # محاولة الحصول على IP من ifconfig
    IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
    
    if [ -z "$IP" ]; then
        IP="0.0.0.0"
        echo "⚠️  لم يتم العثور على IP - استخدام 0.0.0.0 (يسمح بالاتصال من أي IP)"
    else
        echo "✅ تم العثور على IP: $IP"
    fi
else
    IP="$1"
    echo "✅ استخدام IP المحدد: $IP"
fi

echo ""
echo "🚀 تشغيل Backend على: http://$IP:8000"
echo "📚 Swagger UI: http://$IP:8000/docs"
echo ""
echo "اضغط Ctrl+C لإيقاف السيرفر"
echo ""

# التحقق من وجود ملف .env
if [ ! -f .env ]; then
    echo "⚠️  ملف .env غير موجود"
    echo "📝 أنشئ ملف .env مع بيانات قاعدة البيانات"
fi

# تشغيل uvicorn
uvicorn main:app --reload --host "$IP" --port 8000

