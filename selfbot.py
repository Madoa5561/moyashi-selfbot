from CHRLINE_Square import *
import time, threading, hashlib, random, sys, json, traceback, qrcode, concurrent,base64
import os
from datetime import datetime
import time
import requests
import json
import datetime
import asyncio
import livejson
from youtubesearchpython import Search
import google.generativeai as genai

dt_now = datetime.datetime.now()
args = sys.argv

async def kickio(gid,target):
     for a in target:
        if not a in cl.mid:
          try:
              cl.deleteOtherFromChat(str(gid), str(a))
          except Exception as e:
              print(e)
              break

async def main(gid,target):
    try:
        task1 = asyncio.create_task(kickio(gid,target))
        await task1
    except Exception as e:
        print(e)
#nohup python3 OWNER.py {Mid} &
def notify(notification_message):
    line_notify_token = '*****'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': notification_message}
    requests.post(line_notify_api, headers = headers, data = data)

json_open = open('authdata.json', 'r')
json_load = json.load(json_open)
if not args[1][0] == "Q":
    try:
        if args[1] in json_load["token"].values():
            try:
                cl = CHRLINE(json_load["token"][args[1]],device="IOSIPAD",useThrift=False)
                notify(f"\nVer: BETA\ntype: AuthToken\nlogged In:{cl.getContact(cl.mid)[22]}\nTime :{dt_now.strftime('%Y年%m月%d日 %H:%M:%S')}")
            except:
                del json_load["token"][args[1]]
                notify("前回のauthTokenが失効しています\nメアドパスログインします")
        else:
            cl = CHRLINE(json_load["mail"][args[1]],json_load["pass"][args[1]],device="IOSIPAD",useThrift=False)
            json_load["token"][args[1]] = cl.authToken
            notify(f"\nVer: BETA\ntype: mail\nlogged In:{cl.getContact(cl.mid)[22]}\nTime :{dt_now.strftime('%Y年%m月%d日 %H:%M:%S')}")
    except:
        notify(f"\nアカウント情報が登録されてないかパスワードが違います")
else:
    try:
        if f"QR:{args[1]}" in json_load["token"].values():
            try:
                cl = CHRLINE(json_load["token"][args[1]],device="IOSIPAD",useThrift=False)
                notify(f"\nVer: BETA\ntype: AuthToken\nlogged In:{cl.getContact(cl.mid)[22]}\nTime :{dt_now.strftime('%Y年%m月%d日 %H:%M:%S')}")
            except:
                del json_load["token"][args[1]]
                notify("前回のauthTokenが失効しています\nQRログインセッションを開始します")
                cl = CHRLINE(device="IOSIPAD",useThrift=False)
                json_load["token"][args[1]] = cl.authToken
                notify(f"\nVer: BETA\ntype: QR\nlogged In:{cl.getContact(cl.mid)[22]}\nTime :{dt_now.strftime('%Y年%m月%d日 %H:%M:%S')}")
        else:
            cl = CHRLINE(device="IOSIPAD",useThrift=False)
            json_load["token"][args[1]] = cl.authToken
            notify(f"\nVer: BETA\ntype: QR\nlogged In:{cl.getContact(cl.mid)[22]}\nTime :{dt_now.strftime('%Y年%m月%d日 %H:%M:%S')}")
    except:
        notify(f"\nQRコードログインが確認できませんでした\n30分後にやり直すか作者をメンションしてください")
json_open.close()

#cl = CHRLINE("","",device="IOSIPAD",useThrift=False) force login
# No E2EE support

def sendE2EE(to,text,where):
    _from = cl.mid
    selfKeyData = cl.getE2EESelfKeyData(_from)
    if len(to) == 0 or cl.getToType(to) != 0:
        cl.sendMessage(where,'Invalid mid')
    if selfKeyData is None:
        cl.sendMessage(where,'E2EE Key has not been saved, try register or use SQR Login')
    senderKeyId = selfKeyData['keyId']
    private_key = base64.b64decode(selfKeyData['privKey'])
    receiver_key_data = cl.negotiateE2EEPublicKey(to)
    if receiver_key_data[3] == -1:
        cl.sendMessage(where,f'Not support E2EE on {to}')
        receiverKeyId = receiver_key_data[2][2]
        keyData = cl.generateSharedSecret(bytes(private_key), receiver_key_data[2][4])
        specVersion = receiver_key_data[3]
        encData = cl.encryptE2EETextMessage(senderKeyId, receiverKeyId, keyData, specVersion, text, to ,_from)


def sendstamp(to):
    contentMetadata = {'STKTXT': '[Sticker]', 'STKOPT': '0', 'STKVER': '3', 'STKID': '47977', 'STKPKGID': '2000000'}
    cl.sendMessage(to,contentMetadata=contentMetadata)

def kick333(a,klist):
    for kmid in klist:
        if not kmid[1] in cl.profile[1]:
            cl.deleteOtherFromChat(a, kmid[1])

def AllStamp(to):
    metadata = {'MENTION': '{"MENTIONEES":[{"S":"0","E":"4","A":"1"}]}','NOTIFICATION_DISABLED': 'false', 'STKTXT': '[Sticker]', 'app_extension_type': 'null', 'app_version_code': '121720390', 'STKVER': '1', 'STKID': '175', 'STKPKGID': '2'}
    cl.sendMessage(to, "@All", contentMetadata=metadata,contentType=7)

