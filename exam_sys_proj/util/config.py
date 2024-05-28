import yaml

class Config:
    def __init__(self, config_file='config.yaml'):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_database_config(self):
        return self.config['database']
