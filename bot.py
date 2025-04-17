from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import time as dtime
import logging
import random
from urllib.parse import quote
from collections import defaultdict

# --- BEÁLLÍTÁSOK --- #
TOKEN = '8182834378:AAH2pse6l2ur-A3dHdJDau0v6TwB2rkEfg8'
GROUP_CHAT_ID = -1002254559635
BASE_INVITE_LINK = 'https://t.me/labubuworldofficial?start='

# --- ÁLLAPOT TÁROLÁS --- #
referral_counts = defaultdict(int)

# --- NAPLÓZÁS --- #
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- VÁLASZ FUNKCIÓK --- #
def start(update, context):
    update.message.reply_text("🐇 Welcome to LABUBU World!\nType /info to get started!")

def welcome(update, context):
    for member in update.message.new_chat_members:
        ref = context.args[0] if context.args else None
        welcome_msg = f"👋 Welcome, {member.first_name}!\nWe’re building something legendary. Type /info to learn more!"
        if ref:
            welcome_msg += f"\n💥 Referred by: {ref}"
            referral_counts[ref] += 1
        context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_msg)

def info(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "🌐 LABUBU is a meme coin built on Solana.\n\n"
            "🔗 Website:\nhttps://labubu2025.github.io/labubu-token/landing-page.html\n\n"
            "💰 Buy now:\nhttps://jup.ag/swap?input=SOL&output=2ygXYFRC82ZjoEEWt5rfEHPVfEdKxWb747GjQSHgVzxi"
        )
    )

def buy(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="💸 Buy LABUBU here:\nhttps://jup.ag/swap?input=SOL&output=2ygXYFRC82ZjoEEWt5rfEHPVfEdKxWb747GjQSHgVzxi"
    )

def address(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📬 Contract address:\n2ygXYFRC82ZjoEEWt5rfEHPVfEdKxWb747GjQSHgVzxi"
    )

def web(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🌐 Website:\nhttps://labubu2025.github.io/labubu-token/landing-page.html"
    )

def chart(update, context):
    keyboard = [[
        InlineKeyboardButton("📊 View Chart", url="https://www.geckoterminal.com/solana/pools/HYnCMEXCxfmjMBtQmeXPWGxaD4VaZponBMfq4TFx6Kki")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="📊 LABUBU is live on GeckoTerminal!\nTrack price, volume & more:",
        reply_markup=reply_markup
    )

def shill(update, context):
    shill_templates = [
        "🐇 $LABU is the next billion-dollar meme coin. Don't miss the train! #Solana #LABUBU",
        "🚀 LABUBU just launched. We're going to the moon. Buy now: https://jup.ag/swap?input=SOL&output=2ygXYFRC82ZjoEEWt5rfEHPVfEdKxWb747GjQSHgVzxi",
        "👀 If you're not holding $LABU yet... you're late. But not too late. Join the revolution.",
        "💥 LABUBU is more than a meme. It's a mission. Tag 3 degens and let’s raid! 🐇💎",
        "🔥 You can't stop what's coming. $LABU is LIVE. Web: https://labubu2025.github.io/labubu-token/landing-page.html"
    ]
    reply = random.choice(shill_templates)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def refer(update, context):
    username = update.effective_user.username or f"user{update.effective_user.id}"
    encoded = quote(username)
    referral_link = f"{BASE_INVITE_LINK}{encoded}"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"🎯 Your personal referral link:\n{referral_link}\n\nInvite friends and grow the LABUBU community! 🐇"
    )

def leaderboard(update, context):
    if not referral_counts:
        context.bot.send_message(chat_id=update.effective_chat.id, text="📉 No referrals yet. Be the first to invite and earn fame!")
        return
    sorted_refs = sorted(referral_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    msg = "🏆 TOP REFERRERS:\n"
    for i, (user, count) in enumerate(sorted_refs, start=1):
        msg += f"{i}. {user} — {count} invites\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def tweet(update, context):
    tweets = [
        "💬 $LABU is the next $DOGE. You just don’t know it yet. #Solana #Crypto",
        "🐇 Just dropped a gem: $LABU. Early. Fast. Memetic.",
        "If $LABUBU hits $0.01, I'm buying a castle on the moon. 🌕",
        "When everyone else fades... LABUBU remains."
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"🧵 Suggested tweet:\n{random.choice(tweets)}"
    )

# --- AI STÍLUSÚ VÁLASZOK --- #
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
    elif "chart" in text:
        chart(update, context)

# --- AUTOMATA POSZT KÉPPEL + GOMBOK --- #
def post_hourly(context):
    keyboard = [[
        InlineKeyboardButton("💸 Buy Now", url="https://jup.ag/swap?input=SOL&output=2ygXYFRC82ZjoEEWt5rfEHPVfEdKxWb747GjQSHgVzxi"),
        InlineKeyboardButton("🌐 Website", url="https://labubu2025.github.io/labubu-token/landing-page.html")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open("buy_image.png", "rb") as image:
        context.bot.send_photo(
            chat_id=GROUP_CHAT_ID,
            photo=image,
            caption="🚀 Time to fly with $LABUBU\n\n🐇 The future of Solana memes starts here.",
            reply_markup=reply_markup
        )

# --- NAPI 3 PROMÓ POSZT --- #
def promo1(context):
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text="🚀 LABUBU is more than a meme — it’s a mission.\nDon’t miss out. Join early. Be legendary.")

def promo2(context):
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text="🔥 Airdrop is live!\n🐇 Claim yours:\nhttps://docs.google.com/forms/d/1nCT02jWL_1aOyePJcz2Tff9Bif-f6SsDH_ml3DjnrkE/edit")

def promo3(context):
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text="🌕 Building wealth together. LABUBU is the future.\nExplore:\nhttps://labubu2025.github.io/labubu-token/landing-page.html")

# --- MAIN --- #
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("buy", buy))
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("web", web))
    dp.add_handler(CommandHandler("chart", chart))
    dp.add_handler(CommandHandler("shill", shill))
    dp.add_handler(CommandHandler("refer", refer))
    dp.add_handler(CommandHandler("leaderboard", leaderboard))
    dp.add_handler(CommandHandler("tweet", tweet))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ai_reply))

    jq = updater.job_queue
    jq.run_repeating(post_hourly, interval=3600, first=10)
    jq.run_daily(promo1, time=dtime(10, 0))
    jq.run_daily(promo2, time=dtime(16, 0))
    jq.run_daily(promo3, time=dtime(22, 0))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
