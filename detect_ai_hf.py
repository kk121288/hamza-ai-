"""
مكتبة متقدمة لكشف النصوص المولدة بالذكاء الاصطناعي
دعم متعدد اللغات وخوارزميات متطورة
"""

import re
import math
from typing import Dict, List, Tuple
from datetime import datetime

def detect_language_simple(text: str) -> str:
    """كشف اللغة بطريقة مبسطة"""
    if not text:
        return "unknown"
    
    # عد الأحرف العربية
    arabic_count = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
    # عد الأحرف الإنجليزية
    english_count = sum(1 for char in text if 'a' <= char.lower() <= 'z')
    
    if arabic_count > english_count * 1.5:
        return "ar"
    elif english_count > arabic_count * 1.5:
        return "en"
    else:
        return "mixed"

def analyze_text_patterns(text: str, language: str = "ar") -> Dict:
    """تحليل الأنماط اللغوية"""
    patterns = {
        "ar": {
            "ai_indicators": [
                r'بالتأكيد', r'كمساعد', r'بصفتي', r'بناءً على', r'وفقًا ل',
                r'نموذج', r'خوارزمية', r'تدريب', r'معالجة', r'تحليل',
                r'يمكنني', r'أستطيع', r'بإمكاني', r'ينبغي', r'يجب'
            ],
            "human_indicators": [
                r'أعتقد', r'أظن', r'أشعر', r'في رأيي', r'برأيي',
                r'حسب', r'بناء على', r'أنا', r'شخصيًا', r'بنفسي',
                r'أتذكر', r'أذكر', r'أستحضر', r'على ما', r'ربما'
            ]
        },
        "en": {
            "ai_indicators": [
                r'as an AI', r'based on', r'according to', r'training data',
                r'language model', r'algorithm', r'processing', r'analysis',
                r'I can', r'I am able', r'should', r'must', r'necessary'
            ],
            "human_indicators": [
                r'I think', r'I believe', r'in my opinion', r'from my experience',
                r'personally', r'I remember', r'I feel', r'perhaps', r'maybe',
                r'in my view', r'as far as I know'
            ]
        }
    }
    
    lang_patterns = patterns.get(language, patterns["ar"])
    
    ai_score = 0
    human_score = 0
    
    for pattern in lang_patterns["ai_indicators"]:
        matches = re.findall(pattern, text, re.IGNORECASE)
        ai_score += len(matches) * 0.5
    
    for pattern in lang_patterns["human_indicators"]:
        matches = re.findall(pattern, text, re.IGNORECASE)
        human_score += len(matches) * 0.5
    
    return {"ai_score": ai_score, "human_score": human_score}

def calculate_complexity(text: str) -> Dict:
    """حساب تعقيد النص"""
    words = text.split()
    sentences = [s.strip() for s in re.split(r'[.!?؟]', text) if s.strip()]
    
    if not words or not sentences:
        return {
            "avg_sentence_length": 0,
            "vocab_diversity": 0,
            "word_count": 0
        }
    
    avg_sentence_len = sum(len(s.split()) for s in sentences) / len(sentences)
    unique_words = set(word.lower() for word in words if len(word) > 2)
    vocab_diversity = len(unique_words) / len(words) if words else 0
    
    return {
        "avg_sentence_length": round(avg_sentence_len, 2),
        "vocab_diversity": round(vocab_diversity, 3),
        "word_count": len(words),
        "unique_words": len(unique_words)
    }

def detect_ai_text_hf(text: str, max_length: int = 5000) -> Dict[str, float]:
    """
    دالة رئيسية لكشف النصوص المولدة بالذكاء الاصطناعي
    """
    if not text or not text.strip():
        return {
            "ai_probability": 0.5,
            "note": "النص فارغ",
            "confidence": 50,
            "language": "unknown"
        }
    
    # تقليل النص إذا كان طويلاً جداً
    if len(text) > max_length:
        text = text[:max_length]
        note = f"تم تحليل أول {max_length} حرف فقط"
    else:
        note = "تم تحليل النص بالكامل"
    
    # كشف اللغة
    language = detect_language_simple(text)
    
    # تحليل الأنماط
    pattern_results = analyze_text_patterns(text, language)
    
    # حساب التعقيد
    complexity = calculate_complexity(text)
    
    # حساب الاحتمالية الأساسية
    base_prob = 0.5
    
    # تعديل بناءً على الأنماط
    total_patterns = pattern_results["ai_score"] + pattern_results["human_score"]
    if total_patterns > 0:
        pattern_ratio = pattern_results["ai_score"] / total_patterns
        base_prob = 0.5 + (pattern_ratio - 0.5) * 0.3
    
    # تعديل بناءً على طول الجمل
    if complexity["avg_sentence_length"] > 25:
        base_prob = min(base_prob + 0.15, 0.9)
    elif complexity["avg_sentence_length"] < 10:
        base_prob = max(base_prob - 0.1, 0.1)
    
    # تعديل بناءً على تنوع المفردات
    if complexity["vocab_diversity"] < 0.4:
        base_prob = min(base_prob + 0.1, 0.9)
    elif complexity["vocab_diversity"] > 0.7:
        base_prob = max(base_prob - 0.1, 0.1)
    
    # حساب الثقة
    confidence = 50
    if complexity["word_count"] > 100:
        confidence += 20
    if abs(base_prob - 0.5) > 0.2:
        confidence += 15
    confidence = min(95, confidence)
    
    # تحديد النتيجة النهائية
    ai_probability = max(0.05, min(0.95, base_prob))
    
    # إنشاء ملاحظة مفصلة
    if ai_probability > 0.7:
        result_note = f"احتمالية عالية للذكاء الاصطناعي ({round(ai_probability*100)}%)"
    elif ai_probability > 0.55:
        result_note = f"احتمالية متوسطة للذكاء الاصطناعي ({round(ai_probability*100)}%)"
    elif ai_probability < 0.3:
        result_note = f"احتمالية عالية للبشرية ({round((1-ai_probability)*100)}%)"
    elif ai_probability < 0.45:
        result_note = f"احتمالية متوسطة للبشرية ({round((1-ai_probability)*100)}%)"
    else:
        result_note = "النتيجة غير حاسمة"
    
    return {
        "ai_probability": round(ai_probability, 4),
        "human_probability": round(1 - ai_probability, 4),
        "note": f"{note}. {result_note}",
        "confidence": confidence,
        "language": language,
        "analysis": {
            "word_count": complexity["word_count"],
            "sentence_count": len(re.split(r'[.!?؟]', text)),
            "avg_sentence_length": complexity["avg_sentence_length"],
            "vocab_diversity": complexity["vocab_diversity"],
            "ai_patterns_found": pattern_results["ai_score"],
            "human_patterns_found": pattern_results["human_score"]
        },
        "timestamp": datetime.now().isoformat()
    }

# دالة مساعدة للاختبار
def test_detection():
    """اختبار الدالة"""
    test_text = "هذا نص اختبار للتحقق من عمل النظام"
    result = detect_ai_text_hf(test_text)
    print("نتيجة الاختبار:")
    for key, value in result.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    test_detection()