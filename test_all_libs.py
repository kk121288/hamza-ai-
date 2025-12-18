# -*- coding: utf-8 -*-

# اختبار مكتبة numpy
try:
    import numpy as np
    print(" تم استيراد مكتبة numpy بنجاح")
    arr = np.array([1, 2, 3])
    print("مثال numpy:", arr)
except Exception as e:
    print(" خطأ في استيراد numpy:", e)

# اختبار مكتبة pandas
try:
    import pandas as pd
    print(" تم استيراد مكتبة pandas بنجاح")
    df = pd.DataFrame({"الاسم": ["أحمد", "سارة", "محمد"], "العمر": [25, 30, 28]})
    print("مثال pandas:\n", df)
except Exception as e:
    print(" خطأ في استيراد pandas:", e)

# اختبار مكتبة matplotlib مع رسم بياني من بيانات pandas
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    print(" تم استيراد مكتبة matplotlib بنجاح")
    plt.bar(df["الاسم"], df["العمر"], color="skyblue")
    plt.title("أعمار الأشخاص")
    plt.xlabel("الاسم")
    plt.ylabel("العمر")
    plt.savefig("test_plot.png")
    print(" تم إنشاء الرسم البياني وحفظه في test_plot.png")
except Exception as e:
    print(" خطأ في استيراد matplotlib:", e)

# اختبار مكتبة scikit-learn
try:
    from sklearn.linear_model import LinearRegression
    print(" تم استيراد مكتبة scikit-learn بنجاح")
    model = LinearRegression()
    print("مثال scikit-learn: تم إنشاء نموذج الانحدار الخطي")
except Exception as e:
    print(" خطأ في استيراد scikit-learn:", e)

# اختبار مكتبة transformers
try:
    import transformers
    print(" تم استيراد مكتبة transformers بنجاح (بدون تنزيل نموذج)")
except Exception as e:
    print(" خطأ في استيراد transformers:", e)

# اختبار مكتبة PyTorch
try:
    import torch
    print(" تم استيراد مكتبة PyTorch بنجاح")
    x = torch.tensor([1.0, 2.0, 3.0])
    print("مثال PyTorch:", x)
except Exception as e:
    print(" خطأ في استيراد PyTorch:", e)
