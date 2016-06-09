import yaml

class Parser (object):
    def __init__(self, path="../../config.yml"):
        with open(path, 'r') as stream:
            try:
                self.configuration = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                
    def get_load_balancer_configuration (self):
        return self.configuration["loadbalancer_conf"]
    
    def get_server_configuration (self):
        return self.configuration["api_server"]
    
    def get_distributed_db_configuration (self):
        return self.configuration["distributed_db"]
            