import os
import sys

def get_eno():
	eno_list = []
	cmd = "ifconfig | awk '{print $1}' | grep en"
	en = os.popen(cmd).read()
	for i in en.strip().split('\n'):
		eno = i
		eno_list.append(eno)
	return eno_list
def get_bdwh(eno_list):
	for i in eno_list:
		cmd = "sudo ethtool %s | awk '{print $2}'" %i
		bandwidth = os.popen(cmd).read().strip().split('\n')
		if '1000Mb/s' not in bandwidth: 
			print i 
			print bandwidth
			
		
if __name__ == "__main__":
	eno_list = get_eno()	
	get_bdwh(eno_list)
