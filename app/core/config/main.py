from dotenv import dotenv_values, find_dotenv
from python_json_config import ConfigBuilder
from app.definitions import ROOT_DIR
    
class Config: 
    def __init__(self) -> None:
        self.env = dotenv_values(find_dotenv())
        self.app_builder = ConfigBuilder()
        self.app = self.app_builder.parse_config(f"{ROOT_DIR}/config.json")

config = Config()