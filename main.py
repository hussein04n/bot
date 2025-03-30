import telebot
import requests
from io import BytesIO
from PIL import Image

# استبدل هذا بالتوكن الخاص بك
TOKEN = "1475041982:AAFx_SAgQaHxuyls4dNvE2i_JoMyX4m2ivM"
bot = telebot.TeleBot(TOKEN)

# استبدل هذا برابط API لتحويل الصور إلى أنمي
ANIME_API_URL = "https://api.deepai.org/api/toonify"
API_KEY = "958b8a9d-60b2-41a6-b888-51e68d3c057f"

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
    
    response = requests.get(file_url)
    if response.status_code == 200:
        img = BytesIO(response.content)

        # إرسال الصورة إلى API
        response = requests.post(
            ANIME_API_URL,
            files={'image': img},
            headers={'api-key': API_KEY}
        )

        if response.status_code == 200:
            result_url = response.json().get('output_url')
            bot.send_photo(message.chat.id, result_url)
        else:
            bot.reply_to(message, "حدث خطأ أثناء تحويل الصورة.")

bot.polling()
