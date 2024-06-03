import yaml
import os


class Config:
    def __init__(self, config_file='config.yaml'):
        current_script_path = os.path.dirname(os.path.abspath(__file__))
        config_file = current_script_path + "\\config.yaml"
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_database_config(self):
        return self.config['database']
