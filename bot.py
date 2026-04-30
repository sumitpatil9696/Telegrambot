import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

# 🔥 ADD THIS (Flask part)
from flask import Flask
import threading

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

# ================= SETTINGS =================
TOKEN = "8629584902:AAEuAPMIW6V0eTaRRxxwvmWT7EMbGl3r3zU"
ADMIN_ID = 7156406347
ADMIN_USERNAME = "Taskman96"

FREE_CHANNEL_LINK = "https://t.me/+GFi7yL9PNqhlN2I1"
PREMIUM_CHANNEL_LINK = "https://t.me/+WIBBIo-JaMljZjM1"

PRICE = "₹30"
QR_FILE = "payment_qr.png"
USERS_FILE = "users.json"
# ============================================

bot = telebot.TeleBot(TOKEN)
pending_payments = {}

# ---------- USER DATABASE ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def add_user(user):
    users = load_users()
    if not any(u["id"] == user.id for u in users):
        users.append({
            "id": user.id,
            "name": user.first_name,
            "username": user.username if user.username else "NoUsername",
            "premium": False
        })
        save_users(users)

def give_premium(user_id):
    users = load_users()
    for u in users:
        if u["id"] == user_id:
            u["premium"] = True
    save_users(users)

# ---------- START ----------
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔓 Free Channel", url=FREE_CHANNEL_LINK),
        InlineKeyboardButton("💎 Buy Premium", callback_data="premium")
    )

    bot.send_message(
        message.chat.id,
        "Welcome 👋\n\nChoose your access type below.",
        reply_markup=markup
    )

# ---------- PREMIUM BUTTON ----------
@bot.callback_query_handler(func=lambda call: call.data == "premium")
def premium(call):
    bot.answer_callback_query(call.id)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📩 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")
    )

    if os.path.exists(QR_FILE):
        with open(QR_FILE, "rb") as photo:
            bot.send_photo(
                call.message.chat.id,
                photo,
                caption=f"💎 PREMIUM ACCESS\n\n💰 Price: {PRICE}\n\n📌 Scan QR and pay.\nSend payment screenshot here.",
                reply_markup=markup
            )
    else:
        bot.send_message(
            call.message.chat.id,
            f"⚠ QR file not found!\n\n💰 Price: {PRICE}\nSend screenshot after payment.",
            reply_markup=markup
        )

# ---------- CAPTURE SCREENSHOT ----------
@bot.message_handler(content_types=['photo'])
def screenshot_handler(message):

    user_id = message.from_user.id

    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)

    if user and user["premium"]:
        bot.send_message(user_id, "✅ You already have premium access.")
        return

    file_id = message.photo[-1].file_id
    pending_payments[user_id] = file_id

    markup = InlineKeyboardMarkup()
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

# 🔥 ADD THIS (Flask part)
from flask import Flask
import threading

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_web).start()

# ================= SETTINGS =================
TOKEN = "8629584902:AAEuAPMIW6V0eTaRRxxwvmWT7EMbGl3r3zU"
ADMIN_ID = 7156406347
ADMIN_USERNAME = "Taskman96"

FREE_CHANNEL_LINK = "https://t.me/+GFi7yL9PNqhlN2I1"
PREMIUM_CHANNEL_LINK = "https://t.me/+WIBBIo-JaMljZjM1"

PRICE = "₹30"
QR_FILE = "payment_qr.png"
USERS_FILE = "users.json"
# ============================================

bot = telebot.TeleBot(TOKEN)
pending_payments = {}

# ---------- USER DATABASE ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def add_user(user):
    users = load_users()
    if not any(u["id"] == user.id for u in users):
        users.append({
            "id": user.id,
            "name": user.first_name,
            "username": user.username if user.username else "NoUsername",
            "premium": False
        })
        save_users(users)

def give_premium(user_id):
    users = load_users()
    for u in users:
        if u["id"] == user_id:
            u["premium"] = True
    save_users(users)

