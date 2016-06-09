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
    
def test():
    parser = Parser("test_config.yml")
    get_db_host_test(parser)
    get_db_port_test(parser)
    get_db_db_test(parser)
    get_loadbalancer_link_name_test(parser)
    get_loadbalancers_count_test(parser)

def get_db_host_test(parser):
    if not '192.168.56.2' == parser.get_db_host() :
        print ("DB host should be returned correctly")
        return -1
    print ("OK")
    return 0

def get_db_port_test(parser):
    if not 6379 == parser.get_db_port() :
        print ("DB port should be returned correctly")
        return -1
    print ("OK")
    return 0

def get_db_db_test(parser):
    if not 0 == parser.get_db_db() :
        print ("DB db should be returned correctly")
        return -1
    print ("OK")
    return 0

def get_loadbalancer_link_name_test(parser):
    if not 'loadbalancer' == parser.get_loadbalancer_link_name() :
        print ("Loadbalancer link name should be returned correctly")
        return -1
    print ("OK")
    return 0

def get_loadbalancers_count_test(parser):
    if not 3 == parser.get_loadbalancers_count() :
        print ("Loadbalancers count should be returned correctly")
        return -1
    print ("OK")
    return 0

if __name__ == '__main__':
    test()
