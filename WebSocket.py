from fastapi import FastAPI
import websockets

from Model import Todo

app = FastAPI()

# Java 서버의 WebSocket 엔드포인트 주소
java_server_uri = "ws://localhost:8080/chatt"
import websockets

class WebSocketManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.websocket = None
        return cls._instance

    async def connect(self, java_server_uri):
        if self.websocket is None or not self.websocket.open:
            self.websocket = await websockets.connect(java_server_uri)
            print("연결 완료")

    async def send_message(self, message):
        if self.websocket is not None and self.websocket.open:
            await self.websocket.send(message)

    async def close(self):
        if self.websocket is not None and self.websocket.open:
            await self.websocket.close()

websocket_manager = WebSocketManager()

@app.on_event("startup")
async def startup_event():
    await websocket_manager.connect(java_server_uri)

@app.post("/send_data")
async def send_data_to_java_server(todo: Todo):
    try:
        await websocket_manager.send_message("message.id")
        return {"message": "Data sent to Java server successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.on_event("shutdown")
async def shutdown_event():
    await websocket_manager.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
