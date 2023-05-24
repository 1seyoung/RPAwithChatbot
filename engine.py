#import pyevsim 
from pyevsim.system_simulator import SystemSimulator
from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.definition import *

#import config
from config import confingManger

#import googlesheet
from GsheetManager import gsheetManagerModel

#import model
from TelegramManager import TelegramManagerModel

class systemEngine():
    def __init__(self) :
        
        #config -> data type : json
        self.config = confingManger('instance/config.json')
        self.gm = gsheetManagerModel(self.config)

        #register simulation engine -> (engine_name, mode, engine operation_period)
        self.ss = SystemSimulator()
        ename = "mainEngine"

        self.engine = self.ss.register_engine(ename,"REAL_TIME",1)

        #create engine input port
        self.ss.get_engine(ename).insert_input_port("start")

        #define DEVS model (class)
        Tmanager = TelegramManagerModel(0, Infinite,"telegram_manager",ename, self.engine, self.config, self.gm)
    
    def start(self):
        self.engine.simulate()


if __name__ == "__main__":
    pysim = systemEngine()
    pysim.start()