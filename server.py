import twisted.internet.protocol
import twisted.internet.reactor

connections = []
networkMap = {}

class EchoProtocol(twisted.internet.protocol.Protocol):
	def connectionMade(self):
		self.peer = self.transport.getPeer()
	def dataReceived(self, data):
		if self not in connections:
			connections.append(self)
			
			#make network map
			def mapNet(name,words):
				if data == name:
					networkMap[name] = self
					self.transport.write(words)
					if 'ntwrkMngr' in networkMap.keys(): 
							networkMap['ntwrkMngr'].transport.write('connected : ')
							networkMap['ntwrkMngr'].transport.write(str(networkMap.keys()))
		
			mapNet('3DC','\nyou are 3DC\n')
			mapNet('ntwrkMngr','\nyou are network manager\n')
			mapNet('barGraph','\nyou are bar graph\n')
			mapNet('imu','\nyou are imu\n')
			mapNet('dispIMU','\nyou are imu display\n')
			mapNet('lidar','\nyou are lidar\n')
			mapNet('radar','\nyou are radar\n')

		#send data to appropriate locations
		if '3DC' in networkMap.keys():
			if self == networkMap['3DC']:
				if 'barGraph' in networkMap.keys():
					networkMap['barGraph'].transport.write(data)
		if 'imu' in networkMap.keys():
			if self == networkMap['imu']:
				if 'dispIMU' in networkMap.keys():
					networkMap['dispIMU'].transport.write(data)
		if 'lidar' in networkMap.keys():
			if self == networkMap['lidar']:
				if 'radar' in networkMap.keys():
					networkMap['radar'].transport.write(data)


	def connectionLost(self,reason):
		for key in networkMap.keys():
			if networkMap[key] == self:
				del networkMap[key]
		if 'ntwrkMngr' in networkMap.keys(): 
				networkMap['ntwrkMngr'].transport.write('connected : ')
				networkMap['ntwrkMngr'].transport.write(str(networkMap.keys()))
		#print "Disconnected from", self.peer, reason.value,'\n'

factory = twisted.internet.protocol.Factory(  )
factory.protocol = EchoProtocol

twisted.internet.reactor.listenTCP(9999, factory)
twisted.internet.reactor.run(  )
