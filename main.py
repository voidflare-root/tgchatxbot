import os
import random
import telebot
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")
if not GEMINI_KEY:
    raise ValueError("GEMINI_KEY missing")

bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=GEMINI_KEY)

SYSTEM = """
Tum ek AI friend bot ho.
Friendly Hinglish me baat karo.
Human ya real girlfriend hone ka jhooth mat bolo.
Coding mange to direct working code do.
Photo mange to safe random photo do.
GIF/gift mange to cute safe GIF bhejo.
Respectful aur safe reply do.
"""

gifs = [
    "https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif",
    "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/5GoVLqeAOo6PK/giphy.gif"
]

reactions = ["😊", "😂", "🔥", "💯", "✨", "👍", "🤝", "😄"]

def ask_ai(user_text):
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=SYSTEM + "\nUser: " + user_text
        )
        return response.text or "Samajh gaya 😊"
    except Exception as e:
        return f"AI error: {e}"

def send_photo(chat_id):
    bot.send_photo(
        chat_id,
        "https://picsum.photos/800/600",
        caption="Ye lo safe random photo 📸"
    )

def send_gif(chat_id):
    bot.send_animation(
        chat_id,
        random.choice(gifs),
        caption="🎁 Ye lo tumhare liye GIF"
    )

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Hey! Main AI Friend Bot hoon 🤖\n\n"
        "Normal message bhejo.\n"
        "Photo chahiye to: photo do\n"
        "GIF chahiye to: gif do\n"
        "Reaction chahiye to: reaction do\n"
        "Coding ke liye: python code do"
    )

@bot.message_handler(content_types=["text"])
def handle_text(message):
    text = message.text.strip()
    low = text.lower()

    bot.send_chat_action(message.chat.id, "typing")

    if low.startswith("/"):
        bot.send_message(message.chat.id, "Sirf /start command available hai.")
        return

    if any(word in low for word in ["photo", "pic", "image", "tasveer"]):
        send_photo(message.chat.id)
        return

    if any(word in low for word in ["gif", "gift", "animation"]):
        send_gif(message.chat.id)
        return

    if any(word in low for word in ["reaction", "react", "emoji"]):
        bot.send_message(message.chat.id, random.choice(reactions))
        return

    reply = ask_ai(text)

    if len(reply) > 3900:
        reply = reply[:3900] + "\n\n...reply long tha."

    bot.send_message(message.chat.id, reply)

print("Bot started...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
