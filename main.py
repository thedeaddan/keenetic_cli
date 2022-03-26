import paramiko 
import os
import time
import sys
import webbrowser
import keyboard

global host
global user
global secret
global port
host = '192.168.1.100' # IP Роутера
user = 'admin' # Логин Админ-учётки
secret = '45hH_en@H!WTfYf' # Пароль Админ-учётки
port = 1234 # Порт SSH

selected = 1
class ssh():
	def send_command(command):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname=host, username=user, password=secret, port=port)
		stdin, stdout, stderr = client.exec_command(command)
		client.close()
		
class menu():
	def show():
		os.system("cls")
		global selected
		print("Управление роутером Keenetic:")
		for i in range(1, 5):
			if i == 1:
				text = "Включить VPN клиент"
			elif i == 2:
				text = "Выключить VPN клиент"
			elif i == 3:
				text = "Открыть Админ-Панель"
			elif i == 4:
				text = "Открыть SSH"
			print("{1} {0}.{3} {2}".format(i, ">" if selected == i else " ", "<" if selected == i else " ",text))

	def up():
		global selected
		if selected == 1:
			return
		selected -= 1
		menu.show()

	def down():
		global selected
		if selected == 4:
			return
		selected += 1
		menu.show()
		
	def enter():
		if selected == 1:
			print("Включаю VPN соединение.")
			ssh.send_command("interface PPPoE0 ip global auto")
			print("Выставил нейтральный приоритет стандартному соединению")
			ssh.send_command("interface Wireguard0 ip global auto")
			print("Выставил нейтральный приоритет VPN соединению")
			ssh.send_command("interface PPPoE0 ip global 1")
			print("Приоритет стандартного соединения равен 1")
			ssh.send_command("interface Wireguard0 ip global 2")
			print("Приоритет VPN соединения равен 2")
			print("VPN Включен!")
			time.sleep(5)
			os._exit(0)
		if selected == 2:
			print("Выключаю VPN соединение.")
			ssh.send_command("interface PPPoE0 ip global auto")
			print("Выставил нейтральный приоритет стандартному соединению")
			ssh.send_command("interface Wireguard0 ip global auto")
			print("Выставил нейтральный приоритет VPN соединению")
			ssh.send_command("interface PPPoE0 ip global 2")
			print("Приоритет стандартного соединения равен 2")
			ssh.send_command("interface Wireguard0 ip global 1")
			print("Приоритет VPN соединения равен 1")
			print("VPN Выключен!")
			time.sleep(5)
			os._exit(0)
		if selected == 3:
			webbrowser.get('windows-default').open(f"http://{host}")
		if selected == 4:
			print("Пароль: "+secret)
			os.system(f'ssh -p {port} {user}@{host}')

menu.show()
keyboard.add_hotkey('up', menu.up)
keyboard.add_hotkey('down', menu.down)
keyboard.add_hotkey('enter',menu.enter)
keyboard.wait("enter")
