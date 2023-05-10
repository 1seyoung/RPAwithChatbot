
from config import confingManger



# ConfigManager 객체 생성
config_manager = confingManger('instance/config.json')

# Config 값 가져오기
telegram_token = config_manager.telegram_token

print(telegram_token)