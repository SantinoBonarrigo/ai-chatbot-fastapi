# Chatbot with FastAPI, SQLite and Gemini

## Overview

This project is a full-stack chatbot built using FastAPI for the backend, SQLite for persistent storage, and a simple HTML/CSS/JavaScript frontend.
It integrates with the Gemini API to generate responses and stores the full chat history in a database.

## Features

* Real-time chat interface
* Persistent message history using SQLite
* Backend API built with FastAPI
* Integration with Gemini (Google AI)
* Dynamic frontend rendering with JavaScript
* Clean UI with chat bubbles (user vs assistant)

## Tech Stack

* Backend: FastAPI (Python)
* Database: SQLite
* Frontend: HTML, CSS, JavaScript
* AI: Gemini API (Google Generative AI)

## Project Structure

```
project/
│
├── main.py
├── requirements.txt
├── chat.db (ignored)
├── .env (ignored)
│
└── templates/
    └── index.html
```

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Create a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

## Run the App

```
uvicorn main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000
```

## API Endpoints

### GET /messages

Returns the full chat history.

### POST /chat

Send a message to the chatbot.

Body:

```
{
  "message": "Hello"
}
```

Response:

```
{
  "response": "Hi there!"
}
```

## Notes

* The database is stored locally using SQLite.
* `.env` and `chat.db` should not be committed.
* If Gemini API quota is exceeded, a fallback response is returned.

## Future Improvements

* Streaming responses (like ChatGPT)
* Multi-chat support (sessions)
* Authentication system
* Deployment (Render / Railway)
* UI improvements (typing indicator, animations)

## Author

Santino Bonarrigo
