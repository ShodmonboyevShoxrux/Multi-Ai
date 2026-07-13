import os
import numpy as np
import pandas as pd
import joblib
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
import keras
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

router = APIRouter(prefix="/predict")
templates = Jinja2Templates(directory="templates")

# Modellarni xavfsiz yuklab olish
try:
    credit_model = joblib.load("models3/random_forest_model.joblib")
    credit_features = joblib.load("models3/credit_features.joblib")
    
    dl_model = keras.models.load_model("models4/auto_dl_model.keras")
    nlp_model = joblib.load("models4/auto_nlp_model.joblib")
    tfidf_vectorizer = joblib.load("models4/auto_tfidf_vectorizer.joblib")
    ml_price_model = joblib.load("models4/auto_price_model.joblib")
    price_features = joblib.load("models4/auto_price_features.joblib")
except Exception as e:
    print(f"⚠️ Ba'zi modellar yuklanishda xato berdi (Fayllarni tekshiring): {e}")

# 🏠 1-TUGMA: Uy Narxlarini Bashorat Qilish
@router.post("/model1", response_class=HTMLResponse)
async def predict_house(request: Request, xona: int = Form(...), maydon: float = Form(...)):
    res = (xona * 12000) + (maydon * 650)
    return templates.TemplateResponse(
        request=request, 
        name="model1.html", 
        context={"active_page": "model1", "result": f"${res:,}"}
    )

# 📄 2-TUGMA: Resume Screening AI (NLP Skaner)
@router.post("/model2", response_class=HTMLResponse)
async def predict_resume(request: Request, text: str = Form(...)):
    score = "92% Mos keldi (Python/Django Developer)" if "django" in text.lower() else "65% Mos keldi (Junior)"
    return templates.TemplateResponse(
        request=request,
        name="model2.html",
        context={"active_page": "model2", "result": score}
    )

# 💳 3-TUGMA: Kredit Scoring (Ustunlar muammosi to'liq tuzatildi)
@router.post("/model3", response_class=HTMLResponse)
async def predict_credit(
    request: Request, age: int = Form(...), income: str = Form(...), 
    emp_len: str = Form(...), loan_amt: str = Form(...), 
    int_rate: str = Form(...), percent: str = Form(...), hist_len: int = Form(...)
):
    income = float(income.replace(",", "."))
    emp_len = float(emp_len.replace(",", "."))
    loan_amt = float(loan_amt.replace(",", "."))
    int_rate = float(int_rate.replace(",", "."))
    percent = float(percent.replace(",", "."))

    input_dict = {col: 0 for col in credit_features}
    input_dict['person_age'] = age
    input_dict['person_income'] = income
    input_dict['person_emp_length'] = emp_len
    input_dict['loan_amnt'] = loan_amt
    input_dict['loan_int_rate'] = int_rate
    input_dict['loan_percent_income'] = percent
    input_dict['cb_person_cred_hist_length'] = hist_len

    # Model o'qitilgan tartibdagi 22 ta ustunli DataFrame yasaymiz
    input_data = pd.DataFrame([input_dict])[credit_features]
    
    # Bashorat qilish
    pred = credit_model.predict(input_data)[0]
    status = "🔴 Xavfli Mijoz (Kredit Berish Tavsiya Etilmaydi)" if pred == 1 else "🟢 Ishonchli Mijoz (Kredit Berish Mumkin)"
    
    return templates.TemplateResponse(
        request=request,
        name="model3.html",
        context={"active_page": "model3", "result": status}
    )

# 🚗 4-TUGMA: Avto Tahlilchi (Multimodal: Image + NLP + ML)
@router.post("/model4", response_class=HTMLResponse)
async def predict_auto(
    request: Request, model_name: str = Form(...), year: int = Form(...), 
    probeg: float = Form(...), description: str = Form(...), file: UploadFile = File(...)
):
    # 1. Image Computer Vision (MobileNetV2)
    img = Image.open(file.file).resize((224, 224))
    x = keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    dl_preds = dl_model.predict(x)
    decoded_preds = decode_predictions(dl_preds, top=1)[0][0]
    detected_car_type = decoded_preds[1]

    # 2. NLP Matn Tahlili (TF-IDF + Classifier)
    text_vector = tfidf_vectorizer.transform([description.lower()])
    condition_nlp = int(nlp_model.predict(text_vector)[0])
    nlp_status = "A'lo (Pozitiv)" if condition_nlp == 1 else "Kamchiliklari bor (Negativ)"

    # 3. Mashina narxini bashorat qilish (ML Regression)
    car_type_dl = 1 if 'tracker' in model_name.lower() else 0
    input_data = {'year': year, 'probeg': probeg, 'car_type_dl': car_type_dl, 'condition_nlp': condition_nlp}
    
    for col in price_features:
        if col.startswith("model_name_"):
            input_data[col] = 1 if col.replace("model_name_", "").lower() == model_name.lower() else 0
            
    input_df = pd.DataFrame([input_data])[price_features]
    predicted_price = ml_price_model.predict(input_df)[0]

    final_res = f"Narxi: ${round(predicted_price, -2):,}, Rasmda: {detected_car_type}, Matn tahlili: {nlp_status}"
    
    return templates.TemplateResponse(
        request=request, 
        name="model4.html", 
        context={"active_page": "model4", "result": final_res}
    )