def kick(gid,target):
    try:
        cl.deleteOtherFromChat(gid, target)
    except:
        pass

def allmention(to):
 arr = {}
 reply = "@NHK"
 arr = [
          {
               "S": str(0),
               "A": str(1),
               "E": str(4)
          }
 ]
 contentMetadata = {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}
 cl.sendMessage(to, reply, contentMetadata=contentMetadata)

def youtubeSearch(word,limit):
    base = {
    "type": "carousel",
    "contents": []
}
    result = Search(word, limit = limit).result()['result']
    print(len(result))
    ct = 0
    for data in result:
        if ct == 11:
            break
        if data['type'] == 'video':
            ct += 1
            flat = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": data['thumbnails'][0]['url'],
        "size": "full",
        "action": {
          "type": "uri",
          "label": "URL",
          "uri": f"https://www.youtube.com/watch?v={data['id']}"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": data['channel']['name'],
            "weight": "bold",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "text",
            "wrap": True,
            "text": data["title"]
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "©2024 moyashi bot",
            "size": "sm",
            "weight": "bold",
            "align": "center"
          }
        ],
        "backgroundColor": "#7FCCE3"
      }
    }
            base["contents"].append(flat)
    return base

def youtubeVideos(samune,title,sityousuu,nagasa):
  base = {
  "type": "bubble",
  "size": "kilo",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": samune,
            "aspectRatio": "2:1",
            "aspectMode": "cover",
            "size": "full"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "YOUTUBE",
                "weight": "bold",
                "color": "#ff0000",
                "size": "xxs"
              }
            ],
            "position": "absolute",
            "backgroundColor": "#ffffff",
            "paddingAll": "5px"
          }
        ],
        "flex": 0
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": title,
            "weight": "bold",
            "wrap": True,
            "decoration": "underline",
            "size": "xs"
          }
        ],
        "paddingTop": "5px"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Author",
                "size": "xs"
              },
              {
                "type": "text",
                "text": nagasa,
                "size": "xs"
              },
              {
                "type": "text",
                "text": sityousuu,
                "size": "xs"
              }
            ],
            "paddingEnd": "10px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "author",
                "size": "xs"
              },
              {
                "type": "text",
                "text": "duration",
                "size": "xs"
              },
              {
                "type": "text",
                "text": "watched",
                "size": "xs"
              }
            ],
            "paddingEnd": "15px",
            "flex": 2
          }
        ],
        "backgroundColor": "#ffffff",
        "paddingTop": "5px"
      }
    ],
    "paddingAll": "10px",
    "cornerRadius": "10px"
  }
}

def sendFlex(to: str, alt: str, flex: dict) -> None:
    """
    LINE Liff Flex を送信する

    Parameters:
        to (str): 送信する user ID
        alt (str): Flex の altText
        flex (dict): Flex の内容

    Returns:
        None
    """
    data = {"type": "flex", "altText": alt, "contents": flex}
    cl.sendLiff(to, data)

logoutFlex = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "iPadをログアウトしてください",
        "weight": "bold",
        "align": "center"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "ログアウトする",
          "uri": "line://nv/connectedDevices"
        }
      }
    ],
    "flex": 0
  }
}

unicode = """͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.
coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.co ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.c	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻oﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.co
coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.co ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.co
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.co
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.co
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.co
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.co
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.co
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
ﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.coﭱ.
 ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	
	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉ ͇	 ͈	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻	 ̻ ̻	 ̻ ͍	 ͎	 ͇	 ͈	 ͉	 ͊	 ͋	 ͌	 ͍	 ͎	  ͇	 ͈	 ͉	 ͊"""
rev = 0
rec_msgs = []

status = livejson.File(f'{cl.mid}.json', True, False, 4)

if status == {}:
  status["HIDE"] = False
  status["HIDEkc"] = False
  status["NYA"] = False
  status["kickpro"] = []
  status["invpro"] = []
  status["canpro"] = []
  status["urlpro"] = []
  status["AU"] = False
  status["AR"] = []
  status["local"] = {}
  status["black"] = {}
  status["st"] = []
  status["lockdown"] = False
else:
  pass

def RefusalReceive(cl, enabled=True):
    set = {}
    set[26] = enabled
    cl.updateSettingsAttributes2(set, [25])

def ustamp(to):
   contentMetadata = {'STKTXT': "None", 'STKOPT': '0', 'STKVER': '3', 'STKID': '47977', 'STKPKGID': '2000000'}
   cl.sendMessage(to,unicode,contentMetadata=contentMetadata)
