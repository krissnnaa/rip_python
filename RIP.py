import time
import socket
import threading

neighbour_table = {}  # Neighbor table
routing_table = {}  # Routing table
live_router_table = {}
timer_table = {}

MAX_ROUTE_VALUE = 1000  # Cost of non-neighbor routers
INF = 999

SUBNET = '255.255.255.0'  # subnet mask for all ip address

UDP_SERVER_PORT = 5000  # port address for udp connection


def get_ip_address():
    """
    function to get ip address of current computer
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def get_network_prefix(network_ip, net_mask=SUBNET):
    """
    function to calculate network prefixes
    :param network_ip:
    :param net_mask:
    :return:
    """
    i = network_ip.split('.')  # it splits strings from .
    l = map(int, i)  # it maps the i string into integer
    m = map(int, net_mask.split('.'))  # it splits net mask with . and maps it into int

    b = map(lambda x, y: x & y, l, m)  # lambda is used to create function without name
    return '.'.join(map(str, b))  # join is used to join the elements of list with given char-
    # acter here '.' here map converts given b into string and join
    # joins with '.'


IP = get_ip_address()
SELF_NETWORK_PREFIX = get_network_prefix(IP)  # get current machine network prefix


def make_message(sep='|'):
    """
    this function is used to create message to be passed to the neighbor
    :return:
    """
    m = []
    for k, v in routing_table.iteritems():  # iterate over key,value pairs in routing table
        m.append(' '.join([k, str(v)]))  # joins key and value with space
    return sep.join(m)


def main():
    print 'The IP address of the current machine is : ', get_ip_address()
    i = raw_input("Input the number of neighbours : ")
    neighbour_count = int(i)

    i = neighbour_count
    while i != 0:
        a = raw_input('Input the IP of the neighbour : ')
        ip = str(a)
        a = raw_input('Input the cost for the neighbour : ')
        cost = int(a)

        neighbour_table[ip] = cost  # dictionary which holds ip as key
        prefix = get_network_prefix(ip)  # and cost as a value
        routing_table[prefix] = cost
        live_router_table[ip] = 0  # and cost as a value
        timer_table[prefix] = 0
        i -= 1


def send_table():
    """
    function to send update message to the neighbor
    :return:
    """
    while True:
        message = make_message()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for k, v in neighbour_table.iteritems():  # must have to send corresponding node IP
            sock.sendto(message, (k, UDP_SERVER_PORT))  # it sends msg to its neigh whose IP address if k

        time.sleep(1)


def update_table(new_table, neighbour_ip):
    """
    update the content of the table
    :param new_table:
    :param neighbour_ip:
    :return:
    """
    # Reset Live Router Entry to 0.
    live_router_table[neighbour_ip] = 0

    neighbour_prefix = get_network_prefix(neighbour_ip)
    neighbour_cost = routing_table[neighbour_prefix]

    if routing_table.get(neighbour_prefix) == MAX_ROUTE_VALUE:
        routing_table[neighbour_prefix] = neighbour_table[neighbour_ip]

    for k, v in new_table.iteritems():
        if k == SELF_NETWORK_PREFIX:
            continue

        # Reset Timer table to 0.
        if v != MAX_ROUTE_VALUE:
            timer_table[k] = 0

        # New updated by me
        new_cost = v + neighbour_cost
        if new_cost < routing_table.get(k, MAX_ROUTE_VALUE):
            routing_table[k] = new_cost

    print_route_table()


def receive_table():
    """
    function to receive the message from neighbors
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind((IP, UDP_SERVER_PORT))

    while True:
        recv_data, addr = sock.recvfrom(1024)

        m = map(lambda x: x.split(' '), recv_data.split('|'))
        new_table = {_[0]: int(_[1]) for _ in m}  # _[0] means variable m's 0th index
        update_table(new_table, addr[0])


def print_route_table():
    print "The Routing Table is :"
    print make_message(sep='\n')
    print
    print


# this is the extra part of the project for bonus
def update_live_router_table():
    """
    this function id used to check whether neighbors are active or not
    :return:
    """
    time.sleep(5)
    while True:
        for k, v in live_router_table.iteritems():
            v += 1

            if v > 20:
                k_prefix = get_network_prefix(k)
                routing_table[k_prefix] = MAX_ROUTE_VALUE

            live_router_table[k] = v
        time.sleep(1)


# this is also bonus part of the project
def update_timer_table():
    """
    this function updates timer of each entires of routing table
    :return:
    """
    time.sleep(10)
    expired_entries = []
    while True:
        for k, v in timer_table.iteritems():
            v += 1

            if v > 20:
                expired_entries.append(k)
                if k in routing_table:
                    for e in neighbour_table.keys():
                        e_p = get_network_prefix(e)
                        if e_p == k:
                            routing_table[k] = neighbour_table[e]
                            break
                    else:
                        del routing_table[k]
                        print 'Removed entry from the table %s' % k
            timer_table[k] = v

        [timer_table.pop(k, 0) for k in expired_entries]

        time.sleep(1)


if __name__ == '__main__':
    main()
    t = threading.Thread(target=send_table)
    t.daemon = True
    t.start()
    t1 = threading.Thread(target=receive_table)
    t1.daemon = True
    t1.start()
    t2 = threading.Thread(target=update_live_router_table)
    t2.daemon = True
    t2.start()
    # t3 = threading.Thread(target=update_timer_table)
    # t3.daemon = True
    # t3.start()

    while True:
        time.sleep(1)
