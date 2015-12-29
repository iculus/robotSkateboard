import setupNetwork as net

host = 'localhost';port = 9999;size = 100;idtag ='ntwrkMngr'
inOnline,network = net.goOnline(host,port,size,idtag)

while True:
	data = network.recv(size)
	if data:
		print data
s.close()
