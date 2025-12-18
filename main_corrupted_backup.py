cd "D:\New folder\AI-Plagiarism-Checker"

# Create a fresh main.py with correct encoding
@'
from fastapi import FastAPI, HTTPException, File, UploadFile, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
import io
import os
import json
import uuid
from datetime import datetime

# Optional libraries for PDF and DOCX text extraction
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None

try:
    import langdetect
except ImportError:
    langdetect = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Detector Pro API",
    description="نظام متقدم للكشف عن النصوص المولدة بالذكاء الاصطناعي",
    version="2.0.0",
    docs_url="/api-docs",
    redoc_url="/redoc"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# إعداد المجلدات
os.makedirs("static", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# تقديم الملفات الثابتة
app.mount("/static", StaticFiles(directory="static"), name="static")

# تحميل القوالب
templates = Jinja2Templates(directory="templates")

# ========== دوال مساعدة محسنة ==========

def detect_language_advanced(text: str) -> str:
    """كشف اللغة بطرق متعددة"""
    if not text or len(text.strip()) < 10:
        return "unknown"
    
    try:
        # الطريقة 1: استخدام langdetect
        if langdetect:
            result = langdetect.detect(text)
            if result and len(result) > 0:
                lang_code = result[0].lang
                lang_map = {
                    "ar": "العربية", "en": "الإنجليزية", "fr": "الفرنسية",
                    "es": "الإسبانية", "de": "الألمانية", "it": "الإيطالية",
                    "ru": "الروسية", "zh": "الصينية", "ja": "اليابانية"
                }
                return lang_map.get(lang_code, lang_code)
    except:
        pass
    
    # الطريقة 2: كشف بسيط من الأحرف
    arabic_chars = sum(1 for char in text if "\u0600" <= char <= "\u06FF")
    english_chars = sum(1 for char in text if "a" <= char.lower() <= "z")
    
    if arabic_chars > english_chars * 2:
        return "العربية"
    elif english_chars > arabic_chars * 2:
        return "الإنجليزية"
    
    return "مختلطة"

def advanced_ai_detection(text: str) -> Dict:
    """خوارزمية متقدمة لكشف الذكاء الاصطناعي"""
    if not text or len(text.strip()) < 20:
        return {
            "ai_probability": 0.5,
            "note": "النص قصير جدًا لتحليل دقيق",
            "confidence": 50,
            "language": detect_language_advanced(text)
        }
    
    words = text.split()
    if len(words) < 10:
        return {
            "ai_probability": 0.5,
            "note": "نقص في البيانات للتحليل",
            "confidence": 50,
            "language": detect_language_advanced(text)
        }
    
    # مؤشرات متقدمة لكل لغة
    patterns = {
        "العربية": {
            "ai": [
                "بالتأكيد", "كمساعد ذكي", "من خلال قدراتي", "بصفتي نموذج لغة",
                "بناءً على معلوماتي", "كأداة ذكاء اصطناعي", "وفقًا لمعرفتي",
                "نموذج التدريب", "كخوارزمية", "في إطار قدراتي", "يمكنني",
                "أستطيع", "بإمكاني", "ينبغي", "يجب", "من الضروري"
            ],
            "human": [
                "أعتقد", "أظن", "أشعر", "في رأيي", "برأيي", "من وجهة نظري",
                "حسب تجربتي", "بناء على خبرتي", "أنا شخصياً", "شخصياً", "بنفسي",
                "أتذكر", "أذكر أن", "أستحضر", "على ما أعتقد", "على ما أظن"
            ]
        },
        "الإنجليزية": {
            "ai": [
                "as an AI", "based on the data", "I can", "it is necessary",
                "according to my knowledge", "as a language model",
                "based on my training", "I am designed to", "the algorithm",
                "artificial intelligence"
            ],
            "human": [
                "I think", "in my opinion", "from my experience",
                "personally", "I remember", "I feel", "I believe",
                "according to my understanding", "in my view"
            ]
        }
    }
    
    language = detect_language_advanced(text)
    lang_patterns = patterns.get(language, patterns["العربية"])
    
    # حساب المؤشرات
    ai_count = sum(1 for pattern in lang_patterns["ai"] if pattern.lower() in text.lower())
    human_count = sum(1 for pattern in lang_patterns["human"] if pattern.lower() in text.lower())
    
    # تحليل إضافي
    sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").replace("؟", ".").split(".") if s.strip()]
    avg_sentence_len = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    
    unique_words = set(word.lower() for word in words if len(word) > 2)
    vocab_diversity = len(unique_words) / len(words) if words else 0
    
    # حساب الاحتمالية
    base_score = 0.5
    
    if ai_count + human_count > 0:
        base_score = (ai_count + 1) / (ai_count + human_count + 2)
    
    if avg_sentence_len > 25:
        base_score = min(base_score + 0.15, 0.9)
    elif avg_sentence_len < 10:
        base_score = max(base_score - 0.1, 0.1)
    
    if vocab_diversity < 0.4:
        base_score += 0.1
    elif vocab_diversity > 0.7:
        base_score -= 0.1
    
    # التأكد من النطاق
    ai_probability = max(0.05, min(0.95, base_score))
    
    # حساب الثقة
    confidence = 50
    if len(words) > 100:
        confidence += 20
    if abs(ai_probability - 0.5) > 0.3:
        confidence += 15
    confidence = min(95, confidence)
    
    # تحديد النتيجة
    if ai_probability > 0.7:
        note = "نص ذو احتمالية عالية للذكاء الاصطناعي"
    elif ai_probability > 0.55:
        note = "نص مشتبه به (مائل نحو الذكاء الاصطناعي)"
    elif ai_probability < 0.3:
        note = "نص بشري واضح"
    elif ai_probability < 0.45:
        note = "نص مشتبه به (مائل نحو البشر)"
    else:
        note = "النتيجة غير حاسمة"
    
    return {
        "ai_probability": round(ai_probability, 3),
        "human_probability": round(1 - ai_probability, 3),
        "note": note,
        "confidence": confidence,
        "language": language,
        "analysis": {
            "ai_indicators": ai_count,
            "human_indicators": human_count,
            "avg_sentence_length": round(avg_sentence_len, 1),
            "vocab_diversity": round(vocab_diversity, 3),
            "word_count": len(words),
            "character_count": len(text)
        }
    }

# ========== نماذج البيانات ==========

class Texts(BaseModel):
    doc: str
    references: List[str]

class TextAnalysis(BaseModel):
    text: str
    language: Optional[str] = None
    min_confidence: Optional[float] = 0.5

class FileBatchAnalysis(BaseModel):
    file_ids: List[str]
    analysis_type: str = "ai_detection"

# ========== نقاط الوصول الرئيسية ==========

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """الصفحة الرئيسية"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "AI Detector Pro", "version": "2.0.0"}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """لوحة التحكم"""
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "title": "لوحة التحكم"}
    )

@app.get("/api/health")
async def health_check():
    """فحص حالة الخادم"""
    return {
        "status": "healthy",
        "service": "AI Detector Pro",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "ai_detection": True,
            "plagiarism_check": True,
            "file_processing": True,
            "multi_language": True
        }
    }

@app.post("/api/detect_ai")
async def detect_ai(payload: Dict):
    """كشف الذكاء الاصطناعي - النسخة المحسنة"""
    try:
        text = payload.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="النص مطلوب")
        
        # استخدام الخوارزمية المحلية
        result = advanced_ai_detection(text)
        result["method"] = "advanced_algorithm"
        return result
            
    except Exception as e:
        logger.exception("Error in /api/detect_ai")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/check_plagiarism")
async def check_plagiarism(payload: Texts):
    """فحص الانتحال"""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        docs = [payload.doc] + payload.references

        if all(not d or len(d.strip().split()) < 2 for d in docs):
            return {
                "scores": [{"ref_index": i, "score": 0.0} for i in range(len(payload.references))],
                "warning": "النصوص قصيرة جدًا"
            }

        vect = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b").fit_transform(docs)

        if vect.shape[1] == 0:
            return {"scores": [{"ref_index": i, "score": 0.0} for i in range(len(payload.references))]}

        sims = cosine_similarity(vect[0:1], vect[1:]).flatten()
        
        results = []
        for i, s in enumerate(sims):
            status = "high" if s > 0.7 else "medium" if s > 0.4 else "low"
            results.append({
                "ref_index": i,
                "score": float(s),
                "percentage": round(s * 100, 2),
                "status": status
            })
        
        return {
            "scores": results,
            "summary": {
                "total_references": len(payload.references),
                "highest_similarity": max(sims) if len(sims) > 0 else 0,
                "average_similarity": sum(sims) / len(sims) if len(sims) > 0 else 0
            }
        }
    except Exception as e:
        logger.exception("Error in /api/check_plagiarism")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """الحصول على إحصائيات النظام"""
    try:
        # حساب ملفات التحميل
        upload_files = [f for f in os.listdir("uploads") if f.endswith("_info.json")]
        
        return {
            "total_uploads": len(upload_files),
            "server_time": datetime.now().isoformat(),
            "server_uptime": "running",
            "features_enabled": {
                "pdf_processing": PyPDF2 is not None,
                "docx_processing": docx is not None,
                "ai_detection": True,
                "plagiarism_check": True,
                "multi_language": True
            },
            "storage_info": {
                "uploads_dir": "uploads/",
                "static_dir": "static/"
            }
        }
    except Exception as e:
        logger.exception("Error in /api/stats")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test")
async def test_endpoint():
    """نقطة وصول للاختبار"""
    return {
        "message": "✅ الخادم يعمل بنجاح!",
        "endpoints": [
            "/api/health",
            "/api/detect_ai",
            "/api/check_plagiarism",
            "/api/stats"
        ],
        "server_time": datetime.now().isoformat()
    }

# ========== معالجة أخطاء ==========

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": "الصفحة غير موجودة", "path": request.url.path}
    )

@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"خطأ في الخادم: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "حدث خطأ داخلي في الخادم"}
    )
'@ | Out-File -FilePath "main.py" -Encoding UTF8

Write-Host "✓ Created fresh main.py with UTF-8 encoding" -ForegroundColor Green