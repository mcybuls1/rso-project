import yaml

class Parser (object):
    def __init__(self, path="../../config.yml"):
        with open(path, 'r') as stream:
            try:
                print(yaml.load(stream))
            except yaml.YAMLError as exc:
                print(exc)
                
if __name__ == '__main__':
    Parser()
    path = "../../config.yml"
    Parser(path)
