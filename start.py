import subprocess
import webbrowser


webbrowser.open("http://127.0.0.1:8000/")
subprocess.run("python manage.py runserver", shell=True)
