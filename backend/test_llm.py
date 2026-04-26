import google.generativeai as genai

# 🔐 Setup API Key
genai.configure(api_key="AIzaSyBgFr99HRPz70DGfUdS4ATETVa0c693crM")

# 🧠 Smart doctor-like system prompt
system_prompt = """
You are a professional medical assistant like a doctor.

Your goal is to help the user correctly and safely.

Rules:

- Understand the query carefully.
- If the question is clear → give a direct answer.
- If important info is missing → ask follow-up questions.
- Do NOT ask unnecessary questions.
- Keep responses concise (3–5 lines max).
- Use simple, natural conversational language.
- Avoid long paragraphs.
- Avoid bullet points unless necessary.
- Only suggest medicines when enough information is available.

Act like a real doctor helping a patient.
"""

# 🚀 Initialize model with system behavior
model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=system_prompt
)

# 💬 Start chat with memory
chat = model.start_chat(history=[])

print("AI: Hello! I am your medical assistant. Type 'exit' to end.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("AI: Goodbye!")
        break

    # 🔥 optional context (you can later connect SBERT here)
    context = "No additional medical context available."

    prompt = f"""
Context: {context}

User: {user_input}
"""

    response = chat.send_message(prompt)

    print(f"\nAI: {response.text}\n")