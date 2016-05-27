import yaml

class Parser (object):
    def __init__(self, path="../../config.yml"):
        with open(path, 'r') as stream:
            try:
                self.configuration = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                
    def getLoadbalancerConfiguration (self):
        return self.configuration["loadbalancer_conf"]
    
    def getServerConfiguration (self):
        return self.configuration["api_server"]
    
    def getDistributedDBConfiguration (self):
        return self.configuration["distributed_db"]
                