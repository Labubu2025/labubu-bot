from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, time

# --- BEÁLLÍTÁSOK --- #
TOKEN = '8182834378:AAH2pse6l2ur-A3dHdJDau0v6TwB2rkEfg8'
GROUP_CHAT_ID = -1002254559635

# --- NAPLÓZÁS --- #
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- VÁLASZ FUNKCIÓK --- #
def start(update, context):
    update.message.reply_text("🐇 Welcome to LABUBU World!\nType /info to get started!")

def welcome(update, context):
    for member in update.message.new_chat_members:
        context.bot.send_message(chat_id=update.effective_chat.id,
            text=f"👋 Welcome, {member.first_name}!\nWe’re building something legendary. Type /info to learn more!")

def info(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
        text="🌐 LABUBU is a meme coin built on Solana.\n\n🔗 Website:\nhttps://labubu2025.github.io/labubu-token/landing-page.html\n\n💰 Buy now:\nhttps://jup.ag/swap?input=SOL&output=2ygXYFRC82ZjoEEWt5rfEHPVfEdKxWb747GjQSHgVzxi")

def buy(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
        text="💸 Buy LABUBU here:\nhttps://jup.ag/swap?input=SOL&output=2ygXYFRC82ZjoEEWt5rfEHPVfEdKxWb747GjQSHgVzxi")

def address(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
        text="📬 Contract address:\n2ygXYFRC82ZjoEEWt5rfEHPVfEdKxWb747GjQSHgVzxi")

def web(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
        text="🌐 Website:\nhttps://labubu2025.github.io/labubu-token/landing-page.html")

# --- AI JELLEGŰ VÁLASZOK ÜZENETRE --- #
def ai_reply(update, context):
    text = update.message.text.lower()
    if "how to buy" in text or "buy" in text:
        buy(update, context)
    elif "airdrop" in text:
        context.bot.send_message(chat_id=update.effective_chat.id, text="🎁 Airdrop link:\nhttps://docs.google.com/forms/d/1nCT02jWL_1aOyePJcz2Tff9Bif-f6SsDH_ml3DjnrkE/edit")
    elif "website" in text or "web" in text:
        web(update, context)
    elif "address" in text:
        address(update, context)

# --- ÓRÁNKÉNTI BUY POSZT KÉPPEL + GOMBOKKAL --- #
def post_hourly(context):
    keyboard = [[
        InlineKeyboardButton("💸 Buy Now", url="https://jup.ag/swap?input=SOL&output=2ygXYFRC82ZjoEEWt5rfEHPVfEdKxWb747GjQSHgVzxi"),
        InlineKeyboardButton("🌐 Website", url="https://labubu2025.github.io/labubu-token/landing-page.html")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open("buy_image.png", "rb") as image:
        context.bot.send_photo(chat_id=GROUP_CHAT_ID, photo=image,
            caption="🚀 Time to fly with $LABUBU\n\n🐇 The future of Solana memes starts here.",
            reply_markup=reply_markup)

# --- NAPI 3 PROMÓ POSZT --- #
def promo1(context):
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text="🚀 LABUBU is more than a meme — it’s a mission.\nDon’t miss out. Join early. Be legendary.")

def promo2(context):
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text="💥 Airdrop is live!\n🐇 Claim yours before it’s too late:\nhttps://docs.google.com/forms/d/1nCT02jWL_1aOyePJcz2Tff9Bif-f6SsDH_ml3DjnrkE/edit")

def promo3(context):
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text="🌕 Building wealth together. LABUBU is the future.\nVisit us:\nhttps://labubu2025.github.io/labubu-token/landing-page.html")

# --- MAIN --- #
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("buy", buy))
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("web", web))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ai_reply))

    jq = updater.job_queue
    jq.run_repeating(post_hourly, interval=3600, first=10)
    jq.run_daily(promo1, time=time.strptime("10:00", "%H:%M"))
    jq.run_daily(promo2, time=time.strptime("16:00", "%H:%M"))
    jq.run_daily(promo3, time=time.strptime("22:00", "%H:%M"))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
