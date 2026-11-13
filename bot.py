import re
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")

BAD_WORDS = [
    "كلب", "حمار", "غبي", "احمق", "زبالة", "قذر", "وسخ",
    "لعين", "حقير", "واطي", "سافل", "منحط", "كذاب",
    "خنزير", "حيوان", "تافه", "اهبل", "مجنون",
    "انقلع", "اخرس", "قحبة", "شرموطة", "عاهرة",
    "زانية", "ديوث", "مخنث", "لوطي", "ساقط",
    "ابن حرام", "بنت حرام", "عرص",
    "fuck", "shit", "bitch", "asshole", "bastard", "whore", "slut"
]

def clean_text(text):
    text = text.lower()
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ة", "ه").replace("ى", "ي")
    text = re.sub(r'[^a-zا-ي0-9 ]', ' ', text)
    return text

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return
    if msg.photo:
        try: await msg.delete(); return
        except: pass
    if msg.video:
        try: await msg.delete(); return
        except: pass
    if msg.sticker:
        try: await msg.delete(); return
        except: pass
    if msg.animation:
        try: await msg.delete(); return
        except: pass

    text_to_check = msg.text or msg.caption or ""
    if text_to_check:
        text_clean = clean_text(text_to_check)
        for word in BAD_WORDS:
            if clean_text(word) in text_clean:
                try: await msg.delete()
                except: pass
                break

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, check_message))
    print("البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
