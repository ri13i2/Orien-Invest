from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 발급받은 토큰과 관리자 ID 입력
TOKEN = "여기에_토큰_입력"
ADMIN_ID = 123456789  # 본인의 텔레그램 ID로 바꾸세요

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "안녕하세요 오리엔 인베스트 상담 봇 입니다.\n"
        "상담원하시는 내용 및 정보기재 부탁드리면\n"
        "순차적으로 신속히 확인후 상담 도와드리겠습니다."
    )

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"새로운 상담 요청:\n\n"
             f"보낸 사람: {user.full_name} (ID: {user.id})\n"
             f"메시지:\n{update.message.text}"
    )
    await update.message.reply_text("귀하의 메시지가 접수되었습니다. 곧 상담원이 연락드리겠습니다.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))

    # 🚫 asyncio.run() 사용하지 않음
    app.run_polling()

if __name__ == "__main__":
    main()
