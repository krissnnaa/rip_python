---------------RIP Version 2---------------
written by: Krishna prd Neupane

This program initially displays IP address
information of current device and then asks
to user to insert number of neighbors and 
their information.It includes following 
functions:
1) get_ip_address : to get ip address of
current computer

2) get_network_prefix : to get network 
prefix of provided ip address

3) make_message : to create a message to
send for update routing table

4) main : dispalys current ip address of devices
and asks for its neighbors information

5) send_table : to send updated message to the 
neighor

6) update_table: to update routing table based on 
received neighbor information


7) reveive_table : to receive sent message from neighbors

Following functions are used for extra part of the project:

8) update_live_router_table : to check whether neibhors are
active or not.

9) update_timer_table: used to calculate time of active
for each entries in a routing table.
