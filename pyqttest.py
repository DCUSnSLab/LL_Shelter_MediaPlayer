"""
A simple example for VLC python bindings using PyQt5.

Author: Saveliy Yusufov, Columbia University, sy2685@columbia.edu
Date: 25 December 2018
"""
import asyncio
import glob
import json
import platform
import os
import sys
from time import sleep

import sysv_ipc
import websockets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import vlc

from advertiser import Advertiser


class Player(QMainWindow):
    def __init__(self, master=None, screens=None, debug=False):
        QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")
        # Create a basic vlc instance
        self.instance = vlc.Instance()

        self.media = None

        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool | Qt.FramelessWindowHint)
        if debug is False:
            self.move(screens[0].geometry().topLeft())
            self.showFullScreen()
        else:
            self.resize(640, 480)
            self.move(700,0)


        self.create_ui()
        self.is_paused = False

        # self.timer = QTimer(self)
        # self.timer.setInterval(100)
        # self.timer.timeout.connect(self.update_ui)

        #self.open_file('/home/soobin/development/LL_Docker_Setup/data/shelter/Advertisement/AID-16/daegu_ad.mp4')

        self.plistwk = Playlist(self.mediaplayer, parent=self)
        self.plistwk.content_msg.connect(self.playupdater)
        self.plistwk.start()

        self.advsync = AdvSync(self.mediaplayer, parent=self)
        self.advsync.sync_handler.connect(self.plistwk.syncEventHndl)
        self.advsync.start()

    def create_ui(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if platform.system() == "Darwin": # for MacOS
            self.videoframe = QMacCocoaViewContainer(0)
        else:
            self.videoframe = QFrame()

        self.palette = self.videoframe.palette()
        self.palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        #self.videoframe.setAutoFillBackground(True)

        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.vboxlayout)



    def playupdater(self, msg):
        self.open_file(msg)


    def play_pause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            #self.playbutton.setText("Play")
            self.is_paused = True
            #self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file()
                return

            self.mediaplayer.play()
            #self.playbutton.setText("Pause")
            #self.timer.start()
            self.is_paused = False

    def stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        #self.playbutton.setText("Play")

    def open_file(self, addr):
        filename = addr
        if not filename:
            return

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = self.instance.media_new(filename)

        # Put the media in the media player
        self.mediaplayer.set_media(self.media)

        # Parse the metadata of the file
        self.media.parse()

        # Set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == "Linux": # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows": # for Windows
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

        self.play_pause()

    def set_volume(self, volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(volume)

    def set_position(self):
        """Set the movie position according to the position slider.
        """

        # The vlc MediaPlayer needs a float value between 0 and 1, Qt uses
        # integer variables, so you need a factor; the higher the factor, the
        # more precise are the results (1000 should suffice).

        # Set the media position to where the slider was dragged
        self.timer.stop()
        pos = self.positionslider.value()
        self.mediaplayer.set_position(pos / 1000.0)
        self.timer.start()

    def update_ui(self):
        """Updates the user interface"""

        # Set the slider's position to its corresponding media position
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        #self.positionslider.setValue(media_pos)

        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # After the video finished, the play button stills shows "Pause",
            # which is not the desired behavior of a media player.
            # This fixes that "bug".
            if not self.is_paused:
                self.stop()

class Playlist(QThread):
    content_msg = pyqtSignal(str)

    def __init__(self, mediaplayer, parent=None):
        super().__init__()
        print('create playlist worker')
        self.main = parent
        self.mediaplayer = mediaplayer
        self.working = True

    def __del__(self):
        print('finish thread...')
        self.wait()

    def syncEventHndl(self, data):
        print('Playlist handled=',data)
        subdir = 'AID-'+data
        path = '/Users/soobinjeon/Developments/LL_Docker_Setup/data/shelter/Advertisement/'+subdir+'/*'
        content = glob.glob(path)
        for var in content:
            self.content_msg.emit(var)

    def run(self):
        #self.playlist()
        while True:
            sleep(1)
        pass

    def playlist(self):
        sleep(0.5)
        while True:
            path = '/Users/soobinjeon/Developments/LL_Docker_Setup/data/shelter/Advertisement/'
            media_list = list()
            for path, subdirs, files in os.walk(path):
                for name in files:
                    fn = os.path.join(path, name)
                    print(fn)
                    media_list.append(fn)
            # print(media_list)

            for var in media_list:
                # self.open_file(var)
                self.content_msg.emit(var)
                # player.play(var)
                self.adStatus = 1
                print('play media:', var)
                sleep(0.5)
                while True:
                    # print('mediaplayer : ', self.mediaplayer.is_playing())
                    if not self.mediaplayer.is_playing():
                        break
                    else:
                        sleep(0.5)
                    # if self.adStatus == 2:
                    #     if self.conStatus == 0:
                    #         self.open_file(var)
                    #         #player.play(var)
                    #         self.adStatus = 1
                    #         print(var)
                    #     else:
                    #         sleep(1)
                    #         pass
                    # elif self.adStatus == 0:
                    #     break
                    # else:
                    #     sleep(1)
                    #     pass

class AdvSync(QThread):
    sync_handler = pyqtSignal(str)

    def __init__(self, mediaplayer, parent=None):
        super().__init__()
        print('create websocket worker')
        self.main = parent
        self.mediaplayer = mediaplayer
        self.working = True
        self.adv_mq = sysv_ipc.MessageQueue(3820, sysv_ipc.IPC_CREAT)

    def run(self):
        while True:
            data = self.adv_mq.receive(type=0)
            self.sync_handler.emit(str(int(data[0])))




def main():
    """Entry point for our simple vlc player
    """
    app = QApplication(sys.argv)
    player = Player(master=None, screens=app.screens(), debug=True)
    player.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()