# run_and_test.ps1
# سكربت متكامل لتشغيل خادم FastAPI واختبار /health و /extract_text تلقائيًا

# ⚙️ إعداد المسار إلى ملف الاختبار
$testFile = "D:\New folder\AI-Plagiarism-Checker\sample.pdf"  # غيّر هذا إلى ملفك التجريبي

# 🚀 1. تشغيل الخادم في نافذة مستقلة
Start-Process powershell -ArgumentList 'cd "D:\New folder\AI-Plagiarism-Checker"; py -m uvicorn main:app --reload --host 127.0.0.1 --port 8000'

# ⏳ 2. الانتظار حتى يبدأ الخادم
Start-Sleep -Seconds 5

# ✅ 3. اختبار /health
Write-Host "`n--- Testing /health endpoint ---" -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get -TimeoutSec 5
    Write-Host "✅ Server is up! Response: $($health | ConvertTo-Json -Depth 2)" -ForegroundColor Green
} catch {
    Write-Host "❌ Server did not respond to /health." -ForegroundColor Red
    exit
}

# 📤 4. إرسال الملف إلى /extract_text
Write-Host "`n--- Testing /extract_text with file: $testFile ---" -ForegroundColor Cyan

try {
    $form = @{ file = Get-Item $testFile }
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/extract_text" -Method Post -Form $form

    Write-Host "`n✅ Text extracted successfully:" -ForegroundColor Green
    $response.text | Out-String | Write-Host
} catch {
    Write-Host "`n❌ Failed to extract text. Error:" -ForegroundColor Red
    $_.Exception.Message
}