import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7642185587:AAHypPZPZEQ8B7cgkqzl1SPuiPmThKjespo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ I'm alive forever and free!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    print("🚀 Bot started...")
    app.run_polling(stop_signals=None)  # no stop signals = keeps forever