# ---------- START ----------
@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔓 Free Channel", url=FREE_CHANNEL_LINK),
        InlineKeyboardButton("💎 Buy Premium", callback_data="premium")
    )

    bot.send_message(
        message.chat.id,
        "Welcome 👋\n\nChoose your access type below.",
        reply_markup=markup
    )

# ---------- PREMIUM BUTTON ----------
@bot.callback_query_handler(func=lambda call: call.data == "premium")
def premium(call):
    bot.answer_callback_query(call.id)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📩 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")
    )

    if os.path.exists(QR_FILE):
        with open(QR_FILE, "rb") as photo:
            bot.send_photo(
                call.message.chat.id,
                photo,
                caption=f"💎 PREMIUM ACCESS\n\n💰 Price: {PRICE}\n\n📌 Scan QR and pay.\nSend payment screenshot here.",
                reply_markup=markup
            )
    else:
        bot.send_message(
            call.message.chat.id,
            f"⚠ QR file not found!\n\n💰 Price: {PRICE}\nSend screenshot after payment.",
            reply_markup=markup
        )

# ---------- CAPTURE SCREENSHOT ----------
@bot.message_handler(content_types=['photo'])
def screenshot_handler(message):

    user_id = message.from_user.id

    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)

    if user and user["premium"]:
        bot.send_message(user_id, "✅ You already have premium access.")
        return

    file_id = message.photo[-1].file_id
    pending_payments[user_id] = file_id

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
    )

    username = message.from_user.username if message.from_user.username else "NoUsername"

    bot.send_photo(
        ADMIN_ID,
        file_id,
        caption=f"Payment screenshot from {message.from_user.first_name} (@{username})",
        reply_markup=markup
    )

    bot.send_message(user_id, "📨 Screenshot received. Wait for admin approval.")

# ---------- ADMIN DECISION ----------
@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_") or call.data.startswith("reject_"))
def admin_decision(call):

    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Not authorized")
        return

    action, user_id = call.data.split("_")
    user_id = int(user_id)

    if action == "approve":
        give_premium(user_id)
        bot.send_message(
            user_id,
            f"✅ Payment Approved!\n\nJoin Premium:\n{PREMIUM_CHANNEL_LINK}"
        )
        bot.answer_callback_query(call.id, "Approved")

    elif action == "reject":
        bot.send_message(
            user_id,
            "❌ Payment Rejected. Contact admin."
        )
        bot.answer_callback_query(call.id, "Rejected")

# ---------- ADMIN PANEL ----------
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📊 Stats", callback_data="admin_stats"),
        InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
    )
    markup.add(
        InlineKeyboardButton("👥 Users List", callback_data="admin_list"),
        InlineKeyboardButton("📄 Export CSV", callback_data="admin_export")
    )

    bot.send_message(message.chat.id, "🎛 Admin Panel", reply_markup=markup)

# ---------- ADMIN BUTTON HANDLER ----------
@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def admin_buttons(call):

    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Not allowed")
        return

    data = call.data

    if data == "admin_stats":
        users = load_users()
        total = len(users)
        premium = len([u for u in users if u["premium"]])
        free = total - premium

        bot.send_message(
            call.message.chat.id,
            f"📊 BOT STATS\n\n👥 Total: {total}\n💎 Premium: {premium}\n🆓 Free: {free}"
        )

    elif data == "admin_list":
        users = load_users()
        text = "👥 USER LIST\n\n"

        for u in users:
            text += f"{u['id']} | {u['name']} | @{u['username']} | Premium: {u['premium']}\n"

        for i in range(0, len(text), 4000):
            bot.send_message(call.message.chat.id, text[i:i+4000])

    elif data == "admin_broadcast":
        bot.send_message(call.message.chat.id, "📢 Use:\n/broadcast Your message")

    elif data == "admin_export":
        bot.send_message(call.message.chat.id, "📄 CSV export next step madhe add karu")

# ---------- RUN ----------
print("🔥 Bot Running Successfully 🔥")
bot.infinity_polling()
