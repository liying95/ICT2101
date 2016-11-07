from scapy.all import *

def main():
	conf.checkIPaddr=False #to not check with the dest ip address, just check with mac address
	tap_interface='eth0' # to use eth0 inteterface
	src_mac = "" # used to store random mac address

	while True:

	 
		#DHCP Discovery(Broadcast)
		src_mac = RandMAC().replace(':','').decode('hex') #obtain random mac address and decode mac into hex(0x000)
		print RandMAC() #print mac address
		machineMAC = get_if_hwaddr('eth0') #get mac address of eth0

		ethernet = Ether(src=machineMAC, dst='ff:ff:ff:ff:ff:ff') # craft layer 2 with own com mac address and broadcast address
		ip = IP(src ='0.0.0.0',dst='255.255.255.255') # craft layer 3 with broadcast as dest address
		udp = UDP(sport=68,dport=67) # craft layer 4 with source and dest port(both are UDP port)
		bootp = BOOTP(giaddr = '0.0.0.0', ciaddr = '0.0.0.0', chaddr = src_mac, xid = RandInt(),flags = 0x8000) # craft layer 5 with random 			mac address and random xid value

		dhcp = DHCP(options=[("message-type","discover"),"end"]) # craft layer 5 a discover message
		packet = ethernet / ip / udp / bootp / dhcp # craft a packet with the layers (scapy message format rule)		
		offer = srp1(packet, iface=tap_interface) # srp1 = send and receive packet and store the received packet to offer variable

		#must print packet ip addr
		#print offer.display()
		print "HIHIHIHIHIHIHIHI"

		server_id = offer[DHCP].options[1][1]
	
		#DHCP Request(Broastcast) 
		ethernet1 = Ether(dst='ff:ff:ff:ff:ff:ff',src = machineMAC) 
		ip1 = IP(src='0.0.0.0', dst='255.255.255.255')
		udp1 = UDP(sport=68, dport=67)
		bootp1 = BOOTP(chaddr = src_mac, xid = offer[BOOTP].xid) 
		dhcp1 = DHCP(options=[("message-type","request"),("requested_addr",offer[BOOTP].yiaddr), ("requested_addr",offer		       			[BOOTP].yiaddr), ("server_id", server_id), "end"]) # obtain the yiaddr from the offer's 			layer 5	
		
		packet1 = ethernet1 / ip1 / udp1 / bootp1 / dhcp1
		ack = srp1(packet1)
		print ack.display()
		break

    
main()


