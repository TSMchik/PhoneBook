import socket
import json


class ClientSocket:
	def __init__(self):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.connect(('127.0.0.1', 12345))

	def send_request(self, action, data=None, field=None, value=None):
		request_data = {'action': action, 'data': data, 'field': field, 'value': value}
		self.client_socket.send(json.dumps(request_data).encode())
# Этот блок кода проверяет, содержит ли переменная `response` какие-либо данные перед попыткой декодирования JSON.
# Если `response` не пустой, то данные декодируются как JSON. Если `response` пустой, то выводится сообщение
# "Empty response received from the server.".
		response = self.client_socket.recv(1024).decode()
		if response:
			try:
				print(json.loads(response))
			except json.decoder.JSONDecodeError as e:
				print("Error decoding JSON response:", e)
		else:
			print("Empty response received from the server.")

	def close_connection(self):
		self.client_socket.close()


class UserInterface:
	@staticmethod
	def get_user_input():
		action = input("Enter action (add/search/delete/view): ")

		if action == 'add':
			first_name = input("Enter first name: ")
			last_name = input("Enter last name: ")
			phone_number = input("Enter phone number: ")
			note = input("Enter note: ")
			data = {'first_name': first_name, 'last_name': last_name, 'phone_number': phone_number, 'note': note}
			client.send_request(action, data)

		elif action == 'search':
			field = input("Enter field to search by (e.g., first_name, last_name): ")
			value = input("Enter value to search for: ")
			client.send_request(action, None, field, value)

		elif action == 'delete':
			entry_id = input("Enter ID to delete: ")
			client.send_request(action, entry_id)

		elif action == 'view':
			entry_id = input("Enter ID to view: ")
			client.send_request(action, entry_id)


# Создаем экземпляр класса ClientSocket
client = ClientSocket()

# Получаем пользовательский ввод и обрабатываем действия
UserInterface.get_user_input()

# Закрываем соединение с сервером
client.close_connection()
