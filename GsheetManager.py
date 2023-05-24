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
    
    def update_row(self):
        pass

    def worksheet_to_json(self, worksheet):
        # Get all values from the worksheet
        values = worksheet.get_all_values()

        # Assume the first row is the header
        headers = values[0]
        data_rows = values[1:]

        # Convert to a list of dictionaries
        data_dicts = [dict(zip(headers, row)) for row in data_rows]

        # Convert to JSON
        json_data = json.dumps(data_dicts, indent=4)

        return json_data    

gc = gsheetManagerModel()


print(gc.worksheet_to_json(gc.Cwks))