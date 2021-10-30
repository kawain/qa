import subprocess
import webbrowser
import time
import socket


subprocess.Popen("python manage.py runserver", shell=True)

while True:
    time.sleep(1)
    try:
        socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket1.connect(("127.0.0.1", 8000))
        socket1.close()
        webbrowser.open("http://127.0.0.1:8000/")
        break
    except Exception as e:
        _ = e

print("スタート！！！")
