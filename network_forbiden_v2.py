import os
import sys
from log import *
import requests
import socket 

def get_ip():
	hostname = socket.gethostname()
	ip = socket.gethostbyname(hostname)
	return ip

def send_msg(title, message, to_party=20):
	logger().info('send message:%s:%s', title, message)
        send_msg_url = 'http://op-01.gzproduction.com:9527/api/msg/send'
        payload = {'title': title, 'message': message, 'to_party': to_party}
        ret = requests.get(send_msg_url, params=payload)
	logger().info('ret %s', ret)
        return '0' == ret.json()['code']

def get_network_interface():
	eno_list = []
	cmd = "/sbin/ifconfig | awk '{print $1}' | grep en"
	en = os.popen(cmd).read()
	if not en:
		logger().info('eno list %s', en)
		return None
	for i in en.strip().split('\n'):
		eno = i
		eno_list.append(eno)
	return eno_list

def bandwidth_check(eno_list):
	ip = get_ip()
	problem_num = 0
	if not eno_list:
		logger().info('eno_list[%s] is empty', eno_list)
		sys.exit(1)
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
				logger().error('send alert failed')
				sys.exit(1)
	logger().info('bandwidth problem:%d', problem_num)

if __name__ == "__main__":
	log_init('info', '/opt/network_check/network.txt', quiet = False)
	eno_list = get_network_interface()	
	logger().info('eno_list %s', eno_list)
	bandwidth_check(eno_list)
