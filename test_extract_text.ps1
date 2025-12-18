# إعداد المسار إلى ملف الاختبار
$testFile = "D:\New folder\AI-Plagiarism-Checker\sample.pdf"  # غيّر هذا إلى مسار ملفك

# 1. تشغيل الخادم في نافذة مستقلة
Start-Process powershell -ArgumentList 'cd "D:\New folder\AI-Plagiarism-Checker"; py -m uvicorn main:app --reload --host 127.0.0.1 --port 8000'

# 2. الانتظار حتى يبدأ الخادم
Start-Sleep -Seconds 5

# 3. إرسال الملف إلى /extract_text
Write-Host "`n--- Testing /extract_text with file: $testFile ---" -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/extract_text" `
        -Method Post `
        -InFile $testFile `
        -ContentType "multipart/form-data"
    
    Write-Host "`n✅ Text extracted successfully:" -ForegroundColor Green
    $response.text | Out-String | Write-Host
} catch {
    Write-Host "`n❌ Failed to extract text. Error:" -ForegroundColor Red
    $_.Exception.Message
}

