@echo off
chcp 65001 >nul
echo ========================================
echo    تشغيل AI Detector Pro - FastAPI
echo ========================================
echo.

echo 📦 تثبيت المكتبات المطلوبة...
call pip install -r requirements.txt

echo.
echo 🚀 تشغيل الخادم...
echo 📊 الإصدار: 2.0.0
echo 🌐 الرابط: http://localhost:8000
echo 📚 التوثيق: http://localhost:8000/api-docs
echo.

python main.py

pause