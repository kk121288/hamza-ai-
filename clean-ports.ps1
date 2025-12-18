Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🔧 تنظيف المنافذ 8000 و 8080 بالقوة" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# دالة لقتل العمليات على منفذ معين
function Kill-PortProcess {
    param([int]$Port)
    
    Write-Host "`n🔍 البحث عن عمليات على المنفذ $Port..." -ForegroundColor Yellow
    $output = netstat -ano | findstr ":$Port"
    
    if ($output) {
        Write-Host "✅ تم العثور على عمليات على المنفذ $Port:" -ForegroundColor Green
        $output | ForEach-Object {
            $parts = $_ -split '\s+'
            $pidNum = $parts[-1]
            $localAddress = $parts[2]
            
            if ($pidNum -ne "0") {
                # الحصول على اسم العملية
                $processName = "Unknown"
                try {
                    $process = Get-Process -Id $pidNum -ErrorAction SilentlyContinue
                    if ($process) {
                        $processName = $process.ProcessName
                    }
                } catch {}
                
                Write-Host "   📌 PID: $pidNum | العملية: $processName | العنوان: $localAddress" -ForegroundColor White
                
                # قتل العملية
                try {
                    taskkill /PID $pidNum /F 2>$null
                    Write-Host "   ❌ تم قتل العملية $pidNum ($processName)" -ForegroundColor Red
                } catch {
                    try {
                        Stop-Process -Id $pidNum -Force -ErrorAction SilentlyContinue
                        Write-Host "   ❌ تم إيقاف العملية $pidNum ($processName)" -ForegroundColor Red
                    } catch {
                        Write-Host "   ⚠️  فشل في إيقاف العملية $pidNum" -ForegroundColor Yellow
                    }
                }
            }
        }
    } else {
        Write-Host "✅ المنفذ $Port خالي" -ForegroundColor Green
    }
}

# تحرير المنفذ 8000
Kill-PortProcess -Port 8000

# تحرير المنفذ 8080
Kill-PortProcess -Port 8080

# تحرير منافذ أخرى شائعة
Write-Host "`n🔍 تحرير منافذ إضافية..." -ForegroundColor Yellow
@(8001, 8002, 8003, 8081, 8082, 5000, 5001) | ForEach-Object {
    Kill-PortProcess -Port $_
}

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "✅ اكتمل تنظيف المنافذ!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

# انتظار قليل
Start-Sleep -Seconds 2

Write-Host "`n🌐 يمكنك الآن تشغيل التطبيق:" -ForegroundColor Green
Write-Host "   uvicorn main:app --reload --port 8000" -ForegroundColor White
Write-Host "   أو" -ForegroundColor White
Write-Host "   uvicorn main:app --reload --port 8080" -ForegroundColor White

pause