#import pyevsim
from pyevsim.behavior_model_executor import BehaviorModelExecutor

#import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

#custom handler
from handler.RegisterHandler import registerHandler
import sys,os
import signal

class TelegramManagerModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, engine, config, gm):
        super().__init__(inst_t, dest_t, mname, ename)

        self.gm = gm
        self.config = config

        signal.signal(signal.SIGINT,  self.signal_handler)
        signal.signal(signal.SIGABRT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)



        self.updater = Updater(self.config.telegram_token)
        dispatcher = self.updater.dispatcher


        #custom handler with conversation
        self.handlers = {
            registerHandler()

        }
        
        for handler in self.handlers:
            dispatcher.add_handler(handler.get_handler())


        #dispatcher.add_handler
        # start handler : The role of the bot at the beginning is to provied guide & assistance

        dispatcher.add_handler(CommandHandler('start', self.start))


        #start the bot
        self.updater.start_polling()


    def start(self, update: Update, context: CallbackContext) -> None:
        
        resp = ""
        
        for handler in self.handlers:
            resp += handler.get_help()
            resp += "\n"
        update.message.reply_text(resp)   
       
    def signal_handler(self, sig, frame):
        print("Terminating Monitoring System")
		
        if not self.is_terminating:
            self.is_terminating = True
            self.updater.stop()
		
        sys.exit(0)