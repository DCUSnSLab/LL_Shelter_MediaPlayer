import asyncio
import json
import pickle
import websockets

async def accept(websocket, path):
    print('accepted', websocket.origin, websocket.id)
    while True:
        data = await websocket.recv()  # 클라이언트로부터 메시지를 대기한다.
        recvdata = json.loads(data)
        recvMsg = recvdata['message']

        # if you receive '0' data from client once, add client socket into Advertiser client list
        # advertise mode ready to client
        print(data)

        # keywork.sendMedia(recvMsg)


async def websockermain():
    print('run websocker')
    async with websockets.serve(accept, "localhost", 5001):
        await asyncio.Future()

if "__main__" == __name__:
    asyncio.run(websockermain())