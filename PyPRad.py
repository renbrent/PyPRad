import sys, validators
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import (QApplication, QInputDialog, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QMessageBox, QPushButton, QSizePolicy, QSlider,
                               QStyle, QVBoxLayout, QWidget)
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtGui  import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(400,100)

        self.setWindowTitle("PyPRad")

        # Icon made by https://www.flaticon.com/authors/freepik
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowIconText("PyPRad")

        self.current_stream = ""

        # Setup Media Player
        self.player = QMediaPlayer(self, QMediaPlayer.StreamPlayback)
        self.player.setMedia(QUrl(self.current_stream))

        # Connect Button
        connect_btn = QPushButton("Connect To Stream")
        connect_btn.setFixedWidth(150)
        connect_btn.clicked.connect(self.connectStream)
        
        # Play Button
        self.play = QPushButton()
        self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play.setFixedWidth(100)
        self.play.clicked.connect(self.playStream)

        # Volume Slider
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0,100)
        slider.setFixedWidth(100)
        slider.setValue(100)
        slider.valueChanged.connect(self.setVolume)

        # Horizontal Layout
        hbox_layout = QHBoxLayout()
        hbox_layout.setContentsMargins(0,0,0,0)
        hbox_layout.addWidget(connect_btn)
        hbox_layout.addWidget(self.play)
        hbox_layout.addWidget(slider)

        widget = QWidget()
        widget.setLayout(hbox_layout)

        self.player.stateChanged.connect(self.mediaStateChanged)

        self.setCentralWidget(widget)

    def connectStream(self):
        dlg = QInputDialog(self)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText("URL:")
        dlg.setTextEchoMode(QLineEdit.Normal)
        dlg.setTextValue(self.current_stream)
        dlg.resize(400,100)
        dlg.exec()

        if dlg.result() and validators.url(dlg.textValue()) and dlg.textValue() != self.current_stream:
            self.current_stream = dlg.textValue()
            self.player.setMedia(QUrl(self.current_stream))
        elif dlg.result() and not validators.url(dlg.textValue()):
            msg_box = QMessageBox()
            msg_box.setText("Error URL. Please try again")
            msg_box.setWindowTitle("Error URL")
            msg_box.exec()
            self.connectStream()

    def playStream(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()
    
    def mediaStateChanged(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    
    def setVolume(self, volume):
        self.player.setVolume(volume)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())