from time import sleep

import vlc
import glob

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
    global status
    status = 1


if "__main__" == __name__:

    # 뮤직비디오 파일
    media_file = "/home/jiwon/Downloads/test1.mp4"

    path = '/home/jiwon/Videos/*.mp4'
    media_list = glob.glob(path)

    print(media_list)

    player = VlcPlayer()
    player.add_callback(vlc.EventType.MediaPlayerStopped, my_call_back)

    while True:
        path = '/home/jiwon/Videos/*.mp4'
        media_list = glob.glob(path)
        for var in media_list:
            player.play(var)
            status = 0
            while True:
                if status == 1:
                    break
                else:
                    sleep(1)
                    pass
