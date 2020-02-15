import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import random


class gaugeApp:

	def __init__(self, frame, min, max, title):
		self.img = ImageTk.PhotoImage(file='gauge_background.png') 				# Load the background image
		self.width, self.height = self.img.width(), self.img.height()							# Get the width and height
		self.title = title
		self.make_gauge()


	def polar2cartesian(self, theta):
		'''
		Convert a given angle to x-y coordinates of the tip of the dial
		Return: x-y coordinates
		'''
		x2 = 150 + 90*np.cos(theta)
		y2 = 150 + 90*np.sin(theta)
		return x2, y2


	def map(self, number):
		'''
		Convert a number from 0 to 100, to 0.75*np.pi to 2.25*np.pi
		Return: the required angle
		'''
		slope = (2.25*np.pi - 0.75*np.pi)/(90 - 0)
		angle = slope*(number-0) + 0.75*np.pi
		return angle

	def make_gauge(self):
		self.canvas = tk.Canvas(root, width=self.width, height=self.height) 				# Create the canvas, for the gauge
		self.canvas.pack()														# Pack the canvas
		background = self.canvas.create_image(150, 150, image=self.img) 				# Load the image on the canvas
		x2,y2 = self.polar2cartesian(self.map(0))
		self.canvas.create_oval(140,140,160,160, fill='red')
		self.canvas.create_text(150, 180, 
				fill="white", 
				font=("Purisa", 12), 
				text=self.title)
		self.line = self.canvas.create_line(150,150,x2,y2, fill="red", width=3) 	# Create the dial line

		# Add the numbers
		for i in range(10): 	
			label = i*10
			x2, y2 = self.polar2cartesian(self.map(label))
			self.canvas.create_text(x2, y2, 
				fill="white", 
				font=("Purisa", 12), 
				text=str(label))

	def set_dial(self, value):
		'''
		Method to set the dial line to some value
		'''
		x2,y2 = self.polar2cartesian(self.map(value))
		self.canvas.coords(self.line, 150, 150, x2,y2)
		return None


if __name__ == '__main__':

	root = tk.Tk()

	gauge_frame1 = tk.Frame(root)
	gauge_frame1.pack()
	mygauge1 = gaugeApp(gauge_frame1, 0, 100, "speed")
	#mygauge.set_dial(50)
	#root.after(2000,lambda: mygauge1.set_dial( random.randint(0,90) ))

	gauge_frame2 = tk.Frame(root)
	gauge_frame2.pack()
	mygauge2 = gaugeApp(gauge_frame2, 0, 100, "rpm")
	#mygauge.set_dial(50)
	#root.after(2000,lambda: mygauge2.set_dial( random.randint(0,90) ))


	def update():
		mygauge1.set_dial( random.randint(0,90) )
		mygauge2.set_dial( random.randint(0,90) )
		root.after(1000, update)

	root.after(1000, update)

	root.mainloop()