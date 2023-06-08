import pygsheets
from config import confingManger

import json

class gsheetManagerModel():
    def __init__(self) :

        #self.config = config
        self.config = confingManger('instance/config.json')
        self.gc = pygsheets.authorize(service_file = self.config.gsheet_api)
        self.sh = self.gc.open(self.config.gsheet_name)
        
        self.wkList = self.get_all_worksheet_names()

        print(self.wkList)

        self.Cwks =self.sh.worksheet('title','info_structure')

    
    def get_all_worksheet_names(self):
        worksheets = self.sh.worksheets()
        worksheet_names = [ws.title for ws in worksheets]
        return worksheet_names
    


gc = gsheetManagerModel()


#print(gc.worksheet_to_json(gc.Cwks))