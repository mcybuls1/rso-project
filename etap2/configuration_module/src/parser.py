import yaml

class Parser (object):
    def __init__(self, path="../../config.yml"):
        with open(path, 'r') as stream:
            try:
                self.configuration = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                
    def get_load_balancer_configuration (self):
        return self.configuration["load_balancer"]
    
    def get_server_configuration (self):
        return self.configuration["server"]
    
    def get_distributed_db_configuration (self):
        return self.configuration["data_base"]
    
    def get_loadbalancer_link_name(self):
        return self.get_load_balancer_configuration()["link"]
    
    def get_loadbalancers_count(self):
        return self.get_load_balancer_configuration()["nodes_info"]["count"]
    
    def get_db_host(self):
        return self.get_server_configuration()["db_host"]
    
    def get_db_port(self):
        return self.get_server_configuration()["db_port"]
    
    def get_db_db(self):
        return self.get_server_configuration()["db_db"]
    
