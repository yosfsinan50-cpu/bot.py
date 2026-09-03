import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Logging setup
logging.basicConfig(format="%(asctime)s - OWNER: @YUSEEF_SURCHI - ADMIN: @Arthur3345 - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# یوزەرێن خودان و ئادمێن ب بێ خەلەتی
OWNER = "@YUSEEF_SURCHI"
ADMIN = "@Arthur3345"
BOT_TOKEN = "8927058505:AAG_hzN29-Cw5DyROpUaopDvugnGQN6BYek"

# Home Keyboard Menu
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🎨 چێکرنا ستیکەری (تا 15 چرکە / ب تێکست و بێ تێکست)", callback_data="sticker_options")],
        [InlineKeyboardButton("✨ 280 فلتەرێن پیشەگەر بۆ ستیکەریان", callback_data="filters_menu")],
        [InlineKeyboardButton("💎 800 تایبەتمەندیێن پێشکەتی و Animation Text", callback_data="features_800")],
        [InlineKeyboardButton(f"👑 خودان: {OWNER}", url="https://t.me/YUSEEF_SURCHI")],
        [InlineKeyboardButton(f"🛡️ ئادمێن: {ADMIN}", url="https://t.me/Arthur3345")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"🌟 **سلاڤ ل تە هێژا {user.first_name}!**\n\n"
        "ب خێر هات بۆ پاشایێ بۆتێن تلێگرامێ یێن ستیکەران!\n"
        "• **ڤیدیۆ تا 15 چرکە ب بێ بەرانبەر (Free)**\n"
        "• **مۆدێن: ب تێکست، بێ تێکست و Animation Text**\n"
        "• **شاندنا ڕسمی/ڤیدیۆیێن نوو پاشی ستیکەری**\n\n"
        f"👑 {@YUSEEF_SURCHI} | 🛡️ {@Arthur3345}"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# Callback Query Handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "sticker_options":
        keyboard = [
            [InlineKeyboardButton("✍️ چێکرنا ستیکەری ب تێکست (With Text)", callback_data="make_with_text")],
            [InlineKeyboardButton("🖼️ چێکرنا ستیکەری بێ تێکست (No Text)", callback_data="make_no_text")],
            [InlineKeyboardButton("✨ تێکستێ جووڵاو (Animation Text)", callback_data="make_animated_text")],
            [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "⚙️ **مۆدێ چێکرنا ستیکەری هەڵبژێرە (تا 15 چرکە):**\n\n"
            "هەمی تشت ب بێ بەرانبەرە. چ تێکست، بێ تێکست یان ئەنیمیەشن ڤەبژێرە.\n\n"
            f"👑 {@YUSEEF_SURCHI} | 🛡️ {@Arthur3345}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    elif data == "make_with_text":
        keyboard = [[InlineKeyboardButton("🔙 ڤەگەر", callback_data="sticker_options")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "✍️ **مۆدا ب تێکست هاتە هەلبژارتن!**\n\n"
            "نوکە وێنە یان ڤیدیۆیا خۆ (تا 15 چرکە) بنێرە و تێکستێ خۆ ل سەر بنڤیسە.\n\n"
            f"👑 {@YUSEEF_SURCHI} | 🛡️ {@Arthur3345}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    elif data == "make_no_text":
        keyboard = [[InlineKeyboardButton("🔙 ڤەگەر", callback_data="sticker_options")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "🖼️ **مۆدا بێ تێکست هاتە هەلبژارتن!**\n\n"
            "نوکە وێنە یان ڤیدیۆیا خۆ (تا 15 چرکە) بێ تێکست بنێرە.\n\n"
            f"👑 {@YUSEEF_SURCHI} | 🛡️ {@Arthur3345}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif data == "make_animated_text":
        keyboard = [[InlineKeyboardButton("🔙 ڤەگەر", callback_data="sticker_options")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "✨ **مۆدا تێکستێ جووڵاو (Animation Text) هاتە ڤەکرن!**\n\n"
            "ڤیدیۆ یان GIF (تا 15 چرکە) بنێرە دا تێکستەکێ جووڵاو لسەر بهێتە چێکرن.\n\n"
            f"👑 {@YUSEEF_SURCHI} | 🛡️ {@Arthur3345}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    elif data == "filters_menu":
        keyboard = [
            [InlineKeyboardButton("🎨 1-140 فلتەرێن سەرەتایی", callback_data="filters_batch_1")],
            [InlineKeyboardButton("🔥 141-280 فلتەرێن سینەمایی", callback_data="filters_batch_2")],
            [InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "✨ **سیستەمێ 280 فلتەران:**\n\n"
            "هەلبژێرە و ب سەر مێدیایا خۆ یا ستیکەری دا زێدە بکە ب کیفیتەکا زۆر بلند.\n\n"
            f"👑 {@YUSEEF_SURCHI} | 🛡️ {@Arthur3345}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    elif data == "filters_batch_1":
        keyboard = [[InlineKeyboardButton("🔙 ڤەگەر بۆ فلتەران", callback_data="filters_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "⚙️ **فلتەرێن (1 هەتا 140) چالاکن!** مێدیایا خۆ بنێرە.\n\n"
            f"👑 {@YUSEEF_SURCHI} | 🛡️ {@Arthur3345}", 
            reply_markup=reply_markup, 
            parse_mode="Markdown"
        )
        
    elif data == "filters_batch_2":
        keyboard = [[InlineKeyboardButton("🔙 ڤەگەر بۆ فلتەران", callback_data="filters_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "⚙️ **فلتەرێن (141 هەتا 280) چالاکن!** مێدیایا خۆ بنێرە.\n\n"
            f"👑 {@YUSEEF_SURCHI} | 🛡️ {@Arthur3345}", 
            reply_markup=reply_markup, 
            parse_mode="Markdown"
        )

    elif data == "features_800":
        keyboard = [[InlineKeyboardButton("🔙 ڤەگەر بۆ سەرەکی", callback_data="back_home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "💎 **800 تایبەتمەندیێن بۆتی:**\n\n"
            "• ڤیدیۆ تا 15 چرکە ب بێ بەرانبەر\n"
            "• Animation Text و 280 فلتەر\n"
            "• شاندنا ڕسمی پشتی ستیکەری ب شێوەیەکێ خۆکار\n\n"
            f"👑 {@YUSEEF_SURCHI} | 🛡️ {@Arthur3345}",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    elif data == "back_home":
        await start(update, context)

# Media Processing Handler (Up to 15 seconds + Auto sending result photo/sticker after)
async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_name = message.from_user.first_name
    
    await message.reply_text(
        f"⏳ **بڕێز {user_name}**...\n"
        "مێدیایا تە (تا 15 چرکە) هاتە وەرگرتن. پڕۆسەکرنا ستیکەری و تێکستێ جووڵاو (Animation Text) دەستپێکر!\n"
        "🔹 *پشتی هندێ دێ ڕسما تە یا تێراپیساوی بێ بەرانبەر بۆ تە هێتە هناردن.*\n\n"
        f"👑 {@YUSEEF_SURCHI} | 🛡️ {@Arthur3345}",
        parse_mode="Markdown"
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(filters.PHOTO | filters.VIDEO | filters.ANIMATION, handle_media)

    logger.info("Bot is running with 15s support, Animation Text, and post-media results!")
    application.run_polling()

if __name__ == "__main__":
    main()
