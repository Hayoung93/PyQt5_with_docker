from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QVideoFrame
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QPixmap, QImage
import sys
import os
import threading
app = QtWidgets.QApplication(sys.argv)
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from time import sleep


class UI(QtWidgets.QMainWindow):
	# changePixmap = QtCore.pyqtSignal()
	def __init__(self):
		super().__init__()
		self.ui = uic.loadUi('/workspace/demo_cv2_load_entire.ui', self)
		self.ui.button_loadvideo.clicked.connect(self.get_videopath)
		self.ui.button_playpause.clicked.connect(self.playpause)
		self.ui.button_playpause.setEnabled(False)
		self.lineEdit.returnPressed.connect(self.set_videopath)
		# self.slider_video.setRange(0, 0)
		# self.slider_video.sliderMoved.connect(self.set_video_position)

		# self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		# self.player.setVideoOutput(self.videowidget)
		# self.player.positionChanged.connect(self.set_slider_position)
		# self.player.durationChanged.connect(self.set_slider_duration)

		self.slider_cv2.setRange(0, 0)
		self.slider_cv2.setValue(0)
		self.slider_cv2.valueChanged.connect(self.read_videoframe)
		self.slider_cv2.sliderReleased.connect(self.read_videoframe)
		self.slider_cv2.sliderPressed.connect(self.stop_timer)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.set_slider_position)

		self.fig = plt.Figure()
		self.canvas = FigureCanvas(self.fig)
		self.graph_layout.addWidget(self.canvas)

		# self.changePixmap = QtCore.pyqtSignal(QImage)
		# self.changePixmap.connect(self.show_videoframe)

		#-------------
		self.video_format = ('mp4', 'avi', 'mpeg')
		self.videopath = ''
		self.frames = []
		self.isplaying = False
		self.position = 0
		self.cap = None
		self.max_frame = None
		self.values = []
		#-------------

		self.ui.show()
	
	def set_videopath(self):
		self.videopath = self.lineEdit.text()
		# print(self.videopath)
		if (self.videopath != '') \
		and os.path.isfile(self.videopath) \
		and self.videopath.split('.')[-1] in self.video_format:
			# self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.videopath)))
			# self.read_videoframe()
			self.cap = cv2.VideoCapture(self.videopath)
			self.max_frame = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
			self.slider_cv2.setRange(0, self.max_frame)
			self.values = [0 for _ in range(self.max_frame)]
			self.ax = self.fig.add_subplot(111)
			self.ax.plot(self.values)
			self.ax.set_xlabel("frame")
			self.ax.set_ylabel("confidence")
			self.ax.set_title("TEMP graph")
			self.ax.set_ylim([0., 1.])
			self.ax.legend()
			self.read_videoframe()
			self.ui.button_playpause.setEnabled(True)
	
	def get_videopath(self):
		filter = "Videos(*.mp4 *.avi *.mpeg)"
		self.videopath = QtWidgets.QFileDialog.getOpenFileName(self, filter=filter)[0]
		# print(self.videopath)
		if self.videopath != '':
			# self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.videopath)))
			# self.read_videoframe()
			self.lineEdit.setText(self.videopath)
			self.cap = cv2.VideoCapture(self.videopath)
			self.max_frame = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
			self.slider_cv2.setRange(0, self.max_frame)			
			self.values = [0 for _ in range(self.max_frame)]
			self.ax = self.fig.add_subplot(111)
			self.ax.plot(self.values)
			self.ax.set_xlabel("frame")
			self.ax.set_ylabel("confidence")
			self.ax.set_title("TEMP graph")
			self.ax.set_ylim([0., 1.])
			self.ax.legend()
			self.read_videoframe()
			self.ui.button_playpause.setEnabled(True)
			# self.changePixmap.emit()

	def playpause(self):
		# if self.player.state() == QMediaPlayer.PlayingState:
		# 	self.player.pause()
		# 	# pass
		# else:
		# 	self.player.play()
		if not self.isplaying:
			self.timer.start(500)
			self.isplaying = True
			# print("BTN clicked")
		else:
			self.timer.stop()
			self.isplaying = False
			# self.changePixmap.emit()
			# self.read_videoframe()
	
	# def set_video_position(self, position):
	# 	self.player.setPosition(position)
	
	def set_slider_position(self):
		# self.slider_video.setValue(position)
		self.position += 1
		self.slider_cv2.setValue(self.position)

	# def set_slider_duration(self, duration):
	# 	self.slider_video.setRange(0, duration)
	
	def read_videoframe(self):
		# cap = cv2.VideoCapture(self.videopath)
		# while cap.isOpened():
		# 	ret, frame = cap.read()
		# 	if ret:
		# 		self.frames.append(frame)
		# 		print("Loading frame: ", len(self.frames))
		# 	else:
		# 		break
		# 	# cv2.waitKey(30)
		# 	# sleep(1)
		# print("End loading")
		self.position = self.slider_cv2.value()
		self.cap.set(1, self.slider_cv2.value())
		ret, frame = self.cap.read()
		if ret:
			self.show_videoframe(frame)
		else:
			print("Nothing to show")
		# cap.release()
		# cv2.destroyAllWindows()
		self.process_frames_temp(frame)
	
	def show_videoframe(self, frame):
		# print(self.slider_cv2.value())
		# frame = self.frames[self.slider_cv2.value()]
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		h, w, ch = frame.shape
		frame = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
		frame = QPixmap(frame)
		frame = frame.scaled(320, 270, QtCore.Qt.KeepAspectRatio)
		self.label.setPixmap(frame)
		# self.label.update()
	
	# def show_videoframe_stop_timer(self):
	# 	self.timer.stop()
	# 	frame = self.frames[self.slider_cv2.value()]
	# 	self.position = self.slider_cv2.value()
	# 	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	# 	h, w, ch = frame.shape
	# 	frame = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
	# 	frame = QPixmap(frame)
	# 	frame = frame.scaled(320, 270, QtCore.Qt.KeepAspectRatio)
	# 	self.label.setPixmap(frame)
	# 	self.timer.start(500)

	def stop_timer(self):
		self.timer.stop()
		self.isplaying = False
	
	def process_frames_temp(self, frame):
		# values = [0.8 for _ in range(len(self.frames))]
		# print(values)
		self.values[self.slider_cv2.value()] = 0.8
		self.ax.plot(self.values)
		self.canvas.draw()


if __name__ == "__main__":
	# import cv2
	# app = QtWidgets.QApplication(sys.argv)
	window = UI()
	app.exec_()
