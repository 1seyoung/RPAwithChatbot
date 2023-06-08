import pygsheets
from config import confingManger

import json
import pandas as pd

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', filename='app.log', filemode='a')


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
    

    def get_admin_info(self):
        wks = self.sh.worksheet('title','user')
        df = wks.get_as_df()

        admin_info = df[df['Permission'] == 'Admin'].values.tolist()

        return admin_info
    
    def update_table(self, wks_name, data):

        wks = self.sh.worksheet('title', wks_name)
        wks.append_table(data)

        logging.info(f'Appended new data to worksheet: {data} in "{wks_name}" worksheet')


    def get_df_to_list(self, wks_name,type):
        wks = self.sh.worksheet('title', wks_name)
        df = wks.get_as_df()

        if type == "df" :
            return df
        
        elif type == "list" :
            df_list = []
            for index, row in df.iterrows():
                row_list = row.values.tolist()
                df_list.append(row_list)

            return df_list

