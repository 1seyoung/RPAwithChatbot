from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler,CallbackQueryHandler, CallbackContext

from pygsheets import Spreadsheet

class registerHandler():
    def __init__(self):
        pass

    def get_help(self):
        #explain the role of handler

        return f"/register : register use using employee(student) ID"
    
    def get_handler(self) -> Dispatcher:
        return self.handler