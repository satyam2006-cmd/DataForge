import os
from dotenv import load_dotenv
from google import genai
import tkinter as tk
from tkinter import scrolledtext

# Load environment variables 
load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")

if not API_KEY:
    raise RuntimeError("Please set GENAI_API_KEY in .env")

# Setup Gemini client 
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

# Chatbot Logic 
def send_message():
    user_msg = entry.get().strip()
    if not user_msg:
        return
    if user_msg.lower() == "exit":
        root.destroy()
        return

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {user_msg}\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)
    entry.delete(0, tk.END)

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=user_msg
        )
        bot_reply = response.text
    except Exception as e:
        bot_reply = f" Error: {str(e)}"

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"Bot: {bot_reply}\n\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

# GUI Setup
root = tk.Tk()
root.title("Chatbot🤖")
root.geometry("600x500")

# Chat display area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Input frame
frame = tk.Frame(root)
frame.pack(fill=tk.X, padx=10, pady=5)

entry = tk.Entry(frame, font=("Arial", 14))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(frame, text="Send", command=send_message, font=("Arial", 12))
send_button.pack(side=tk.RIGHT)

# Start GUI loop
root.mainloop()
