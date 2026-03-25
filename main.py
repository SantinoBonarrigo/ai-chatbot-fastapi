from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()  # load variables from .env

app = FastAPI()  # create app
templates = Jinja2Templates(directory="templates")  # HTML templates folder

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # Gemini client

chat_history = []  # store conversation history


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()  # get JSON from frontend
    user_message = data.get("message") or data.get("mensaje")  # accept both keys

    if not user_message:
        return {"response": "No message received."}

    # save user message
    chat_history.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    try:
        # try Gemini first
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=chat_history
        )
        bot_reply = response.text

    except Exception as e:
        print("ERROR:", e)
        # fallback so the app still works
        bot_reply = f"Echo: {user_message}"

    # save bot reply
    chat_history.append({
        "role": "model",
        "parts": [{"text": bot_reply}]
    })

    return {"response": bot_reply}