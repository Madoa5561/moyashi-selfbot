from CHRLINE_0 import *
import requests, json
import subprocess, time, threading
import pyqrcode
from youtubesearchpython import *

cl = CHRLINE("***",device="ANDROID",useThrift=True)


def sendMessage(message):
    line_notify_token = '*****'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers)

waitd = {"wait":{},"freze":[]}
def wait(mid,time):
    waitd['wait'][mid] = {"time":time,"TF":True}
    waitd['freze'].append(mid)
    try:
        while waitd['wait'][mid]["TF"]:
            if not waitd['wait'][mid]["time"] == 0:
                waitd['wait'][mid]["time"] = waitd['wait'][mid]["time"] - 1
                time.sleep(1)
            else:
                waitd['freze'].remove(mid)
                del waitd["wait"][mid]
    except:
        pass

def login(code):
    subprocess.run(['nohup', 'python3', 'selfbot.py', code, '&'])

def beta(code):
    subprocess.run(['nohup', 'python3', 'selfbot_beta.py', code, '&'])

def sendQR(message):
    url = "https://notify-api.line.me/api/notify"
    token = "*****"
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message" :  message}
    files = {"imageFile":open('./qr.jpeg','rb')}
    post = requests.post(url ,headers = headers ,params=payload,files=files)

def handle_message(op,cl):
    if op.type == 124:
        if op.param3 == cl.mid:
            if op.param1 == "c262b0f92f0b8d5c1cf4197282a062741":
                cl.acceptChatInvitation(op.param1)
            else:
                cl.deleteSelfFromChat(op.param1)
        else:
            pass
    if op.type == 26:
        if not op.message._from in waitd['freze']:
            if op.message.text.startswith("debug:"):
                dd = op.message.text.replace("debug:","")
                video = Video.get(dd, mode = ResultMode.json, get_upload_date=True)
            if op.message.text == "reset" and op.message._from == "ua8754c2f3804b5379e19938fa89afbc5":
                sendMessage("\nおk")
            if op.message.text == "login":
                #threading.Thread(target=wait,args=(op.message._from,1800)).start()
                json_open = open('authdata.json', 'r')
                json_load = json.load(json_open)
                json_open.close()
                if op.message._from in json_load["mail"]:
                    sendMessage("\nメアドログインを開始します")
                    threading.Thread(target=login,args=(op.message._from,)).start()
                else:
                    sendMessage("QRコードログインを開始します")
                    subprocess.run(['rm', './url.txt'])
                    subprocess.run(['rm', './pin.txt'])
                    threading.Thread(target=login,args=(f"QR:{op.message._from}",)).start()
                    time.sleep(7)
                    try:
                        URL = open('./url.txt', 'r')
                        data = URL.read()
                        code = pyqrcode.create(data, error='L', version=8, mode='binary')
                        code.png("./qr.jpeg", scale=5, module_color=[0, 0, 0, 128], background=[255, 255, 255])
                        sendQR(f"\n1分以内にログインしてください\n{data}")
                        URL.close()
                        time.sleep(60)
                        pin = open('./pin.txt', 'r')
                        data = pin.read()
                        sendMessage(f"{data}")
                        pin.close()
                    except:
                        pass
            if op.message.text == "login:beta":
                #threading.Thread(target=wait,args=(op.message._from,1800)).start()
                json_open = open('authdata.json', 'r')
                json_load = json.load(json_open)
                json_open.close()
                if op.message._from in json_load["mail"]:
                    sendMessage("これはベータ版です、不安定です、規制なるかもしれないです\nメアドログインを開始します")
                    threading.Thread(target=beta,args=(op.message._from,)).start()
                else:
                    sendMessage("これはベータ版です、不安定です、規制なるかもしれないです\nQRコードログインを開始します")
                    subprocess.run(['rm', './url.txt'])
                    subprocess.run(['rm', './pin.txt'])
                    threading.Thread(target=beta,args=(f"QR:{op.message._from}",)).start()
                    time.sleep(7)
                    try:
                        URL = open('./url.txt', 'r')
                        data = URL.read()
                        code = pyqrcode.create(data, error='L', version=8, mode='binary')
                        code.png("./qr.jpeg", scale=5, module_color=[0, 0, 0, 128], background=[255, 255, 255])
                        sendQR(f"\n1分以内にログインしてください\n{data}")
                        URL.close()
                        time.sleep(60)
                        pin = open('./pin.txt', 'r')
                        data = pin.read()
                        sendMessage(f"{data}")
                        pin.close()
                    except:
                        pass
            else:
                pass
        else:
            if op.message.text == "login":
                sendMessage(f"次ログインできるのは{waitd['wait'][op.message._from]['time']}秒後です")
cl.trace(handle_message)
