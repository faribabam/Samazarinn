import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

app = FastAPI(title="Samazarinn Jewelry Store")

# ایجاد پوشه قالب‌ها در صورت عدم وجود برای جلوگیری از خطا هنگام اجرا
if not os.path.exists("templates"):
    os.makedirs("templates")

templates = Jinja2Templates(directory="templates")

# دیتای محصولات، دسته‌بندی‌ها و قیمت‌های زنده فرضی (قابل توسعه)
GOLD_PRODUCTS = [
    {
        "id": 1,
        "category": "necklace",
        "fa": {"name": "گردنبند برلیان سما", "desc": "طراحی لوکس با طلای ۱۸ عیار و نگین‌های برلیان پاک"},
        "en": {"name": "Sama Diamond Necklace", "desc": "Luxury 18k gold necklace with pristine diamond cuts"},
        "price_usd": 1200,
        "price_irr": 72000000,
        "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb" # در پروداکشن جایگزین با فایل glb طلا شود
    },
    {
        "id": 2,
        "category": "bracelet",
        "fa": {"name": "دستبند کارتیه زرین", "desc": "طراحی کلاسیک و ماندگار، کاملاً صیقل داده شده"},
        "en": {"name": "Zarrin Cartier Bracelet", "desc": "Classic timeless design, high-polish finish"},
        "price_usd": 850,
        "price_irr": 51000000,
        "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
    },
    {
        "id": 3,
        "category": "ring",
        "fa": {"name": "انگشتر سولیتیر پرنس", "desc": "تک نگین درخشان مناسب برای حلقه ازدواج و تعهد"},
        "en": {"name": "Prince Solitaire Ring", "desc": "Brilliant single stone ideal for engagement"},
        "price_usd": 650,
        "price_irr": 39000000,
        "model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
    }
]

class ChatMessage(BaseModel):
    message: str
    lang: str = "fa"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "products": GOLD_PRODUCTS})

@app.post("/api/ai-chat")
async def ai_assistant(data: ChatMessage):
    msg = data.message.lower().strip()
    lang = data.lang
    
    # موتور پاسخ‌دهی هوش مصنوعی محلی و سریع بر اساس کلیدواژه‌ها
    if lang == "fa":
        if "قیمت" in msg or "طلا" in msg:
            return JSONResponse({"response": "قیمت طلا به صورت لحظه‌ای محاسبه می‌شود. محصولات موجود در سایت با آخرین نرخ صنف طلا بروزرسانی شده‌اند."})
        elif "ارسال" in msg or "خرید" in msg:
            return JSONResponse({"response": "ارسال تمامی سفارشات سمازرین به سراسر کشور با بیمه کامل و پست پیشتاز رایگان انجام می‌شود."})
        elif "پشتیبانی" in msg or "ارتباط" in msg:
            return JSONResponse({"response": "شما می‌توانید از طریق دکمه‌های تلگرام و اینستاگرام در پایین صفحه مستقیماً با مدیریت در ارتباط باشید."})
        return JSONResponse({"response": "سلام! من مشاور هوشمند سمازرین هستم. چطور می‌توانم در انتخاب طلا و جواهرات به شما کمک کنم؟"})
    else:
        if "price" in msg or "gold" in msg:
            return JSONResponse({"response": "Gold prices are live. All products listed are automatically updated with the latest market rates."})
        elif "ship" in msg or "delivery" in msg:
            return JSONResponse({"response": "We provide secure insured worldwide shipping. National deliveries are completely free."})
        elif "support" in msg or "contact" in msg:
            return JSONResponse({"response": "You can reach our dynamic support 24/7 via the Telegram and Instagram action buttons below."})
        return JSONResponse({"response": "Hello! I am the Samazarinn AI Assistant. How can I help you choose your luxury piece today?"})

if __name__ == "__main__":
    uvicorn.run("main.py:app", host="0.0.0.0", port=8000, reload=True)
