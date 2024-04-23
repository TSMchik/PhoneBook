import socket
import sqlite3
import json
import threading


# Класс для работы с базой данных
class Database:
	def __init__(self, db_name):
		self.conn = sqlite3.connect(db_name)
		self.conn.row_factory = sqlite3.Row
		self.c = self.conn.cursor()

	def add_contact(self, data):
		with self.conn:
			self.c.execute("INSERT INTO phonebook (first_name, last_name, phone_number, note) VALUES (?, ?, ?, ?)",
						   (data['first_name'], data['last_name'], data['phone_number'], data['note']))
			return json.dumps("Контакт успешно добавлен")

	def delete_contact(self, contact_id):
		with self.conn:
			self.c.execute("DELETE FROM phonebook WHERE id=?", (contact_id,))
			return json.dumps("Контакт успешно удален")

	def search_contact(self, field, value):
		with self.conn:
			self.c.execute(f"SELECT * FROM phonebook WHERE {field}=?", (value,))
			result = self.c.fetchall()
			return json.dumps(result)

	def view_contact(self, contact_id):
		with self.conn:
			self.c.execute("SELECT * FROM phonebook WHERE id=?", (contact_id,))
			result = self.c.fetchone()
			return json.dumps(result)


# Класс для создания сервера
class Server:
	def __init__(self):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind(('127.0.0.1', 12345))
		self.server_socket.listen(5)

	def run(self):
		while True:
			client_socket, addr = self.server_socket.accept()
			client_thread = ClientThread(client_socket)
			client_thread.start()


# Поток для обработки клиентских запросов
class ClientThread(threading.Thread):
	def __init__(self, client_socket):
		threading.Thread.__init__(self)
		self.client_socket = client_socket

	def run(self):
		db = Database('phonebook.db')
		request = self.client_socket.recv(1024).decode()
		request_data = json.loads(request)

		if request_data['action'] == 'add':
			response = db.add_contact(request_data['data'])
		elif request_data['action'] == 'delete':
			response = db.delete_contact(request_data['data'])
		elif request_data['action'] == 'search':
			response = db.search_contact(request_data['field'], request_data['value'])
		elif request_data['action'] == 'view':
			response = db.view_contact(request_data['data'])

		self.client_socket.send(response.encode())
		db.conn.close()


if __name__ == "__main__":
	phonebook_server = Server()
	phonebook_server.run()
