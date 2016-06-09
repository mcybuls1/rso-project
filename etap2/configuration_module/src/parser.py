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

if __name__ == '__main__':
    test()
