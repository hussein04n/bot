import telebot
import openai
import re

# بيانات API
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "OPENAI_API_KEY"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# تخزين بيانات الاختبار لكل مستخدم
user_quizzes = {}

def parse_quiz(quiz_text):
    """
    تحليل الأسئلة من النص وإرجاع قائمة تحتوي على الأسئلة، الخيارات والإجابات الصحيحة.
    """
    quiz_data = []
    questions = quiz_text.strip().split("\n\n")  # تقسيم الأسئلة كل فقرة على حدة

    for question_block in questions:
        lines = question_block.split("\n")
        if len(lines) < 6:  # يجب أن يحتوي على 5 أسطر على الأقل (السؤال + 4 خيارات + الجواب)
            continue
        
        question_text = lines[0].strip()  # السؤال
        options = [line.split(") ")[1].strip() for line in lines[1:5]]  # استخراج الخيارات
        answer_line = lines[5]  # السطر الذي يحتوي على "Answer: X"
        
        match = re.search(r"Answer:\s*([A-D])", answer_line, re.IGNORECASE)  # البحث عن الإجابة
        if match:
            correct_option_letter = match.group(1).upper()
            correct_option_index = ord(correct_option_letter) - ord("A")  # تحويل A-D إلى رقم (0-3)
            
            quiz_data.append({
                "question": question_text,
                "options": options,
                "correct_option": correct_option_index
            })

    return quiz_data

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "مرحبًا! أرسل لي أسئلة Quiz بتنسيق معين وسأحولها إلى اختبار تفاعلي.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """
    استقبال نص اختبار وتحويله إلى أسئلة Quiz.
    """
    chat_id = message.chat.id
    username = message.from_user.username or "مستخدم مجهول"
    quiz_data = parse_quiz(message.text)

    if not quiz_data:
        bot.send_message(chat_id, "⚠️ لم يتم العثور على أسئلة بتنسيق صحيح، يرجى المحاولة مجددًا.")
        return

    user_quizzes[chat_id] = {
        "questions": quiz_data,
        "current_question": 0,
        "correct_answers": 0,
        "username": username
    }

    send_next_question(chat_id)

def send_next_question(chat_id):
    """
    إرسال السؤال التالي للمستخدم.
    """
    user_data = user_quizzes.get(chat_id, None)

    if user_data and user_data["current_question"] < len(user_data["questions"]):
        question_data = user_data["questions"][user_data["current_question"]]
        bot.send_poll(
            chat_id=chat_id,
            question=question_data["question"],
            options=question_data["options"],
            type="quiz",
            correct_option_id=question_data["correct_option"],
            is_anonymous=False
        )
    else:
        bot.send_message(chat_id, f"🎉 انتهى الاختبار! لقد أجبت على {user_data['correct_answers']} من {len(user_data['questions'])} أسئلة.")

@bot.poll_answer_handler()
def handle_poll_answer(poll_answer):
    """
    حساب إجابات المستخدم.
    """
    chat_id = poll_answer.user.id
    user_data = user_quizzes.get(chat_id, None)

    if user_data:
        current_question = user_data["current_question"]
        correct_option = user_data["questions"][current_question]["correct_option"]

        if poll_answer.option_ids[0] == correct_option:
            user_data["correct_answers"] += 1

        user_data["current_question"] += 1
        send_next_question(chat_id)

# تشغيل البوت
bot.polling()
