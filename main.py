import os
import random
import requests
import telebot
import google.generativeai as genai
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")      # Telegram BotFather token
GEMINI_KEY = os.getenv("GEMINI_KEY")    # Gemini API key

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable set karo")

bot = telebot.TeleBot(BOT_TOKEN)

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

SYSTEM_PROMPT = """
Tum ek friendly AI companion ho. Dost ki tarah baat karo.
Kabhi human/girlfriend hone ka jhooth mat bolo.
User coding mange to clear code do.
Safe, respectful aur helpful reply do.
Hindi/Hinglish me natural baat karo.
"""

reactions = ["😊", "🔥", "💯", "✨", "😄", "👍", "🤝"]
gifts = [
    "🎁 Ye lo virtual gift!",
    "🌹 Ek safe virtual flower!",
    "🍫 Virtual chocolate!",
    "⭐ Tumhare liye good-luck star!",
    "🎮 Gaming energy gift!"
]

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("💬 Chat", "📸 Photo")
    kb.row("🎁 Gift", "💻 Coding Help")
    kb.row("😂 Reaction", "ℹ️ Help")
    return kb

def ai_reply(text):
    if not model:
        return (
            "AI key set nahi hai, isliye simple mode chal raha hai.\n\n"
            "Gemini key add karo: GEMINI_KEY environment variable me."
        )

    try:
        prompt = SYSTEM_PROMPT + "\nUser: " + text
        res = model.generate_content(prompt)
        return res.text.strip()
    except Exception as e:
        return f"AI error: {e}"

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Hey! Main tumhara AI Friend Bot hoon 🤖\n"
        "Chat, photo, gift, coding help sab kar sakta hoon.",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "Commands:\n"
        "/start - bot start\n"
        "/photo - random photo\n"
        "/gift - virtual gift\n"
        "/code - coding help\n\n"
        "Normal message bhejo, main reply karunga."
    )

@bot.message_handler(commands=["photo"])
def send_photo(message):
    url = "https://picsum.photos/800/600"
    bot.send_photo(message.chat.id, url, caption="Ye lo random safe photo 📸")

@bot.message_handler(commands=["gift"])
def send_gift(message):
    bot.send_message(message.chat.id, random.choice(gifts))

@bot.message_handler(commands=["code"])
def code_help(message):
    bot.send_message(message.chat.id, "Coding question bhejo, main code bana dunga 💻")

@bot.message_handler(content_types=["text"])
def chat(message):
    text = message.text.strip()

    if text == "📸 Photo":
        return send_photo(message)

    if text == "🎁 Gift":
        return send_gift(message)

    if text == "😂 Reaction":
        return bot.send_message(message.chat.id, random.choice(reactions))

    if text == "💻 Coding Help":
        return bot.send_message(message.chat.id, "Apna coding task bhejo, jaise: Python calculator code do")

    if text == "ℹ️ Help":
        return help_cmd(message)

    bot.send_chat_action(message.chat.id, "typing")

    reply = ai_reply(text)

    if len(reply) > 3900:
        reply = reply[:3900] + "\n\n...reply long tha, cut ho gaya."

    bot.send_message(message.chat.id, reply)

print("Bot started...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
