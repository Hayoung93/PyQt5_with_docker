from PyQt5 import QtWidgets, uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import sys


class UI(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = uic.loadUi('/workspace/temp.ui', self)
		# self.ui.setupUi(self)
		# self.ui.button_loadvideo.clicked.connect(self.show_text)
		self.ui.button_loadvideo.clicked.connect(self.get_videopath)
		self.ui.button_playpause.clicked.connect(self.playpause)
		self.ui.button_playpause.setEnabled(False)
		self.lineEdit.returnPressed.connect(self.set_videopath)

		self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		self.player.setVideoOutput(self.videowidget)

		#-------------
		self.videopath = ''
		#-------------

		self.ui.show()
	
	# def show_text(self):
	# 	self.text = "Hello World!"
	# 	self.lineEdit.setText(self.text)
	
	def set_videopath(self):
		self.videopath = self.lineEdit.text()
		# print(self.videopath)
		if self.videopath != '':
			self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.videopath)))
			self.ui.button_playpause.setEnabled(True)
	
	def get_videopath(self):
		filter = "Videos(*.mp4 *.avi *.mpeg)"
		self.videopath = QtWidgets.QFileDialog.getOpenFileName(self, filter=filter)[0]
		# print(self.videopath)
		if self.videopath != '':
			self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.videopath)))
			self.ui.button_playpause.setEnabled(True)
	
	def playpause(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			self.player.pause()
		else:
			self.player.play()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = UI()
	app.exec_()
