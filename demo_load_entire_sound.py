from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QVideoFrame
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QPixmap, QImage
import sys
import os
app = QtWidgets.QApplication(sys.argv)
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class UI(QtWidgets.QMainWindow):
	# changePixmap = QtCore.pyqtSignal()
	def __init__(self):
		super().__init__()
		uic.loadUi('/workspace/demo_cv2_load_entire.ui', self)
		self.button_loadvideo.clicked.connect(self.get_videopath)
		self.button_playpause.clicked.connect(self.playpause)
		self.button_playpause.setEnabled(False)
		self.lineEdit.returnPressed.connect(self.set_videopath)		
		self.button_gtbox.clicked.connect(self.toggle_gtbox)
		self.button_gtbox.setEnabled(False)
		x = self.label.geometry().left()
		w = self.label.geometry().width()
		y = self.label.geometry().top()
		h = self.label.geometry().height()
		self.button_gtbox.move(x + w + 50, y)
		self.button_debug.clicked.connect(self.debug)
		self.button_debug.move(x + w + 50, y + 50)

		self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		self.player.setVideoOutput(self.videowidget)

		self.slider_cv2.setRange(0, 0)
		self.slider_cv2.setValue(0)
		self.slider_cv2.valueChanged.connect(self.show_videoframe)
		self.slider_cv2.valueChanged.connect(self.set_point_on_graph)
		self.slider_cv2.sliderReleased.connect(self.slider_released)
		self.slider_cv2.sliderPressed.connect(self.stop_timer)
		self.slider_cv2.move(x, y + h + 50)

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.inc_slider_position)
		self.timer_resize = QTimer(self)
		self.timer_resize.timeout.connect(self.audio_sink)

		self.fig = plt.Figure()
		self.canvas = FigureCanvas(self.fig)
		

############################
		# self.widget = widget(parent=self.centralwidget)
		# self.widget.resize(400, 170)
		# self.graph_layout = QtWidgets.QVBoxLayout(parent=self.widget)
		# self.graph_layout = qvboxlayout()
		# self.canvas = Canvas(self.fig)
		# self.canvas.setMouseTracking(True)
