from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from google import genai
import os
import sqlite3  # built-in Python library for SQLite databases
load_dotenv()  # load variables from .env





app = FastAPI()  # create app
templates = Jinja2Templates(directory="templates")  # HTML templates folder

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  # Gemini client

chat_history = []  # store conversation history

def init_db():
    conn = sqlite3.connect("chat.db")  # create or open database file
    cursor = conn.cursor()              # create cursor to execute SQL

    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, role text NOT NULL, content text NOT NULL)")

    conn.commit()   # save changes
    conn.close()   # close connection
init_db()  # initialize database on startup

def save_message(role, content):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO messages (role,content) VALUES (?, ?)",
        (role, content)
    )
    
    conn.commit()
    conn.close()



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

    save_message("user", user_message)    # después del append del usuario
    try:
        # try Gemini first
        response = client.models.generate_content(
            model="gemini-2.0-flash",
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
    save_message("model", bot_reply)   # después del append del bot

    return {"response": bot_reply}