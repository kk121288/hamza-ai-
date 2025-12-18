# run_server.ps1
Set-Location -Path "D:\New folder\AI-Plagiarism-Checker"
py -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
# تشغيل خادم FastAPI واختبار /health تلقائيًا

# 1. الانتقال إلى مجلد المشروع
Set-Location -Path "D:\New folder\AI-Plagiarism-Checker"

# 2. تشغيل الخادم في نافذة مستقلة
Start-Process powershell -ArgumentList 'py -m uvicorn main:app --reload --host 127.0.0.1 --port 8000'

# 3. الانتظار 5 ثوانٍ حتى يبدأ الخادم
Start-Sleep -Seconds 5

# 4. اختبار مسار /health
Write-Host "`n--- Testing /health endpoint ---" -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get -TimeoutSec 5
    Write-Host "✅ Server is up! Response: $($response | ConvertTo-Json -Depth 2)" -ForegroundColor Green
} catch {
    Write-Host "❌ Server did not respond. Check if it started correctly." -ForegroundColor Red
}

