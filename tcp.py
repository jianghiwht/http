import json
import  uvicorn
from fastapi import FastAPI,Request,WebSocketDisconnect
from starlette.websockets import WebSocket

app = FastAPI()

# 创建一个类 管理http的连接与重新连接
class ConnectHttp:
    def __init__(self):
        self.allusers = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.allusers.append(websocket)
        print(f"客户端连接：{websocket.client}")
    def disconnect(self, websocket: WebSocket):
        self.allusers.remove(websocket)
        print("断开连接")
    async def SeendThemessage(self,message: str):
     for need_seed in self.allusers:
        await need_seed.send(message)
        print("已发送")

#创建容器，存储web连接人员
webuser = ConnectHttp()

#json文件的读取与dumps的格式化
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
    if need_name in valid_names:
        DateMain =date.get(need_name, {})
        DateMain_geshi = json.dumps(DateMain, indent=4, ensure_ascii=False)
        return DateMain_geshi
    else:
        need_names="errors"
        DateMaine = date.get(need_names, {})
        DateMain_geshie = json.dumps(DateMaine, indent=4, ensure_ascii=False)
        return DateMain_geshie


@app.post("/send")  # 用户的接受与发送
async def sendAndAccept(req:Request):
   acceptData= await req.body()
   geshi_Data= acceptData.decode()#格式化数据
   print(geshi_Data)
   _back=Json_answer(geshi_Data)
   await webuser.SeendThemessage(_back)
   return _back


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await webuser.connect(websocket)
    try:
        while True:
            # 保持连接活跃（不处理接收消息）
            await websocket.receive_text()
    except WebSocketDisconnect:
        webuser.disconnect(websocket)

if __name__ == "__main__":
  uvicorn.run(app,host="127.0.0.1",port=8000)

# 需要pip下载对应的第三方包
