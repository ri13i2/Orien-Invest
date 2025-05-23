from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 봇 토큰 입력
TOKEN = '8135523315:AAF4UQ9NuSKIkhWj7Hb7nXKv0QGyqWpiWQg'

# 관리자 ID 입력
ADMIN_ID = 8069493255  # 실제 관리자 ID로 변경

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "안녕하세요 오리엔 인베스트 상담 봇 입니다.\n"
        "상담원하시는 내용 및 정보기재 부탁드리면\n"
        "순차적으로 신속히 확인후 상담 도와드리겠습니다."
    )
    await update.message.reply_text(welcome_message)

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.message.from_user.full_name
    user_id = update.message.from_user.id

    # 관리자에게 메시지 전달
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"새로운 상담 요청이 있습니다:\n\n"
             f"보낸 사람: {user_name} (ID: {user_id})\n"
             f"메시지 내용: {user_message}"
    )

    # 사용자에게 확인 메시지 전송
    await update.message.reply_text("귀하의 메시지가 접수되었습니다. 곧 상담원이 연락드리겠습니다.")

async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # 핸들러 등록
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_to_admin))

    # 봇 실행
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
