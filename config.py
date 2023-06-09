import json

class confingManger:
    def __init__(self, filemane):
        with open(filemane, 'r') as f:
            config_dict = json.load(f)

        #telegram bot token
        self.telegram_token = config_dict["telegram"]["token"]

        #pygsheets
        self.gsheet_api = config_dict["googlesheet"]["api_key"]
        self.gsheet_name = config_dict["googlesheet"]["sheetname"]

        #file_foder
        self.doc_path = config_dict["path"]["doc_folder"]