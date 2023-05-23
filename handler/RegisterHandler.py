from telegram import * 
from telegram.ext import *

from pygsheets import Spreadsheet

class registerHandler():
    def __init__(self):
        pass

    def get_help(self):
        #explain the role of handler

        return f"/register : register use using employee(student) ID"