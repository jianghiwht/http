import json
import socket
import time

def Json_answer(need_name):
    try:
        with open("date.json", "r", encoding="utf-8") as f:
            date = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("检查date.json是否存在")
        return "date.json 文件不存在或格式错误"

    try:
        with open("name.dat", "r", encoding="utf-8") as f:
            valid_names = {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        print("检查name.dat是否存在")


    print(need_name)
    if need_name in valid_names:
        DateMain =date.get(need_name, {})
        DateMain_geshi = json.dumps(DateMain, indent=4, ensure_ascii=False)
        return DateMain_geshi
    elif need_name == " ":
          return " "   #防止空字符串
    else:
        need_names="errors"
        DateMaine = date.get(need_names, {})
        DateMain_geshie = json.dumps(DateMaine, indent=4, ensure_ascii=False)
        return DateMain_geshie

def AcceptMessage(conn_port):
   _Maxhuanchong=512
   conn_port.settimeout(3)#设置超时等待
   while True:
       ListenDate = b''
       try:
           chunk = conn_port.recv(_Maxhuanchong)#设置一些逻辑辅助超时等待
           ListenDate += chunk
           time.sleep(2)
           break
       except socket.timeout:
           if not ListenDate:
               continue #修复一个问题 break会退出while循环 导致空的字符串 泄露
           else:
            continue
   DateBack=ListenDate.decode('utf-8').strip()
   conn_port.settimeout(None)#回复为空等待下一次
   return DateBack

def SeendThemessage(conn2,message):

    conn2.send(message.encode('utf-8'))
    time.sleep(1)
    print("成功发送")


def SocketConnect():
    IpAddress = "127.0.0.1"
    port = 990
    TheListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TheListen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TheListen.bind((IpAddress, port))
    TheListen.listen(3)
    print("等待客户端连接...")

    TheInterface, addr = TheListen.accept()
    print(f"连接方：{addr}")
    return TheInterface

if __name__ == "__main__":

    while True:
        jiekou = SocketConnect()
        _back=AcceptMessage(jiekou)
        message_=Json_answer(_back)
        SeendThemessage(jiekou,message_)
        time.sleep(2)
        jiekou.close()#这是断开连接的关键。如果不需要可以删除/This is the key to disconnecting. If not needed, delete it.



# the writer country is china  ,so "print"or "#" follow if Chinese， please translation 。

