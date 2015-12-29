import socket

def goOnline(host,port,size,name):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	online = False
	try:
		s.connect((host,port))
		s.send(name)	
		online = True
	except:
		online = False
	return online,s
	

if __name__ == "__main__":
	goOnline("192.168.7.1",9999,100,'tester')
