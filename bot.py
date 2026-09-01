import os
import base64
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# خودانێن فەرمی یێن بۆتی
OWNERS = ["YUSEEF_SURCHI", "Arthur3345"]
CHANNEL_NAME = "LEGEND_MODS33"

# دامەزراندنا داتابەیسا پێشکەفتی
def init_db():
    conn = sqlite3.connect('legend_empire.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            username TEXT,
            user_request TEXT,
            repo_name TEXT,
            live_link TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8866947821:AAGCnFW-TddT0MMbOYBxvbqfpOMMcNPOznk")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "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") 
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "yosfsinan50-cpu") 

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "yosfsinan50@gmail.com")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "rayan1328262")

# فەرمانا /start ب شێوازەکێ زەبەلاح و پڕۆفیشناڵ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = f"@{user.username}" if user.username else user.first_name
    
    keyboard = [
        [InlineKeyboardButton("📢 چەناڵا فەرمی", url=f"https://t.me/{CHANNEL_NAME}")],
        [InlineKeyboardButton("👑 خودانێن بۆتی", url=f"https://t.me/{OWNERS[0]}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"🌟 **بێخێر هاتن بۆ لایێ AI Build Website Legend Bot V3!**\n\n"
        f"👤 سلاڤ {username}!\n"
        f"ئەڤ بۆتە مەزنترین سیستەمە بۆ دروستکرنا هەر جۆرە وێبسایتەکێ ب ڕێکا AI و داتابەیسێ.\n\n"
        f"👑 **خودان:** @{OWNERS[0]} دگەل @{OWNERS[1]}\n"
        f"📢 **چەناڵ:** @{CHANNEL_NAME}\n\n"
        f"✨ *نوکە تەنها پەیامەکی بنێرە و بێژە من تو دخوازی چ جۆرە وێبسایتی بۆ تە چێکەم!*"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)

# فەرمانا ئاماران (/stats) تایبەت ب خودانان
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if user.username not in OWNERS:
        await update.message.reply_text("⛔ لێبوورین، ئەڤ فەرمانە تەنها بۆ خودانێن بۆتی یە!")
        return

    try:
        conn = sqlite3.connect('legend_empire.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM websites")
        total_sites = cursor.fetchone()[0]
        conn.close()

        await update.message.reply_text(
            f"📊 **ئامارێن بۆتێ Legend Empire:**\n\n"
            f"🌐 گشتی وێبسایتێن هاتینە چێکرن: **{total_sites}**\n"
            f"🚀 سیستەم ب سەرکەفتیانە کار دکەت و یێ ئامادەیە!"
        )
    except Exception as e:
        await update.message.reply_text(f"خەلەتی: {e}")

# وەرگرتنا داخوازان و چێکرنا وێبسایتان
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = str(update.message.chat_id)
    user = update.message.from_user
    username = f"@{user.username}" if user.username else (user.first_name or "بەکارهێنەر")
    
    await context.bot.send_message(
        chat_id=chat_id, 
        text=f"🚀 هەیڤال {username}!\nمژارا تە هاتە وەرگرت: *{user_message}*\n\n🤖 AI دگەل پشکێن پڕۆگرامکرنا پێشکەفتی نوکە دەست ب چێکرنێ دکەت...",
        parse_mode="Markdown"
    )

    website_html = f"""
<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legend Empire - {username}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }}
        body {{ background: linear-gradient(135deg, #030712, #1e1b4b); color: #fff; min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }}
        .container {{ background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.15); padding: 45px; border-radius: 28px; max-width: 680px; width: 100%; text-align: center; box-shadow: 0 25px 60px rgba(0,0,0,0.8); }}
        h1 {{ color: #38bdf8; font-size: 32px; margin-bottom: 15px; text-shadow: 0 2px 8px rgba(56,189,248,0.4); }}
        p {{ color: #cbd5e1; font-size: 16px; line-height: 1.8; margin-bottom: 20px; }}
        .request-box {{ background: rgba(30, 41, 59, 0.7); border-right: 6px solid #6366f1; padding: 18px; border-radius: 12px; margin: 25px 0; text-align: right; color: #f8fafc; font-weight: bold; font-size: 17px; }}
        .owners-card {{ background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.3); padding: 18px; border-radius: 14px; margin-top: 25px; }}
        .owners-card h3 {{ color: #a855f7; font-size: 17px; margin-bottom: 8px; }}
        .owners-card p {{ font-size: 15px; color: #38bdf8; margin: 0; }}
        .badge {{ display: inline-block; background: linear-gradient(135deg, #6366f1, #a855f7); color: #fff; padding: 12px 25px; border-radius: 50px; font-size: 15px; font-weight: bold; margin-top: 25px; box-shadow: 0 6px 20px rgba(99,102,241,0.5); }}
        .footer {{ margin-top: 30px; font-size: 13px; color: #64748b; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>✨ شاهکارێ وێبسایتا تە هاتە دروستکرن</h1>
        <p>ئەڤ وێبسایتە تایبەت بۆ بەکارهێنەر <strong>{username}</strong> هاتە دیزاینکرن ل گۆڕەی دوماهین تکنۆلۆژیایێن AI.</p>
        <div class="request-box">🎯 داخوازا تە: {user_message}</div>
        
        <div class="owners-card">
            <h3>👑 خودانێن پڕۆژێ و پێشکێشکەر:</h3>
            <p>@{OWNERS[0]} & @{OWNERS[1]} | چەناڵ: @{CHANNEL_NAME}</p>
        </div>

        <div class="badge">AI Build Website Legend Bot V3</div>
        <div class="footer">Powered by Legend Mods Empire & Yusef Sinan</div>
    </div>
</body>
</html>
"""

    repo_name = f"legend-empire-{chat_id}"
    gh_headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    gh_data = {
        "name": repo_name,
        "description": f"Empire Website for {username} - Request: {user_message}",
        "private": False,
        "auto_init": True
    }
    
    repo_response = requests.post("https://api.github.com/user/repos", headers=gh_headers, json=gh_data)
    
    if repo_response.status_code == 201:
        file_content_encoded = base64.b64encode(website_html.encode('utf-8')).decode('utf-8')
        file_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/index.html"
        file_data = {
            "message": f"Deploy automated index.html for {username}",
            "content": file_content_encoded
        }
        requests.put(file_url, headers=gh_headers, json=file_data)

        repo_link = f"https://github.com/{GITHUB_USERNAME}/{repo_name}"
        live_link = f"https://{GITHUB_USERNAME}.github.io/{repo_name}/"

        try:
            conn = sqlite3.connect('legend_empire.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO websites (chat_id, username, user_request, repo_name, live_link) VALUES (?, ?, ?, ?, ?)",
                           (chat_id, username, user_message, repo_name, live_link))
            conn.commit()
            conn.close()
        except Exception as db_err:
            print(f"خەلەتی د داتابەیسێ دا: {db_err}")

        reply_text = (
            f"✅ **پیرۆزە {username}! وێبسایتێ تە ب سەرکەفتیانە هاتە چێکرن.**\n\n"
            f"🌐 **لینکێ ڕاستەوخۆ (Live Preview):**\n{live_link}\n\n"
            f"📂 **رێپۆزێتۆریا گیتهەب:**\n{repo_link}\n\n"
            f"👑 **خودان:** @{OWNERS[0]} دگەل @{OWNERS[1]}\n"
            f"📢 **چەناڵ:** @{CHANNEL_NAME}\n\n"
            f"📧 زانیاریێن وێبسایتێ بۆ گیماپێ تە (`{SENDER_EMAIL}`) هاتە هناردن!"
        )
        await context.bot.send_message(chat_id=chat_id, text=reply_text, parse_mode="Markdown")

        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = SENDER_EMAIL
            msg['Subject'] = f"🚀 وێبسایتێ نوی هاتە چێکرن بۆ {username}"
            
            email_body = f"""
سلاڤ یوسف،
بۆتێ تە یێ Legend AI Empire V3 وێبسایتەکێ نوی بۆ بەکارهێنەر ({username}) چێکر!
Zanyarî: {live_link}
            """
            msg.attach(MIMEText(email_body, 'plain', 'utf-8'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, SENDER_EMAIL, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"خەلەتی د هناردنا گیماڵی دا: {e}")

    else:
        await context.bot.send_message(
            chat_id=chat_id, 
            text="⚠️ ببورە، چێکرنا ڕیپۆزێتۆریێ سەرکەفتی نەبوو. لطفا گیتەهەب تەکۆنێ خۆ پشکنە."
        )

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command)) # لێرە گۆڕی بۆ stats_command
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 Legend AI Empire Bot V3 دەست بە کار بوو...")
    app.run_polling()

if __name__ == "__main__":
    main()
