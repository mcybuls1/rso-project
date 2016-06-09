import yaml

class ConfigurationParser (object):
    def __init__(self, path="../../config.yml"):
        with open(path, 'r') as stream:
            try:
                self.configuration = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                
    def get_loadbalancer_configuration (self):
        return self.configuration["load_balancer"]
    
    def get_server_configuration (self):
        return self.configuration["server"]
    
    def get_database_configuration (self):
        return self.configuration["data_base"]
    
    def get_membership_protocol_configuration (self):
        return self.configuration["membership_protocol"]
    
    def get_loadbalancer_link_name(self):
        return self.get_loadbalancer_configuration()["link"]
    
    def get_loadbalancers_count(self):
        return self.get_loadbalancer_configuration()["nodes_info"]["count"]
    
    def get_loadbalancers_param(self):
        return self.get_loadbalancer_configuration()["nodes_info"]["nodes_param"]
    
    def get_databases_count(self):
        return self.get_database_configuration()["nodes_info"]["count"]
    
    def get_databases_param(self):
        return self.get_database_configuration()["nodes_info"]["nodes_param"]
        
    def get_servers_count(self):
        return self.get_server_configuration()["nodes_info"]["count"]
        
    def get_servers_param(self):
        return self.get_server_configuration()["nodes_info"]["nodes_param"]
    
    def get_db_host(self):
        return self.get_server_configuration()["db_host"]
    
    def get_db_port(self):
        return self.get_server_configuration()["db_port"]
    
    def get_db_db(self):
        return self.get_server_configuration()["db_db"]
    
    
    
