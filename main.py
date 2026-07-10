import uvicorn
from fastapi import FastAPI
from routers import main_router, ai_models  

app = FastAPI(title="Ultimate Multi AI Hub Ecosystem")

app.include_router(main_router.router)
app.include_router(ai_models.router)

if __name__ == "__main__":
    print("🔥 Multi AI Hub tizimi muvaffaqiyatli ishga tushmoqda...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)