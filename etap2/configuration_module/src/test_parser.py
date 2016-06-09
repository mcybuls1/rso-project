from parser import Parser

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