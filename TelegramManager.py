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
from handler.RegisterHandler import registerHandler
import sys,os
import signal

class TelegramManagerModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, engine, config, gm):
        super().__init__(inst_t, dest_t, mname, ename)

        self.gm = gm
        self.config = config


        #self.updater = Updater(self.config.telegram_token)
        self.application = Application.builder().token("self.config.telegram_token").build()
        #dispatcher = self.updater.dispatcher


        #custom handler with conversation
        self.handlers = {
            registerHandler()

        }
        
        for handler in self.handlers:
            self.application.add_handler(handler.get_handler())


        #dispatcher.add_handler
        # start handler : The role of the bot at the beginning is to provied guide & assistance

        self.application.add_handler(CommandHandler('start', self.start))


        #start the bot
        self.application.run_polling()


    def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        resp = ""
        
        for handler in self.handlers:
            resp += handler.get_help()
            resp += "\n"
        update.message.reply_text(resp)   
       
