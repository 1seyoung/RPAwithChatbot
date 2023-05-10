#import pyevsim
from pyevsim.behavior_model_executor import BehaviorModelExecutor

#import telegram
from telegram import * 
from telegram.ext import *

class TelegramManagerModel(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, mname, ename, engine, config):
        super().__init__(inst_t, dest_t, mname, ename)

        
        
        telegram_token = config.telegram_token

        print(telegram_token)