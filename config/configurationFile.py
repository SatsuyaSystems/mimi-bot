import yaml

class ConfigurationFile:
    def __init__(self, path : str ) -> 'ConfigurationFile':
        self.path = path
        self.data = None

        self.load()

    def load(self) -> dict:
        with open(self.path, 'r', encoding='utf-8') as config_file:
            self.data = yaml.safe_load(config_file)
            return self.data

    def save(self) -> None:
        with open(self.path, 'w', encoding='utf-8') as config_file:
            yaml.safe_dump(self.data, config_file)