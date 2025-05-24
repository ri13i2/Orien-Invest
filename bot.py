from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 봇 토큰과 관리자 ID를 입력하세요
TOKEN = '8135523315:AAF4UQ9NuSKIkhWj7Hb7nXKv0QGyqWpiWQg'
ADMIN_ID = 8069493255  # 실제 관리자 ID로 변경하세요

def start(update: Update, context: CallbackContext):
    welcome_message = (
        "안녕하세요 오리엔 인베스트 상담 봇 입니다.\n"
        "상담원하시는 내용 및 정보기재 부탁드리면\n"
        "순차적으로 신속히 확인후 상담 도와드리겠습니다."
    )
    update.message.reply_text(welcome_message)

def forward_to_admin(update: Update, context: CallbackContext):
    user = update.message.from_user
    message = update.message

    # 텍스트 메시지 처리
    if message.text:
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"새로운 상담 요청:\n\n"
                 f"보낸 사람: {user.full_name} (ID: {user.id})\n"
                 f"메시지:\n{message.text}"
        )
        message.reply_text("귀하의 메시지가 접수되었습니다. 곧 상담원이 연락드리겠습니다.")

    # 사진 처리
    elif message.photo:
        photo_file = message.photo[-1].get_file()
        photo_file.download('user_photo.jpg')
        context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=open('user_photo.jpg', 'rb'),
            caption=f"보낸 사람: {user.full_name} (ID: {user.id})"
        )
        message.reply_text("사진이 접수되었습니다. 곧 상담원이 확인하겠습니다.")

    # 문서 처리
    elif message.document:
        document_file = message.document.get_file()
        document_file.download(message.document.file_name)
        context.bot.send_document(
            chat_id=ADMIN_ID,
            document=open(message.document.file_name, 'rb'),
            caption=f"보낸 사람: {user.full_name} (ID: {user.id})"
        )
        message.reply_text("파일이 접수되었습니다. 곧 상담원이 확인하겠습니다.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, forward_to_admin))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