def bot(op,cl):
            if op[3] == 130:
                if not op[10] in status["black"]:
                  status["black"][op[10]] = []
                else:
                  pass
                if op[11] in status["black"][op[10]]:
                  cl.deleteOtherFromChat(op[10],op[11])
            if op[3] == 132:
              if status["HIDEkc"] == True:
                msgids = cl.getRecentMessagesV2(op[10],30)
                lens = 1
                ids = []
                for dat in msgids:
                  if str(cl.mid) in str(dat[1]):
                    ids.append(str(dat[4]))
                  if len(ids) == lens:
                    break
                  else:
                    pass
                for i in ids:
                    try:
                      cl.unsendMessage(i)
                    except:
                      break
            if op[3] == 133:
              if not op[10] in status["black"]:
                status["black"][op[10]] = []
              else:
                pass
              if not op[10] in status["local"]:
                status["local"][op[10]] = []
              else:
                pass
              if not op[11] in cl.profile[1]:
                 if op[10] in status["kickpro"]:
                    if op[13] in status["local"][op[10]]:
                        status["black"][op[10]].append(op[11])
                        cl.deleteOtherFromChat(op[10],op[11])
                        cl.inviteIntoChat(op[10],[op[12]])
                    else:
                        status["black"][op[10]].append(op[11])
                        cl.deleteOtherFromChat(op[10],op[11])
            if op[3] == 122:
              if not op[10] in status["black"]:
                status["black"][op[10]] = []
              else:
                pass
              if not op[10] in status["local"]:
                status["local"][op[10]] = []
              else:
                pass
              if op[12] == '4' and op[10] in status["urlpro"]:
                if not op[12] in cl.profile[1]:
                  if not op[12] in status["local"][op[10]]:
                    status["black"][op[10]].append(op[12])
                    cl.deleteOtherFromChat(op[10],op[12])
                    cl.updateChatPreventedUrl(op[10], True)
            if op[3] == 124 and status["AU"] == True:
              try:
                inv3 = op[12].replace('\x1e',',')
                data = inv3.split(',')
              except:
                data = op[12]
              if cl.profile[1] in data:
                  cl.acceptInviteIntoChat(op[10])
            if op[3] == 123:
              if status["HIDE"] == True:
                msgids = cl.getRecentMessagesV2(op[10],30)
                lens = 1
                ids = []
                for dat in msgids:
                  if str(cl.mid) in str(dat[1]):
                    ids.append(str(dat[4]))
                  if len(ids) == lens:
                    break
                  else:
                    pass
                for i in ids:
                    try:
                      cl.unsendMessage(i)
                    except:
                      break
            if op[3] == 26:
              if not op[10] in status["black"]:
                status["black"][op[10]] = []
              else:
                pass
              if not op[10] in status["local"]:
                status["local"][op[10]] = []
              else:
                pass
              msg = op[20]
              if msg[15] == 0:
                  if msg[3] == 2:
                    try:
                      if msg[1] in status["local"][msg[2]]:
                        if msg[10] == "test":
                          time.sleep(0.2)
                          cl.sendMessage(msg[2],"Ready")
                        if msg[10] == "help":
                          time.sleep(0.2)
                          cl.sendMessage(msg[2],"helpmessage\n\ntest\n>> 動作確認\nset:{kick or inv or can or url}:{on / off}\n>> 保護設定\nbclear\n>> ブラリス初期化\nblist\n>> ブラリス一覧\nai:質問\n>> geminiに質問")
                        if msg[10] == "bclear":
                          status["black"][op[10]] = []
                          time.sleep(0.2)
                          cl.sendMessage(msg[2],"ブラリス初期化したよ")
                        if msg[10] == "blist":
                          t = "ブラリス一覧"
                          if not status["black"][msg[2]] == []:
                            for mid in status["black"][msg[2]]:
                              try:
                                 t += f"・{cl.getContact(mid)[22]}"
                              except:
                                 t += "・Unknown"
                            cl.sendMessage(msg[2],t)
                          else:
                            cl.sendMessage(msg[2],"ブラリスは登録されていません")
                        if msg[10].startswith("ai:"):
                            gemini_pro = genai.GenerativeModel("gemini-pro")
                            prompt = msg[10][3:]
                            response = gemini_pro.generate_content(prompt)
                            cl.sendMessage(to,f"あなた:{prompt}\n\nGemini:{response.text}",relatedMessageId=msg[4])
                        if msg[10].startswith("set:"):
                          splited = msg[10].split(":")
                          if splited[1] == "kick":
                              if splited[2] == "on":
                                  if not msg[2] in status["kickpro"]:
                                      status["kickpro"].append(msg[2])
                                      cl.sendMessage(msg[2],"ok")
                                  else:
                                      cl.sendMessage(msg[2],"ok")
                              if splited[2] == "off":
                                  if to in status["kickpro"]:
                                      status["kickpro"].remove(to)
                                      cl.sendMessage(to,"ok")
                                  else:
                                      cl.sendMessage(to,"ok")
                          if splited[1] == "inv":
                              if splited[2] == "on":
                                  if not to in status["invpro"]:
                                      status["invpro"].append(to)
                                      cl.sendMessage(to,"ok")
                                  else:
                                      cl.sendMessage(to,"ok")
                              if splited[2] == "off":
                                  if to in status["invpro"]:
                                      status["invpro"].remove(to)
                                      cl.sendMessage(to,"ok")
                                  else:
                                      cl.sendMessage(to,"ok")
                          if splited[1] == "can":
                              if splited[2] == "on":
                                  if not to in status["canpro"]:
                                      status["canpro"].append(to)
                                      cl.sendMessage(to,"ok")
                                  else:
                                      cl.sendMessage(to,"ok")
                              if splited[2] == "off":
                                  if to in status["canpro"]:
                                      status["canpro"].remove(to)
                                      cl.sendMessage(to,"ok")
                                  else:
                                      cl.sendMessage(to,"ok")
                          if splited[1] == "url":
                              if splited[2] == "on":
                                  if not to in status["urlpro"]:
                                      status["urlpro"].append(to)
                                      cl.updateChatPreventedUrl(to, True)
                                      cl.sendMessage(to,"ok")
                                  else:
                                      cl.sendMessage(to,"ok")
                              if splited[2] == "off":
                                  if to in status["urlpro"]:
                                      status["urlpro"].remove(to)
                                  else:
                                      pass

                      if msg[1] in "ucbeb65a5ca8a70ddcba3924ff0522ad5":
                        if msg[10].startswith("_send:"):
                          cl.sendMessage(msg[2],msg[10][:6])
                        if msg[10] == "_test":
                          cl.sendMessage(msg[2],"ok")
                      if msg[2] in status["AR"]:
                        cl.sendChatChecked(msg[1],msg[4])
                    except:
                      pass
                  if status["lockdown"] == True:
                    if msg[2][0] == "u":
                      try:
                          if msg[18]['LOC_KEY'] == "C_MA":
                            cl.blockContact(msg[1])
                      except Exception as e:
                            print(e)

            if op[3] == 25:
              msg = op[20]
              if msg[15] == 0:
                if msg[3] == 2:
                    try:
                      to = msg[2]
                      if status["NYA"] == True:
                        if not "にゃ" in msg[10] and not 'MENTION' in msg[18]:
                          time.sleep(0.2)
                          cl.unsendMessage(msg[4])
                          time.sleep(0.2)
                          try:
                              cl.sendMessage(msg[2],f"{msg[10]}にゃ",relatedMessageId=msg[21])
                          except:
                              cl.sendMessage(msg[2],f"{msg[10]}にゃ")
                      if msg[10] == "Mstmk":
                          for tag in status["st"]:
                            mk_strong = threading.Thread(target=kick, args=(msg[2], tag)).start()
                      if msg[10].startswith("autojoin:"):
                        a = msg[10].replace("autojoin:","")
                        if a == "on":
                          status["AU"] = True
                          cl.sendMessage(msg[2],"自動参加をオンにしました")
                        if a == "off":
                          status["AU"] = False
                          cl.sendMessage(msg[2],"自動参加をオフにしました")
                        else:
                          pass
                      if msg[10].startswith("stdel"):
                        mids = []
                        texts = "del kc"
                        if "MENTION" in msg[18]:
                            key = eval(msg[18]["MENTION"])
                            tags = key["MENTIONEES"]
                        for mids in tags:
                            if mids["M"] in status["st"]:
                                status["st"].remove(mids["M"])
                                texts = texts + f"\n・{cl.getContact(mids['M'])[22]}"
                        cl.sendMessage(to,texts)
                      if msg[10] == "bclear":
                          if not msg[2] in status["black"]:
                            status["black"][msg[2]] = []
                          else:
                            pass
                          status["black"][msg[2]] = []
                          time.sleep(0.2)
                          cl.sendMessage(msg[2],"ブラリス初期化したよ")
                      if msg[10] == "llist":
                        if not msg[2] in status["local"]:
                          status["local"][msg[2]] = []
                        else:
                          pass
                        if not status["local"][msg[2]]:
                          t = "個別権限者リスト"
                          for a in status["local"][msg[2]]:
                            t = t + f"\n・{cl.getContact(a)[22]}"
                          cl.sendMessage(to,t)
                        else:
                          cl.sendMessage(to,"個別権限者リストは空だよ")
                      if msg[10] == "stmklist":
                        if not status["st"] == []:
                          t = "stmklist"
                          for a in status["st"]:
                            t = t + f"\n・{cl.getContact(a)[22]}"
                          cl.sendMessage(to,t)
                        else:
                          cl.sendMessage(to,"蹴りリストは空だよん")
                      if msg[10].startswith("stadd"):
                        mids = []
                        texts = "add kc"
                        if "MENTION" in msg[18]:
                            key = eval(msg[18]["MENTION"])
                            tags = key["MENTIONEES"]
                        for mids in tags:
                            if not mids["M"] in status["st"]:
                                status["st"].append(cl.getContact(mids["M"])[1])
                                texts = texts + f"\n・{cl.getContact(mids['M'])[22]}"
                        cl.sendMessage(to,texts)
                      if msg[10].startswith("ldel"):
                        mids = []
                        if not msg[2] in status["local"]:
                          status["local"][msg[2]] = []
                        else:
                          pass
                        texts = "個別権限削除"
                        if "MENTION" in msg[18]:
                            key = eval(msg[18]["MENTION"])
                            tags = key["MENTIONEES"]
                            for mids in tags:
                              if mids["M"] in status["local"][msg[2]]:
                                status["local"][msg[2]].remove(mids["M"])
                                texts = texts + f"\n・{cl.getContact(mids['M'])[22]}"
                        cl.sendMessage(to,texts)
                      if msg[10].startswith("ladd"):
                        mids = []
                        if not msg[2] in status["local"]:
                          status["local"][msg[2]] = []
                        else:
                          pass
                        texts = "個別権限追加"
                        if "MENTION" in msg[18]:
                            key = eval(msg[18]["MENTION"])
                            tags = key["MENTIONEES"]
                            for mids in tags:
                              if not mids["M"] in status["local"][msg[2]]:
                                status["local"][msg[2]].append(cl.getContact(mids["M"])[1])
                                texts = texts + f"\n・{cl.getContact(mids['M'])[22]}"
                        cl.sendMessage(to,texts)
                      if msg[10] == "blist":
                          if not msg[2] in status["black"]:
                            status["black"][msg[2]] = []
                          else:
                            pass
                          t = "ブラリス一覧"
                          for mid in status["black"][msg[2]]:
                            try:
                              t += f"・{cl.getContact(mid)[22]}"
                            except:
                              t += "・Unknown"
                          cl.sendMessage(msg[2],t)
                      if msg[10].startswith("autoread:"):
                        a = msg[10].replace("autoread:","")
                        if a == "on":
                          if not to in status["AR"]:
                            status["AR"].append(to)
                            cl.sendMessage(msg[2],"自動既読をオンにしました")
                          else:
                            cl.sendMessage(msg[2],"自動既読はすでにオンです")
                        if a == "off":
                          if to in status["AR"]:
                            status["AR"].remove(to)
                            cl.sendMessage(msg[2],"自動既読をオフにしました")
                          else:
                            cl.sendMessage(msg[2],"自動既読をオフにしました")
                        else:
                          pass

                      if msg[10].startswith("kchide:on"):
                        status["HIDEkc"] = True
                        cl.sendMessage(msg[2],"kchideをオンにしました")
                      if msg[10].startswith("kchide:off"):
                        status["HIDEkc"] = False
                        cl.sendMessage(msg[2],"kchideをオフにしました")
                      if msg[10].startswith("hide:on"):
                        status["HIDE"] = True
                        cl.sendMessage(msg[2],"hideをオンにしました")
                      if msg[10].startswith("hide:off"):
                        status["HIDE"] = False
                        cl.sendMessage(msg[2],"hideをオフにしました")
                      if msg[10].startswith("にゃ:on"):
                        status["NYA"] = True
                        cl.sendMessage(msg[2],"にゃモードをオンにしました")
                      if msg[10].startswith("にゃ:off"):
                        status["NYA"] = False
                        cl.sendMessage(msg[2],"にゃモードをオフにしました")
                      if msg[10] == "limit":
                        t="規制状況\n"
                        try:
                          cl.deleteOtherFromChat(to,cl.profile[1])
                        except Exception as E:
                          res = str(E).replace("Code: 0, Message:","")
                          res = res.replace(", Metadata: {}","")
                          if res == " can not kick self out":
                            t+="\n蹴り: 大丈夫！！"
                          else:
                            t+="\n蹴り: 規制だよん"
                        try:
                          cl.inviteIntoChat(to,[cl.profile[1]])
                          t+="\n招待: 大丈夫！！"
                        except Exception as E:
                          t+="\n招待: 規制だよん"
                        cl.sendMessage(to,t)

                      if msg[10].startswith("con:"):
                        try:
                            a = msg[10].replace("con:","")
                            time.sleep(1)
                            cl.sendContact(msg[2],a)
                            time.sleep(1)
                            cl.sendMessage(msg[2],cl.getContact(a))
                        except:
                            pass
                      if msg[10] == 'ginfo':
                        try:
                            gid = cl.getChats([msg[2]])
                            g_info = "ぐる情報"
                            g_info += "\nなまえ\n" + gid[1][0][6]
                            g_info += "\ngid\n" + gid[1][0][2]
                            try:
                                g_info += "\nさくしゃ\n" + cl.getContact(gid[1][0][8][1][1])[22]
                            except:
                                g_info += "\nさくしゃ\n" + cl.getContact(gid[1][0][8][1][1])[22] + " 垢消し"
                            try:
                                g_info += "\nぐる画\n%s/%s" % (
                                        cl.LINE_OBS_DOMAIN, gid[1][0][7])
                            except:
                                g_info += "\nぐる画\n%s/%s" % (
                                          cl.LINE_OBS_DOMAIN, 'None')
                                g_info += "\n作られたじかん\n" + time.strftime(
                                        '%Y-%m-%d %I:%M:%S %p', time.localtime(gid[1][0][2]/1000))
                            try:
                                g_info += "\nメンバー数:" + str(len(gid[1][0][8][1][4])) + "\n招待数:" + str(len(gid[1][0][8][5]))
                            except:
                                g_info += "\nメンバー数:" + str(len(gid[1][0][8][1][4])) + "\n招待数:0"
                            if gid[1][0][8][1][2] is False:
                                g_info += "\nグループURL:おん"
                            else:
                                g_info += "\nグループURL:おふ"
                            time.sleep(0.3)
                            cl.sendMessage(msg[2], f'{g_info}', relatedMessageId=msg[4])
                        except Exception as e:
                            print(e)
                      if msg[10] == "mkof":
                        status["HIDEkc"] == False
                        try:
                            a = cl.getChats([msg[2]])
                            for b in a[1][0][8][1][4]:
                               if 34 in b and b[34]:
                                 try:
                                     cl.deleteOtherFromChat(msg[2], b[1])
                                     time.sleep(1)
                                 except:
                                     break
                            for b in a[1][0][8][1][5]:
                              if 34 in b and b[34]:
                                try:
                                    cl.cancelChatInvitation(msg[2], b[1])
                                    time.sleep(1)
                                except:
                                    break
                        except:
                            pass
                      if msg[10].startswith("yt:"):
                        temp = youtubeSearch(msg[10][2:],10)
                        sendFlex(to,"検索結果",temp)
                      if msg[10].startswith("mute:"):
                        try:
                            contentMetadata = {'NOTIFICATION_DISABLED': 'true'}
                            a = msg[10].replace("mute:","")
                            i = a.split(':')
                            for u in range(int(i[0])):
                               try:
                                   cl.sendMessage(msg[2],str(i[1]),contentMetadata=contentMetadata)
                               except:
                                   break
                        except:
                            pass
                      if msg[10] == 'test':
                        time.sleep(0.3)
                        cl.sendMessage(msg[2],"うごいてるよん:")
                      if msg[10] == "mkall":
                        status["HIDEkc"] = False
                        target = cl.getChats([msg[2]])[1][0][8][1][4]
                        targets = []
                        for a in target:
                            targets.append(a)
                        asyncio.run(main(msg[2],targets))
                      if msg[10].startswith("st_mk"):
                        status["HIDEkc"] == False
                        metadata = msg[18]
                        reply = msg[1]
                        if 'MENTION' in metadata:
                          key = eval(metadata["MENTION"])
                          tags = key["MENTIONEES"]
                          for tag in tags:
                             mk_strong = threading.Thread(target=kick, args=(msg[2], tag['M'])).start()
                        else:
                          cl.sendMessage(msg[2], 'None a memtionees mid data:')
                      if msg[10].startswith('mk') and not msg[10] == "mkall":
                        status["HIDEkc"] == False
                        metadata = msg[18]
                        reply = msg[1]
                        if 'MENTION' in metadata:
                          key = eval(metadata["MENTION"])
                          tags = key["MENTIONEES"]
                          for tag in tags:
                             try:
                                 cl.deleteOtherFromChat(msg[2], tag['M'])
                                 time.sleep(0.7)
                             except:
                                 break
                        else:
                          cl.sendMessage(msg[2], 'みつからなかったよ😥:')
                      if msg[10].startswith("range:"):
                          a = msg[10].replace("range:","")
                          i = a.split(':')
                          for u in range(int(i[0])):
                             try:
                                 cl.sendMessage(msg[2],str(i[1]))
                                 time.sleep(0.4)
                             except:
                                 cl.sendMessage(msg[2],"Error:")
                                 break
                      if msg[10].startswith("all:"):
                          a = msg[10].replace("all:","")
                          for u in range(int(a)):
                             try:
                                 allmention(msg[2])
                                 time.sleep(0.4)
                             except:
                                 cl.sendMessage(msg[2],"error:")
                                 break
                          cl.sendMessage(msg[2],"end:")
                      if msg[10].startswith("set:"):
                        splited = msg[10].split(":")
                        if splited[1] == "kick":
                            if splited[2] == "on":
                                if not msg[2] in status["kickpro"]:
                                    status["kickpro"].append(msg[2])
                                    cl.sendMessage(msg[2],"ok")
                                else:
                                    cl.sendMessage(msg[2],"ok")
                            if splited[2] == "off":
                                if to in status["kickpro"]:
                                    status["kickpro"].remove(to)
                                    cl.sendMessage(to,"ok")
                                else:
                                    cl.sendMessage(to,"ok")
                        if splited[1] == "inv":
                            if splited[2] == "on":
                                if not to in status["invpro"]:
                                    status["invpro"].append(to)
                                    cl.sendMessage(to,"ok")
                                else:
                                    cl.sendMessage(to,"ok")
                            if splited[2] == "off":
                                if to in status["invpro"]:
                                    status["invpro"].remove(to)
                                    cl.sendMessage(to,"ok")
                                else:
                                    cl.sendMessage(to,"ok")
                        if splited[1] == "can":
                            if splited[2] == "on":
                                if not to in status["canpro"]:
                                    status["canpro"].append(to)
                                    cl.sendMessage(to,"ok")
                                else:
                                    cl.sendMessage(to,"ok")
                            if splited[2] == "off":
                                if to in status["canpro"]:
                                    status["canpro"].remove(to)
                                    cl.sendMessage(to,"ok")
                                else:
                                    cl.sendMessage(to,"ok")
                        if splited[1] == "url":
                            if splited[2] == "on":
                                if not to in status["urlpro"]:
                                    status["urlpro"].append(to)
                                    cl.updateChatPreventedUrl(to, True)
                                    cl.sendMessage(to,"ok")
                                else:
                                    cl.sendMessage(to,"ok")
                            if splited[2] == "off":
                                if to in status["urlpro"]:
                                    status["urlpro"].remove(to)
                                else:
                                    pass
                      if msg[10].startswith("an:"):
                        txt = msg[10].replace("an:","")
                        a = txt.split(':')
                        i = cl.sendMessage(msg[2],a[0])
                        msgid = i[4]
                        for u in range(int(a[1])):
                           try:
                               cl.createChatRoomAnnouncement(msg[2],a[0],f"line://nv/chatMsg?chatId={msg[2]}&messageId={msgid}")
                               time.sleep(0.4)
                           except Exception as error:
                               print(f"error:{error}")
                               cl.sendMessage(msg[2],"Error:")
                               break
                        cl.sendMessage(msg[2],"end:")
                      if msg[10].startswith("st_all:"):
                          a = msg[10].replace("st_all:","")
                          for u in range(int(a)):
                             try:
                                 allmention(msg[2])
                             except:
                                 cl.sendMessage(msg[2],"error:")
                                 break
                      if msg[10].startswith("say:"): 
                        a = msg[10].split(":")
                        metadata = msg[18]
                        reply = msg[1]
                        if 'MENTION' in metadata:
                          key = eval(metadata["MENTION"])
                          tags = key["MENTIONEES"]
                          for tag in tags:
                             for a in range(int(a[1])):
                                try:
                                    time.sleep(0.3)
                                    allmention(tag["M"])
                                except:
                                    cl.sendMessage(msg[2],"えらーおきた！")
                                    break
                      if msg[10].startswith("send:"):
                        a = msg[10].replace("send:","")
                        i = a.split(':')
                        try:
                            cl.sendMessage(str(i[0]),str(i[1]))
                        except:
                            time.sleep(0.3)
                            cl.sendMessage(msg[2],"E:not a member")
                      if msg[10].startswith("allsend:"):
                        i = msg[10].replace("allsend:","")
                        gid = cl.getAllChatMids()[1]
                        count = len(gid)
                        sec = int(count) * 3 
                        time.sleep(0.3)
                        cl.sendMessage(msg[2],f"全ぐる送信します\n終了予定:{sec}秒")
                        for a in gid:
                           try:
                               cl.sendMessage(a,i)
                               time.sleep(3)
                           except:
                               name = cl.getGroup(a)[10]
                               cl.sendMessage(msg[2],"エラー：{name}で送信に失敗しました")
                               pass
                      if msg[10] == "friends":
                        getfriends = len(cl.getAllContactIds())
                        time.sleep(0.3)
                        cl.sendMessage(msg[2],f"{getfriends}:")
                      if msg[10].startswith("allkick:"):
                        i = msg[10].replace("allkick:","")
                        gids = cl.getAllChatMids()[1]
                        gid = cl.getChats(gids)
                        count = len(gid)
                        sec = int(count) * 3
                        time.sleep(0.3)
                        cl.sendMessage(msg[2],f"全ぐるから{cl.getContact(i)[22]}を蹴ります\n終了予定:{sec}秒")
                        for a in gid:
                           try:
                               cl.deleteOtherFromChat(a[1],i)
                               time.sleep(3)
                           except:
                               cl.sendMessage(msg[2],"エラー:{a[22]}で蹴りに失敗しました")
                               break
                        cl.sendMessage(msg[2],"終了しました:")
                      if msg[10].startswith("lockdown:"):
                        a = msg[10].replace("lockdown:","")
                        if a == "on":
                          status["lockdown"] = True
                          time.sleep(0.3)
                          cl.sendMessage(to,"ロックダウンモードをオンにしました")
                        if a == "off":
                          status["lockdown"] = False
                          time.sleep(0.3)
                          cl.sendMessage(to,"ロックダウンモードをオフにしました")
                      if msg[10].startswith("sends:"):
                        i = msg[10].replace("sends:","")
                        o = i.split(":",2)
                        gid = cl.getAllChatMids()[1]
                        groups = cl.getChats(gid)
                        count = 0
                        for a in groups[1][0]:
                           if str(o[0]) in str(a[6]):
                             count = count + 1
                           else:
                             pass
                        sec = int(count) * 3 
                        time.sleep(0.3)
                        cl.sendMessage(msg[2],f"特定ぐる送信します\n終了予定:{sec}秒")
                        for a in groups[1][0]:
                           if str(o[0]) in str(a[6]):
                             try:
                                 cl.sendMessage(a[1],o[1])
                                 time.sleep(3)
                             except:
                                 name = a[10]
                                 cl.sendMessage(msg[2],f"エラー:{name}で送信に失敗しました")
                           else:
                             pass
                        time.sleep(0.3)
                        cl.sendMessage(msg[2],"終了しました:")
                      if msg[10].startswith("nk:"):
                        word = msg[10].replace("nk:","")
                        data = cl.getChats([msg[2]])[1][0][8][1][4]
                        data2 = cl.getContacts(data)
                        for names in data2:
                           if str(word) in str(names[22]):
                            cl.deleteOtherFromChat(msg[2],names[1])
                            time.sleep(0.4)
                           else:
                            break
                      if msg[10].startswith("inv:"):
                        a = msg[10].replace("inv:","")
                        i = a.split(':')
                        try:
                            time.sleep(0.3)
                            cl.inviteIntoChat(str(i[0]),[str(i[1])])
                        except:
                            time.sleep(0.3)
                            cl.sendMessage(msg[2],"E:not a member")
                      if msg[10].startswith("kick:"):
                        a = msg[10].replace("kick:","")
                        i = a.split(':')
                        try:
                            time.sleep(0.3)
                            cl.deleteOtherFromChat(str(i[0]), str(i[1]))
                        except:
                            time.sleep(0.3)
                            cl.sendMessage(msg[2],"not a member:")

                      if msg[10] == "glist-id":
                        gid = cl.getAllChatMids()[1]
                        groups = cl.getChats(gid)
                        temp = "all joined group ids:"
                        for a in groups:
                            temp += f"\n・{a[1][0][2]}"
                        time.sleep(0.3)
                        cl.sendMessage(msg[2],temp)
                      if msg[10] == "glist-name":
                        gid = cl.getAllChatMids()[1]
                        groups = cl.getChats(gid)
                        temp = "all joined group names:"
                        for a in groups:
                            temp = temp + f"\n・{a[1][0][6]}"
                        time.sleep(0.3)
                        cl.sendMessage(msg[2],temp)
                      if msg[10] == "glist-name-id" or msg[10] == "glist-id-name":
                        gid = cl.getAllChatMids()[1]
                        groups = cl.getChats(gid)
                        temp = "all joined group names and ids:"
                        for a in groups:
                            temp = temp + f"\nname・{a[1][0][6]}\ngid・{a[1][0][2]}"
                        time.sleep(0.3)
                        cl.sendMessage(msg[2],temp)
                      if msg[10] == "total joined":
                        try:
                            gid = cl.getAllChatMids()[1]
                            total = len(gid)
                            time.sleep(0.3)
                            cl.sendMessage(msg[2],f"{total}:")
                        except:
                            pass
                      if msg[10] == "favorite":
                        try:
                            favo = cl.getFavoriteMids()
                            lenfavo = len(favo)
                            temp = "favorite list:"
                            for con in favo:
                               temp = temp + f"\n・{cl.getContact(con)[22]}"
                            time.sleep(0.3)
                            cl.sendMessage(msg[2],temp + f"\ntotal {lenfavo}")
                        except:
                            pass
                      if msg[10] == "logout":
                        sendFlex(to,"logout",logoutFlex)
                      if msg[10] == "th_kall":
                        status["HIDEkc"] == False
                        klist = cl.getChats([msg[2]])[1][0][8][1][4]
                        ka = threading.Thread(target=kick333, args=(msg[2], klist)).start()
                      if msg[10].startswith("un:"):
                          data = msg[10].split(":")
                          time.sleep(0.3)
                          msgids = cl.getRecentMessagesV2(msg[2],300)
                          lens = int(data[1]) + 1
                          ids = []
                          for dat in msgids:
                               if str(cl.mid) in str(dat[1]):
                                  ids.append(str(dat[4]))
                                  if len(ids) == lens:
                                    break
                                  else:
                                    pass
                               else:
                                 pass
                          for i in ids:
                               try:
                                   time.sleep(0.3)
                                   cl.unsendMessage(i)
                               except:
                                   time.sleep(0.3)
                                   cl.sendMessage(msg[2],"24時間経ったメッセージは取り消せません:")
                                   break
                      if msg[10].startswith("gomi:"):
                        splited = msg[10].split(":")
                        try:
                          for a in range(int(splited[1])):
                            AllStamp(msg[2])
                        except:
                            pass
                      if msg[10] == "help":
                        try:
                            time.sleep(0.3)
                            cl.sendMessage(msg[2],"""helpmessage
type: beta v1.4

logout
>>ログアウトします
con:{mid}
>>連絡先
range:[回数]:[文字]
>>マクロ
mkof
>>公式け.り
mk @
>>メンションけり
st_mk @
>>非同.期メンションけ.り
ginfo
>>ぐる
send:[group id]:[msg]
>>メッセージ送信
inv:[group id]:[mid]
>>招待
kick:[group id]:[mid]
>>回しけ.り
all:[num]
>>オルメンマ.クロ
mute:[回数]:[文字]
>>ミュートメッセージでマ.クロ
allsend:[msg]
>>参加中の全ぐるに送信
sends:[group name]:[msg]
>>特定の名前の全ぐるに送信
glist-id
>>参加中の全ぐるのid
glist-name
>>参加中の全ぐるの名前
glist-name-id
>>参加中の全ぐるの名前とid
total joined
>>合計参加ぐる数
allkick:[mid]
>>全ぐるから回し蹴り
favorite
>>お気に入りリスト表示
un:[num]
>>送信取り消し|30まで|
friends
>>友達数
mkall
>>普通のぜんけり
hide:on / off
>>招待ログ自動削除
にゃ:on / off
>>にゃモードの変更(うんこ機能だ
say:[回数]: @
>>個チャで回数分オ.ルメン
an:[テキスト]:[回数]
>>アナウンスマクロ
th_kall
>>仮非.同期ぜん.けり
gomi:回数
>>オルメンスタンプマ.クロ
autojoin:{on / off}
>>自動参加
set:{kick or inv or can or url}:{on / off}
>>グル別保護
llist
>> 個別権限者リスト
autoread:{on / off}
>>自動既読
stadd @
>> キックリスト追加
stdel @
>>キックリスト削除
Mstmk
蹴りリスト実行
stlist
>>蹴りリスト一覧
l[add / del] @
>> 個別権限追加/削除
--------
yt:文字
>> youtube検索
--------

kchide:{on / off}
>>蹴りログ自動削除(蹴りコマンドを利用した場合自動的にオフになります)
lockdown:{on / off}
>>>アカウントが攻撃された場合にアカウントを閉鎖的にするモードです
>>>よほどのことがない限り有効にしないでください""")
                        except:
                            pass
                    except Exception as error:
                      print(error)
                if msg[15] == 13: # user infomation
                        time.sleep(0.3)
                        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
                            someone = cl.getContact(msg[18]["mid"])
                            try:
                                executor.submit(cl.sendMessage(msg[2], 'なまえ:\n%s\n内部識別子:\n%s\nステメ:\n%s\nプロフ画:\n%s/%s' % (
                                    someone[22], someone[1], someone[26][:100], cl.LINE_PROFILE_CDN_DOMAIN, someone[24])))
                            except:
                                executor.submit(cl.sendMessage(msg[2], 'なまえ:\n%s\n内部識別子:\n%s\nステメ:\n%s\nプロフ画:\n%s/%s' % (
                                    someone[22], someone[1], someone[26][:100], cl.LINE_PROFILE_CDN_DOMAIN, 'None')))
cl.trace(bot)
