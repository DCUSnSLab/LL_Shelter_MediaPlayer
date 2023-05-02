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

    def release(self):
        '''
        미디어 소스 초기화
        :return:
        '''
        return self.media.release()

    def is_playing(self):
        '''
        플레이 상태 확인
        :return: 재생중 : 1, 재생중이지 않음 : 0
        '''
        return self.media.is_playing()

    def get_time(self):
        '''
        Elapsed time, return millisecond value
        :return:
        '''
        return self.media.get_time()

    def set_time(self, ms):
        '''
        미디어 특정시간으로 이동.
        :param ms:
        :return: 성공 : 0, 실패 : -1
        '''
        return self.media.get_time(ms)

    # The total length of audio and video, returns the value in milliseconds
    def get_length(self):
        '''
        미디어소스의 재생길이
        :return: 재생길이(ms)
        '''
        return self.media.get_length()

    def get_volume(self):
        '''
        :return: 현재 볼륨 상태 값 (0~100)
        '''
        return self.media.audio_get_volume()

    def set_volume(self, volume):
        '''
        볼륨 설정
        :param volume: 0~100 사이 값
        :return:
        '''
        return self.media.audio_set_volume(volume)

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

    def get_position(self):
        '''
        현재 playback 진척도
        :return: 미디어의 재생율 (1 이하 소숫점)
        '''
        return self.media.get_position()

    def set_position(self, float_val):
        '''
        특정 재생율로 미디어의 재생위치를 변경.
        :param float_val: 0~1 사이 float값
        :return:
        '''
        return self.media.set_position(float_val)

    def get_rate(self):
        '''
        :return: 재생속도
        '''
        return self.media.get_rate()

    def set_rate(self, rate):
        '''
        재생속도 설정
        :param rate: 배속
        :return:
        '''
        return self.media.set_rate(rate)

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
        for var in media_list:
            player.play(var)
            status = 0
            while True:
                if status == 1:
                    break
                else:
                    pass
