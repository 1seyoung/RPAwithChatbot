import re


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CallbackContext
)


class FileHandler():
    def __init__(self, gm):
        self.gm =gm


        self.handler = ConversationHandler(
            entry_points = [CallbackQueryHandler(self.handle_start, pattern='^file$')]
        )

    def get_help(self):
        return [InlineKeyboardButton("문서 양식", callback_data= "file")]
    
    def get_handler(self) :
        #Telegram Manager 36~37 line
        return self.handler
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Display the gathered info and end the conversation."""
        context.user_data.clear()
        await update.message.reply_text("취소 되었습니다.")
        return ConversationHandler.END
    