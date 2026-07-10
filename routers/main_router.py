import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai  
from dotenv import load_dotenv  

load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="templates")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    if GEMINI_API_KEY:
        ai_client = genai.Client(api_key=GEMINI_API_KEY)
    else:
        print("⚠️ Diqqat: .env faylida GEMINI_API_KEY topilmadi!")
        ai_client = None
except Exception as e:
    print(f"⚠️ Gemini API yuklanishda xato: {e}")
    ai_client = None

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"active_page": "home"}
    )

@router.post("/chat", response_class=HTMLResponse)
async def gen_ai_chat(request: Request, message: str = Form(...)):
    
    if not ai_client:
        bot_response = f".env faylidan API kalit yuklanmadi. Siz yozgan xabar: '{message}'"
    else:
        try:
            system_instruction = (
                "Siz Shoxrux tomonidan yaratilgan 'Multi AI Hub' ekotizimining universal, "
                "o'ta aqlli va xushmuomala yordamchisiz. Foydalanuvchining har qanday savoliga "
                "aniq, lof urmasdan va chiroyli o'zbek tilida javob bering. Promptingizga RAG ulangan."
            )
            
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=message,
                config={'system_instruction': system_instruction}
            )
            bot_response = response.text
        except Exception as e:
            bot_response = f"Gemini LLM modelidan javob olishda xatolik: {str(e)}"
        
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={
            "active_page": "home", 
            "user_message": message, 
            "bot_response": bot_response
        }
    )

@router.get("/model/1", response_class=HTMLResponse)
async def get_model1(request: Request):
    return templates.TemplateResponse(request=request, name="model1.html", context={"active_page": "model1"})

@router.get("/model/2", response_class=HTMLResponse)
async def get_model2(request: Request):
    return templates.TemplateResponse(request=request, name="model2.html", context={"active_page": "model2"})

@router.get("/model/3", response_class=HTMLResponse)
async def get_model3(request: Request):
    return templates.TemplateResponse(request=request, name="model3.html", context={"active_page": "model3"})

@router.get("/model/4", response_class=HTMLResponse)
async def get_model4(request: Request):
    return templates.TemplateResponse(request=request, name="model4.html", context={"active_page": "model4"})