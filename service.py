import socket
import threading
import sys
import pickle

class Service():
	"""docstring for Servidor"""
	def __init__(self, host="localhost", port=4000):

		self.clientes = []

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((str(host), int(port)))
		self.sock.listen(10)
		self.sock.setblocking(False)

		accept = threading.Thread(target=self.acceptCon)
		procesar = threading.Thread(target=self.procesarCon)
		
		accept.daemon = True
		accept.start()

		procesar.daemon = True
		procesar.start()

		while True:
			msg = input('->')
			if msg == 'end':
				self.sock.close()
				sys.exit()
			else:
				pass


	def msg_to_all(self, msg, cliente):
		for c in self.clientes:
			try:
				if c != cliente:
					c.send(msg)
			except:
				self.clientes.remove(c)

	def acceptCon(self):
		print("接受新连接")
		while True:
			try:
				conn, addr = self.sock.accept()
				conn.setblocking(False)
				self.clientes.append(conn)
			except:
				pass

	def procesarCon(self):
		print("转发")
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(1024)
						if data:
							self.msg_to_all(data,c)
					except:
						pass


s = Service()