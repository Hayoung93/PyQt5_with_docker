from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QVideoFrame
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap, QImage
import sys
app = QtWidgets.QApplication(sys.argv)
import cv2
from time import sleep


class UI(QtWidgets.QMainWindow):
	changePixmap = QtCore.pyqtSignal()
	def __init__(self):
		super().__init__()
		self.ui = uic.loadUi('/workspace/temp.ui', self)
		# self.ui.setupUi(self)
		# self.ui.button_loadvideo.clicked.connect(self.show_text)
		self.ui.button_loadvideo.clicked.connect(self.get_videopath)
		self.ui.button_playpause.clicked.connect(self.playpause)
		self.ui.button_playpause.setEnabled(False)
		self.lineEdit.returnPressed.connect(self.set_videopath)
		self.slider_video.setRange(0, 0)
		self.slider_video.sliderMoved.connect(self.set_video_position)

		self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		self.player.setVideoOutput(self.videowidget)
		self.player.positionChanged.connect(self.set_slider_position)
		self.player.durationChanged.connect(self.set_slider_duration)

		# self.changePixmap = QtCore.pyqtSignal(QImage)
		self.changePixmap.connect(self.read_videoframe)

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
			# self.read_videoframe()
			self.changePixmap.emit()
	

	def playpause(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			self.player.pause()
			# pass
		else:
			self.player.play()
			# self.read_videoframe()
	
	def set_video_position(self, position):
		self.player.setPosition(position)
	
	def set_slider_position(self, position):
		self.slider_video.setValue(position)

	
	def set_slider_duration(self, duration):
		self.slider_video.setRange(0, duration)
	
	def read_videoframe(self):
		cap = cv2.VideoCapture(self.videopath)
		while cap.isOpened():
			ret, frame = cap.read()
			if ret:
				self.show_videoframe(frame)
			else:
				break
			cv2.waitKey(30)
			# sleep(1)
		cap.release()
		cv2.destroyAllWindows()
	
	def show_videoframe(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		h, w, ch = frame.shape
		frame = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
		frame = QPixmap(frame)
		frame = frame.scaled(320, 270, QtCore.Qt.KeepAspectRatio)
		self.label.setPixmap(frame)
		# self.label.update()
	
	def process_frame_temp(self, frame):
		return 0.8


if __name__ == "__main__":
	# import cv2
	# app = QtWidgets.QApplication(sys.argv)
	window = UI()
	app.exec_()
