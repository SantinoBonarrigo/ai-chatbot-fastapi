from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from google import genai
import os
import sqlite3

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def init_db():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_message(role, content):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        (role, content)
    )
    conn.commit()
    conn.close()


def get_messages():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM messages ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]


init_db()


@app.get("/messages")
def get_chat_history():
    return {"messages": get_messages()}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message") or data.get("mensaje")

    if not user_message:
        return {"response": "No message received."}

    save_message("user", user_message)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_message
        )
        bot_reply = response.text
    except Exception as e:
        print("ERROR:", e)
        bot_reply = "AI is currently unavailable. Please try again later."

    save_message("assistant", bot_reply)

    return {"response": bot_reply}