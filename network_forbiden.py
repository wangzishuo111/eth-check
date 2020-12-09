import os
import sys
from log import *
import requests
import socket 

def get_ip():
	hostname = socket.gethostname()
	ip = socket.gethostbyname(hostname)
	return ip

def send_msg(title, message):
	logger().info('send message:%s:%s', title, message)
        send_msg_url = 'http://op-01.gzproduction.com:9527/api/msg/send'
        payload = {'title': title, 'message': message}
        ret = requests.get(send_msg_url, params=payload)
        return '0' == ret.json()['code']

def get_network_interface():
	eno_list = []
	cmd = "ifconfig | awk '{print $1}' | grep en"
	en = os.popen(cmd).read()
	for i in en.strip().split('\n'):
		eno = i
		eno_list.append(eno)
	return eno_list

def bandwidth_check(eno_list):
	ip = get_ip()
	problem_num = 0
	for eth in eno_list:
		cmd = "sudo ethtool %s | awk '{print $2}'" % eth
		bandwidth = os.popen(cmd).read().strip().split('\n')
		logger().debug('%s\'s bandwidth %s', eth, bandwidth)
		if '1000Mb/s' not in bandwidth: 
			problem_num += 1
			cmd2 = 'sudo ip link set %s down' % eth
			logger().info('stop the interface %s, cmd:%s', eth, cmd2)
			ret = os.system(cmd2)
			if 0 == ret:
				logger().info('success to set %s down', eth)
			else:
				logger().info('fail to set %s down', eth)
				
			ret = send_msg('bandwidth', '%s network-interface %s is down' % (ip, eth))
			if not ret:
				logger().error('log not effective')
				sys.exit(1)
	logger().info('bandwidth problem:%d', problem_num)		
			
		
if __name__ == "__main__":
#	print get_eno()
	log_init('info', '/opt/network_check/network.txt', quiet = False)
	eno_list = get_network_interface()	
	bandwidth_check(eno_list)
