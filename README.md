# 🩺 Medical AI Chatbot

An intelligent medical chatbot that interacts like a virtual doctor using AI.

## 🚀 Features

* 🤖 Conversational AI (doctor-like interaction)
* 🧠 Smart responses (asks questions only when needed)
* ✂️ Concise and readable answers
* 🔍 SBERT-based context retrieval
* ⚡ FastAPI backend
* 🎨 Modern React frontend UI

## 🧠 Tech Stack

* Python (FastAPI)
* Gemini API (LLM)
* SBERT (semantic search)
* React (frontend)

## 💬 How it Works

User → SBERT → Context → Gemini → Intelligent Response

## ▶️ Run Locally

### Backend

```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend-react
npm install
npm start
```

## 📌 Example

User: I have fever
Bot: Can you tell me your age and symptoms?

User: 22 and body pain
Bot: It could be a viral fever. You can take paracetamol and rest well.

## ⚠️ Disclaimer

This chatbot provides general medical advice and is not a substitute for professional medical consultation.

## 👩‍💻 Author

Vaishnavi Lilhare
Tanvi Bhoyar
