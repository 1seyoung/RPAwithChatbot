#import pyevsim
from pyevsim.behavior_model_executor import BehaviorModelExecutor

#import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

#custom handler
from handler.RegisterHandler import RegisterHandler
from handler.InfoHandler import InfoHandler


class TelegramManagerModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, engine, config, gm):
        super().__init__(inst_t, dest_t, mname, ename)

        self.gm = gm
        self.config = config



        self.application = Application.builder().token(self.config.telegram_token).build()



        #custom handler with conversation
        self.handlers = {
            RegisterHandler(self.gm),
            InfoHandler(self.gm)

        }
        
        for handler in self.handlers:
            self.application.add_handler(handler.get_handler())

        self.application.add_handler(CommandHandler('start', self.start))


        #start the bot
        self.application.run_polling()


    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        resp = ""
        
        for handler in self.handlers:
            resp += handler.get_help()
            resp += "\n"
        await update.message.reply_text(resp)   
       
