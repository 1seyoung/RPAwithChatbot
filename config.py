import json

class confingManger:
    def __init__(self, filemane):
        with open(filemane, 'r') as f:
            config_dict = json.load(f)

        self.telegram_token = config_dict["telegram"]["token"]