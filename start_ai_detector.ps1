# start_ai_detector.ps1
# سكربت لتعديل اسم التطبيق في main.dart + تشغيل FastAPI + Cloudflare Tunnel

# إعداد المتغيرات
$projectDir = "D:\New folder\AI-Plagiarism-Checker"
$tunnelName = "hamza_checker"
$hostname = "app.user1.us"
$uvicornPort = 8000
$mainFile = Join-Path $projectDir "lib\main.dart"

# ===== تعديل ملف main.dart =====
Write-Host "📝 تعديل اسم التطبيق في main.dart ..." -ForegroundColor Cyan

$dartContent = @"
import 'package:flutter/material.dart';

void main() {
  runApp(const AIPlagiarismApp());
}

class AIPlagiarismApp extends StatelessWidget {
  const AIPlagiarismApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Plagiarism Detector',
      theme: ThemeData(
        primarySwatch: Colors.indigo,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Plagiarism Detector'),
        centerTitle: true,
      ),
      body: const Center(
        child: LogoSection(),
      ),
    );
  }
}

class LogoSection extends StatelessWidget {
  const LogoSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Image.asset(
          'assets/images/logo.png',
          width: 160,
          height: 160,
        ),
        const SizedBox(height: 20),
        const Text(
          'AI Plagiarism Detector',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.indigo,
          ),
        ),
      ],
    );
  }
}
"@

$dartContent | Out-File -FilePath $mainFile -Encoding UTF8 -Force
Write-Host "✅ تم تعديل main.dart بنجاح" -ForegroundColor Green

# ===== تشغيل FastAPI =====
Write-Host "🚀 تشغيل خادم FastAPI على http://localhost:$uvicornPort ..." -ForegroundColor Cyan
Start-Process -FilePath uvicorn -ArgumentList "main:app --reload --host 0.0.0.0 --port $uvicornPort" -WorkingDirectory $projectDir -NoNewWindow

Start-Sleep -Seconds 3

# ===== تشغيل Cloudflare Tunnel =====
Write-Host "🌐 تشغيل نفق Cloudflare باسم $tunnelName ..." -ForegroundColor Cyan
Start-Process -FilePath cloudflared -ArgumentList "tunnel run $tunnelName" -WorkingDirectory $projectDir -NoNewWindow

Start-Sleep -Seconds 2

# ===== فتح الرابط الخارجي =====
Write-Host "✅ التطبيق يعمل الآن على:" -ForegroundColor Green
Write-Host "   🔗 http://localhost:$uvicornPort" -ForegroundColor Yellow
Write-Host "   🌍 https://$hostname" -ForegroundColor Yellow
Start-Process "https://$hostname"