#########################
		
		self.graph_layout.addWidget(self.canvas)
		self.widget.move(x, y + h + 100)
		self.button_playpause.move(x, y + h + 150 + self.widget.size().height())

		self.setMouseTracking(True)
		# self.centralwidget.setMouseTracking(True)
		# self.centralwidget.moved.connect()

		#-------------
		self.video_format = ('mp4', 'avi', 'mpeg')
		self.videopath = ''
		self.frames = []
		self.isplaying = False
		self.gt_box = []
		self.isgtbox = False
		self.isresized = False
		self.fps = 0
		#-------------


		#---------For resizeing widget-----------
		w, h = self.size().width(), self.size().height()
		self.ratio_label = (self.label.size().width() / w, self.label.size().height() / h)
		self.ratio_slider_cv2 = self.slider_cv2.size().width() / w
		self.graph_layout.activate()
		self.ratio_widget = (self.widget.size().width() / w, self.widget.size().height() / h)
		self.initial_wh = (w, h)
		#----------------------------------------

		self.show()
		
	
	def debug(self):
		print("debug")
	
	# def mouseMoveEvent(self, event):
	# 	print(event.x(), event.y())	

	def resizeEvent(self, event):
		self.isresized = True
		self.timer_resize.start(100)

		# print("Resized")
		QtWidgets.QMainWindow.resizeEvent(self, event)
		self.resize_widget(self.label, 'both', self.ratio_label)
		self.resize_widget(self.slider_cv2, 'width', self.ratio_slider_cv2)
		# self.resize_widget(self.graph_layout, 'both', self.ratio_graph_layout)
		self.resize_widget(self.widget, 'both', self.ratio_widget)

		x = self.label.geometry().left()
		w = self.label.geometry().width()
		y = self.label.geometry().top()
		h = self.label.geometry().height()
		self.button_gtbox.move(x + w + 50, y)
		self.button_debug.move(x + w + 50, y + 50)
		self.slider_cv2.move(x, y + h + 50)
		self.widget.move(x, y + h + 100)
		self.button_playpause.move(x, y + h+ 150 + self.widget.size().height())

		self.show_videoframe()

	def audio_sink(self):
		if self.isresized:
			self.isresized = False
		else:		
			self.slider_cv2.setValue(int(self.player.position() * self.fps / 1000))
			self.show_videoframe()
			self.timer_resize.stop()

	def set_videopath(self):
		self.videopath = self.lineEdit.text()
		# print(self.videopath)
		if (self.videopath != '') \
		and os.path.isfile(self.videopath) \
		and self.videopath.split('.')[-1] in self.video_format:
			if os.path.exists(self.videopath.split(".")[0] + "_gtbox.txt"):
					with open(self.videopath.split(".")[0] + "_gtbox.txt", "r") as f:
						self.gt_box = f.read().splitlines()
			self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.videopath)))
			self.cap = cv2.VideoCapture(self.videopath)
			self.fps = self.cap.get(cv2.CAP_PROP_FPS)
			self.spf = int(1000 / self.fps)
			self.button_gtbox.setEnabled(True)
			self.read_videoframe()
			self.show_videoframe()
	
	def get_videopath(self):
		if self.isplaying:
			self.timer.stop()
			self.isplaying = False
			self.player.pause()
		filter = "Videos(*.mp4 *.avi *.mpeg)"
		self.videopath = QtWidgets.QFileDialog.getOpenFileName(self, filter=filter)[0]
		if self.videopath != '':
			if os.path.exists(self.videopath.split(".")[0] + "_gtbox.txt"):
				with open(self.videopath.split(".")[0] + "_gtbox.txt", "r") as f:
					self.gt_box = f.read().splitlines()
			self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.videopath)))
			self.cap = cv2.VideoCapture(self.videopath)
			self.fps = self.cap.get(cv2.CAP_PROP_FPS)
			self.spf = int(1000 / self.fps)
			self.button_gtbox.setEnabled(True)
			self.read_videoframe()
			self.show_videoframe()

	def playpause(self):
		if not self.isplaying:
			self.timer.start(self.spf)
			self.isplaying = True
			self.player.play()
		else:
			self.timer.stop()
			self.isplaying = False
			self.player.pause()
	
	def set_video_position(self):
		player_position = self.slider_cv2.value() * self.spf
		self.player.setPosition(player_position)
	
	def inc_slider_position(self):
		self.slider_cv2.setValue(self.slider_cv2.value() + 1)
	
	def read_videoframe(self):
		self.frames = []
		self.slider_cv2.setValue(0)
		self.set_video_position()
		while self.cap.isOpened():
			ret, frame = self.cap.read()
			if ret:
				self.frames.append(frame)
				print("Loading frame: ", len(self.frames))
			else:
				break
		print("End loading")
		self.button_playpause.setEnabled(True)
		self.cap.release()
		cv2.destroyAllWindows()
		self.slider_cv2.setRange(0, len(self.frames) - 1)
		self.process_frames_temp()
	
	def show_videoframe(self):
		if len(self.frames) == 0:
			return
		frame = self.frames[self.slider_cv2.value()]
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		# frame = cv2.resize(frame, (self.label.size().width(), self.label.size().height()), interpolation=cv2.INTER_CUBIC)
		if self.isgtbox:
			box_info = self.gt_box[self.slider_cv2.value()]
			bx, by, bw, bh = list(map(lambda x: int(x), box_info.replace(" ", "").split(",")))
			frame = cv2.rectangle(frame, (bx - int(0.5 * bw), by - int(0.5 * bh)),
								  (bx + int(0.5 * bw), by + int(0.5 * bh)), (0, 0, 255), 3)
		h, w, ch = frame.shape
		frame = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
		frame = QPixmap(frame)
		frame = frame.scaled(self.label.size().width(), self.label.size().height(), QtCore.Qt.KeepAspectRatio)
		self.label.setPixmap(frame)

	def stop_timer(self):
		self.timer.stop()
		self.player.pause()
	
	def process_frames_temp(self):
		values = np.random.randint(0, 2, len(self.frames))
		values = values * 0.1 + 0.7
		self.ax = self.fig.add_subplot(111)
		self.ax.clear()
		self.ax.plot(values, marker="o", markevery=[0], markerfacecolor='red')
		self.ax.plot(values, lw=0.0, marker="o", markevery=[0], mec='red', mew=0.1, mfc=(1, 1, 0, 0.5))
		self.ax.set_xlabel("frame")
		self.ax.set_ylabel("confidence")
		self.ax.set_title("TEMP graph")
		self.ax.set_ylim([0., 1.])
		# ax.legend()
		self.fig.tight_layout()
		self.canvas.draw()
		# self.canvas.isgraph = True
		self.fig.canvas.mpl_connect('motion_notify_event', self.plt_move_event)
		self.fig.canvas.mpl_connect('button_press_event', self.plt_bpress_event)
	
	def set_point_on_graph(self):
		slider_pos = self.slider_cv2.value()
		self.ax.lines[0].set_markevery([slider_pos])
		# self.canvas.slider_pos = self.slider_cv2.value()
		self.canvas.draw()
	
	def slider_released(self):
		if self.isplaying:
			self.timer.start(self.spf)
			self.player.play()
		else:
			self.timer.stop()
			self.player.pause()
		self.show_videoframe()
		self.set_video_position()
	
	def toggle_gtbox(self):
		if self.isgtbox:
			self.isgtbox = False
		else:
			self.isgtbox = True
		self.show_videoframe()
	
	def resize_widget(self, widget, mode, ratio):
		if mode == 'width':
			widget.resize(int(self.size().width() * ratio), widget.geometry().height())
		elif mode == 'height':
			widget.resize(widget.geometry().width(), int(self.size().height() * ratio))
		else:
			try:
				widget.resize(int(self.size().width() * ratio[0]), int(self.size().height() * ratio[1]))
			except AttributeError:
				widget.setGeometry(QtCore.QRect(widget.geometry().left(), widget.geometry().top(), int(self.geometry().width() * ratio[0]), int(self.geometry().height() * ratio[1])))
	
	def plt_move_event(self, e):
		# xs, _ = self.ax.transData.transform_point([0, 0])
		# xe, _ = self.ax.transData.transform_point([len(self.frames), 0])
		if e.xdata is not None:
			if e.xdata > 0 and e.xdata < len(self.frames) - 1:
				# x = trans_x_to_ax(e.x, int(xs), int(xe), len(self.frames) - 1)
				self.ax.lines[1].set_markevery([round(e.xdata)])
				self.canvas.draw()
			elif e.xdata < 0:
				self.ax.lines[1].set_markevery([0])
				self.canvas.draw()
			else:
				self.ax.lines[1].set_markevery([len(self.frames) - 1])
				self.canvas.draw()
		# print("E:", e.xdata)
	
	def plt_bpress_event(self, e):
		# print("B:", e.x, e.xdata)
		if e.xdata is not None:
			if e.xdata > 0 and e.xdata < len(self.frames):
				self.slider_cv2.setValue(round(e.xdata))
				# print(round(e.xdata))
			elif e.xdata < 0:
				self.slider_cv2.setValue(0)
			else:
				self.slider_cv2.setValue(len(self.frames) - 1)
				self.isplaying = False
				self.timer.stop()
			# if self.player.state() == 0:
			# 	self.player.play()
			self.set_video_position()




# class widget(QtWidgets.QWidget):
# 	def __init__(self, parent):
# 		super(widget, self).__init__(parent=parent)
# 		self.setMouseTracking(True)
	
# 	def mouseMoveEvent(self, event):
# 		print(event.x(), event.y())
	
	# def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
	# 	return super().mousePressEvent(a0)


# class Canvas(FigureCanvas):
# 	def __init__(self, figure):
# 		super(Canvas, self).__init__(figure=figure)
# 		self.isgraph = False
# 		self.slider_pos = None
	
# 	def mouseMoveEvent(self, event):
# 		# return super().mouseMoveEvent(event)
# 		# print(event.x(), event.y())
# 		if self.isgraph:
# 			x = event.x()
# 			self.figure.axes[0].lines[0].set_markevery([self.slider_pos, x])
# 			self.draw()

def trans_x_to_ax(x, start, end, _len):
	ratio = _len / (end - start)
	return (x - start) * ratio


if __name__ == "__main__":
	window = UI()
	app.exec_()
