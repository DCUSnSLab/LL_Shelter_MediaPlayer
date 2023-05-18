import os
import subprocess
import threading
from time import sleep

import vlc
import glob

import asyncio  # 웹 소켓 모듈을 선언한다.
import json
import pickle
import websockets  # 클라이언트 접속이 되면 호출된다.

class VlcPlayer:
    '''
    args: VLC인스턴스 생성옵션
    '''

    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()
            

    def set_uri(self, mrl):
        '''
        스트리밍 url주소 또는 로컬 재생파일을 설정
        :param mrl: 스트리밍주소
        :return:
        '''
        self.media.set_mrl(mrl)

    def play(self, path=None):
        '''
        미디어 재생
        :param path:
        :return: 성공:0, 실패:-1
        '''
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()

    def pause(self):
        '''
        재생 멈춤
        :return:
        '''
        self.media.pause()

    def resume(self):
        '''
        재생 다시 시작
        :return:
        '''
        self.media.set_pause(0)

    def stop(self):
        '''
        재생 멈춤
        :return:
        '''
        self.media.stop()

    def is_playing(self):
        '''
        플레이 상태 확인
        :return: 재생중 : 1, 재생중이지 않음 : 0
        '''
        return self.media.is_playing()

    # The total length of audio and video, returns the value in milliseconds
    def get_length(self):
        '''
        미디어소스의 재생길이
        :return: 재생길이(ms)
        '''
        return self.media.get_length()


    # Return to the current state: playing; paused; other
    def get_state(self):
        '''
        현재 플레이어 상태 확인
        :return: playing : 1, paused : 0, 그외 -1
        '''
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    def set_ratio(self, ratio):
        '''
        Set the aspect ratio (such as "16:9", "4:3")
        :param ratio:
        :return:
        '''
        # Must be set to 0, otherwise the screen width and height cannot be modified
        self.media.video_set_scale(0)
        self.media.video_set_aspect_ratio(ratio)

    def add_callback(self, event_type, callback):
        '''
        콜백 listener 설정
        :param event_type: vlc listener 환경변수
        :param callback: 콜백함수
        :return:
        '''
        self.media.event_manager().event_attach(event_type, callback)

    def remove_callback(self, event_type, callback):
        '''
        Remove listener
        :param event_type:
        :param callback:
        :return:
        '''
        self.media.event_manager().event_detach(event_type, callback)


def my_call_back(event):
    print("콜백함수호출: 종료호출")
    global keywork
    if keywork.conStatus == 1 :
        keywork.conStatus = 0
    else :
        keywork.adStatus = 0


async def accept(websocket, path):
    print('accepted', websocket.origin, websocket.id)
    while True:
        data = await websocket.recv()  # 클라이언트로부터 메시지를 대기한다.
        recvdata = json.loads(data)
        recvMsg = recvdata['message']


        #if you receive '0' data from client once, add client socket into Advertiser client list
        #advertise mode ready to client
        print(data)

        keywork.sendMedia(recvMsg)

class KeyWorker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.adStatus = 0  # 0 = 종료, 1 = 재생중, 2 = 일시중지(컨텐츠 재생)
        self.conStatus = 0

    def run(self):
        self.playAd()

    def addCallback(self, callback):
        self.callback = callback
    def playAd(self):
        while True:
            path = '/home/jiwon/dev/LL_Docker_Setup/data/shelter/Advertisement/'
            media_list = list()
            for path, subdirs, files in os.walk(path):
                for name in files:
                    fn = os.path.join(path, name)
                    print(fn)
                    media_list.append(fn)
            print(media_list)

            for var in media_list:
                player.play(var)
                self.adStatus = 1
                while True:
                    if self.adStatus == 2:
                        if self.conStatus == 0:
                            player.play(var)
                            self.adStatus = 1
                            print(var)
                        else:
                            sleep(1)
                            pass
                    elif self.adStatus == 0:
                        break
                    else:
                        sleep(1)
                        pass

    def sendMedia(self, msg):
        self.msg = "CID-"+msg
        self.adStatus = 2
        self.conStatus = 1
        player.play('/home/jiwon/Downloads/loadtest.mp4')
        print(self.msg)


async def main():
    async with websockets.serve(accept, "localhost", 5000):
        await asyncio.Future()


if "__main__" == __name__:
    player = VlcPlayer()
    player.add_callback(vlc.EventType.MediaPlayerStopped, my_call_back)

    keywork = KeyWorker('keyWorker')
    keywork.start()

    asyncio.run(main())
