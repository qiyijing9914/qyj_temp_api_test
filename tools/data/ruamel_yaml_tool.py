from ruamel import yaml

class YamlLoader:

    def __init__(self, file):
        self.file = file

    def file_load(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            data = f.read()
        return yaml.load(data, Loader=yaml.RoundTripLoader)

    def file_dump(self, data):
        with  open(self.file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, Dumper=yaml.RoundTripDumper,default_flow_style=False,encoding='utf-8',allow_unicode=True)
