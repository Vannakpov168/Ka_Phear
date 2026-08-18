import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ជំនួស Bot Token របស់អ្នកពី BotFather នៅទីនេះ
BOT_TOKEN = "8047614722:AAHaV8uANS1U0QDRH0MWZmLTcQX327BZlEo"

# បញ្ជី Extension File ដែលសង្ស័យថាជាមេរោគ និងត្រូវលុបចោលភ្លាមៗ
DANGEROUS_EXTENSIONS = ['.exe', '.bat', '.scr', '.vbs', '.cmd', '.msi', '.ps1', '.jar', '.pif']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def scan_and_delete_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.document:
        return

    file_name = message.document.file_name
    if not file_name:
        return

    # ទាញយក Extension នៃ File (ឧទាហរណ៍៖ .exe, .pdf)
    _, file_extension = os.path.splitext(file_name.lower())
    sender_name = message.from_user.first_name if message.from_user else "Someone"

    # ឆែកមើលថា តើ File នោះស្ថិតក្នុងបញ្ជី Extension គ្រោះថ្នាក់ដែរឬទេ?
    if file_extension in DANGEROUS_EXTENSIONS:
        try:
            # ១. លុបសារ/File នោះចេញពី Chat/Group ភ្លាមៗ
            await message.delete()

            # ២. ផ្ញើសារប្រកាសអាសន្នប្រាប់ក្នុង Group
            warning_msg = f"⚠️ **ប្រព័ន្ធសុវត្ថិភាព:** បានលុប File `{file_name}` ដែលផ្ញើដោយ {sender_name} រួចរាល់! (មូលហេតុ៖ ជាប្រភេទ File គ្រោះថ្នាក់ `{file_extension}`)"
            await context.bot.send_message(chat_id=message.chat_id, text=warning_msg, parse_mode='Markdown')
            
            print(f"[Deleted Security Threat] {file_name} from {sender_name}")

        except Exception as e:
            print(f"មិនអាចលុប File បានទេ (ត្រូវការសិទ្ធិ Admin): {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ចាប់យកគ្រប់ File (Documents) ដែលផ្ញើចូល Chat/Group
    app.add_handler(MessageHandler(filters.Document.ALL, scan_and_delete_file))

    print("Auto-Delete Virus File Bot កំពុងដំណើរការ...")
    app.run_polling()