
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


class registerHandler():
    def __init__(self):

        self.handler = ConversationHandler()

    def get_help(self):
        #explain the role of handler

        return f"/register : register use using employee(student) ID"
    
    def get_handler(self) :
        #Telegram Manager 36~37 line
        return self.handler