# setup_cloudflared.ps1
# شغّل هذا الملف في PowerShell كمسؤول

# === إعدادات قابلة للتعديل ===
$cloudflaredPath = "D:\cloudflared\cloudflared.exe"
$tunnelName      = "my-tunnel"
$hostname        = "app.user1.us"
$originService   = "http://127.0.0.1:8000"
$certSourcePath  = ""   # مثال: "C:\Users\hamza\Downloads\cert.pem"

function Show-Title($t) { Write-Host "`n=== $t ===`n" -ForegroundColor Cyan }

# تحقق من وجود cloudflared
if (-not (Test-Path $cloudflaredPath)) {
    Write-Host "خطأ: لم أجد cloudflared في المسار المحدد: $cloudflaredPath" -ForegroundColor Red
    exit 1
}

# تأكد من وجود مجلد .cloudflared في مجلد المستخدم
$cloudDir = Join-Path $env:USERPROFILE ".cloudflared"
if (-not (Test-Path $cloudDir)) {
    New-Item -ItemType Directory -Path $cloudDir | Out-Null
    Write-Host "تم إنشاء المجلد: $cloudDir" -ForegroundColor Green
}

# نسخ ملف الشهادة إذا تم تحديد مسار
if ($certSourcePath -and (Test-Path $certSourcePath)) {
    Show-Title "نسخ ملف الشهادة"
    try {
        Copy-Item -Path $certSourcePath -Destination (Join-Path $cloudDir "cert.pem") -Force
        Write-Host "تم نسخ الشهادة إلى: $cloudDir\cert.pem" -ForegroundColor Green
    } catch {
        Write-Host "فشل نسخ الشهادة: $_" -ForegroundColor Red
        exit 1
    }
}

# التحقق من وجود cert.pem أو طلب تسجيل الدخول
$certPath = Join-Path $cloudDir "cert.pem"
if (-not (Test-Path $certPath)) {
    Show-Title "تسجيل الدخول إلى Cloudflare للحصول على الشهادة"
    & $cloudflaredPath login
    Read-Host -Prompt "بعد إتمام التفويض في المتصفح، اضغط Enter للمتابعة"
    if (-not (Test-Path $certPath)) {
        Write-Host "خطأ: لم يتم العثور على cert.pem بعد تسجيل الدخول. يمكنك نسخ cert.pem يدوياً إلى $cloudDir ثم إعادة تشغيل السكربت." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "وجدت cert.pem، المتابعة." -ForegroundColor Green
}

# إنشاء النفق (tunnel create)
Show-Title "إنشاء النفق"
try {
    $tunnelCreateOutput = & $cloudflaredPath tunnel create $tunnelName 2>&1
    Write-Host $tunnelCreateOutput
} catch {
    Write-Host "تحذير: حدث خطأ أثناء تنفيذ أمر إنشاء النفق: $_" -ForegroundColor Yellow
}

# محاولة تحديد ملف الاعتماد (.json) الناتج عن إنشاء النفق
$tunnelJsonPath = ($tunnelCreateOutput -split "`n" | Where-Object { $_ -match "\\.cloudflared\\.*\.json" }) -replace '\s+',''
if (-not $tunnelJsonPath) {
    $jsonFile = Get-ChildItem -Path $cloudDir -Filter "*.json" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($jsonFile) { $tunnelJsonPath = $jsonFile.FullName }
}
if (-not $tunnelJsonPath) {
    Write-Host "خطأ: لم أتمكن من تحديد ملف الاعتماد (.json). تأكد من نجاح أمر 'tunnel create' يدوياً." -ForegroundColor Red
    exit 1
}
$tunnelId = [System.IO.Path]::GetFileNameWithoutExtension($tunnelJsonPath)
Write-Host "تم تحديد Tunnel ID: $tunnelId" -ForegroundColor Green

# ربط اسم النطاق بالنفق (DNS route)
Show-Title "ربط DNS"
try {
    & $cloudflaredPath tunnel route dns $tunnelName $hostname 2>&1 | Write-Host
} catch {
    Write-Host "تحذير: فشل ربط DNS تلقائياً. قد تحتاج إلى صلاحيات DNS في حساب Cloudflare أو تنفيذ الربط يدوياً من لوحة Cloudflare." -ForegroundColor Yellow
}

# إنشاء ملف config.yml باستخدام Here-String لتجنب مشاكل التحليل
Show-Title "إنشاء config.yml"
$configPath = Join-Path $cloudDir "config.yml"
$configContent = @"
tunnel: $tunnelId
credentials-file: $tunnelJsonPath

ingress:
  - hostname: $hostname
    service: $originService
  - service: http_status:404
"@
try {
    Set-Content -Path $configPath -Value $configContent -Encoding UTF8
    Write-Host "تم إنشاء config.yml في: $configPath" -ForegroundColor Green
} catch {
    Write-Host "فشل إنشاء config.yml: $_" -ForegroundColor Red
    exit 1
}

# تثبيت cloudflared كخدمة Windows وتشغيلها
Show-Title "تثبيت cloudflared كخدمة Windows"
try {
    & $cloudflaredPath service install 2>&1 | Write-Host
    Start-Sleep -Seconds 2
    sc.exe start Cloudflared | Write-Host
    Start-Sleep -Seconds 2
    sc.exe query Cloudflared | Write-Host
} catch {
    Write-Host "فشل تثبيت أو تشغيل الخدمة تلقائياً. تأكد من تشغيل PowerShell كمسؤول." -ForegroundColor Red
    exit 1
}

# اختبار الوصول المحلي إلى خدمة الأصل
Show-Title "اختبار الوصول المحلي"
try {
    $tempFile = Join-Path $env:TEMP "cloudflared_test_response.html"
    curl.exe "http://127.0.0.1:8000/" -o $tempFile -s
    if (Test-Path $tempFile) {
        Write-Host "تم حفظ استجابة محلية إلى: $tempFile" -ForegroundColor Green
    } else {
        Write-Host "لم يتم الحصول على استجابة محلية. تأكد من أن التطبيق يستمع على $originService" -ForegroundColor Yellow
    }
} catch {
    Write-Host "فشل اختبار HTTP محلي: $_" -ForegroundColor Yellow
}

Show-Title "انتهاء الإعداد"
Write-Host "راجع ملفات الاعتماد وملف config في: $cloudDir" -ForegroundColor Cyan
Write-Host "لعرض آخر سطور لوق cloudflared: Get-Content `"$cloudDir\cloudflared.log`" -Tail 50" -ForegroundColor Cyan
Write-Host "لإيقاف الخدمة: sc stop Cloudflared" -ForegroundColor Cyan

