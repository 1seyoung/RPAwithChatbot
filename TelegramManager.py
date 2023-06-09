#import pyevsim
from pyevsim.behavior_model_executor import BehaviorModelExecutor

#import telegram
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

#custom handler
from handler.RegisterHandler import RegisterHandler
from handler.InfoHandler import InfoHandler
from handler.FileHandler import FileHandler


class TelegramManagerModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, engine, config, gm):
        super().__init__(inst_t, dest_t, mname, ename)

        self.gm = gm
        self.config = config



        self.application = Application.builder().token(self.config.telegram_token).build()



        #custom handler with conversation
        self.handlers = {
            RegisterHandler(self.gm),
            InfoHandler(self.gm),
            FileHandler(self.gm,self.config)

        }
        
        for handler in self.handlers:
            self.application.add_handler(handler.get_handler())

        self.application.add_handler(CommandHandler('start', self.start))


        #start the bot
        self.application.run_polling()


    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        keyboard = []
        
        for handler in self.handlers:
            keyboard.append(handler.get_help())

        reply_markup = InlineKeyboardMarkup(keyboard)
            
        await update.message.reply_text('사용할 메뉴를 선택해주세요', reply_markup=reply_markup)
       
