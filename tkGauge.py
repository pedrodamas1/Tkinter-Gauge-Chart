import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import random
from scipy.interpolate import interp1d


class GaugeWidget:
	'''
	A gauge chart widget for tkinter projects. Gauge charts have the following properties:

	Attributes:
		master: A tkinter widget class (root, frame, or labelframe) where the gauge will be placed.
	Optional:
		Vmin: An int to use as the minimum value on the gauge chart (default is 0).
		Vmax: An int to use as the minimum value on the gauge chart (default is 90).
		title: A string to use as label to the gauge chart.
		size: An int to  (Default is 300)
		value: A float that holds the value of the gauge dial (default is 0, or min).
	'''


	########################################################################## INITIALIZE
	def __init__(self, master, *args, **kwargs):
		'''
		Initialize the gauge
		'''

		############################### BACKGROUND IMAGE

		# Load the image for the background
		image = Image.open('Images/template.png')
		# Get the width and height of the original image
		width, height = image.size

		############################### KWARGS VARIABLES	

		# Tkinter widget where the gauge chart will be placed
		self.master  = master
		# Minimum value for the chart
		self.Vmin = kwargs.pop('Vmin', 0)
		# Maximum value for the chart
		self.Vmax = kwargs.pop('Vmax', 90)
		# Title for the chart
		self.title = kwargs.pop('title', '')
		# Size for the chart
		size = kwargs.pop('size', width)
		# Initial value for the dial
		self.value = kwargs.pop('value', self.Vmin)

		############################### IMAGE RESIZING

		# Load the background image for the gauge chart
		image = image.resize((size, size), Image.ANTIALIAS)
		# Load the image as a tkinter object
		self.img = ImageTk.PhotoImage(image)
		# Get the centre position of the background image
		self.x, self.y = size/2, size/2
		# Define the dial length
		self.dial_length = int(0.3*size)

		############################### CREATE CANVAS AND CHART

		# Create an interpolation object. Could also use numpy.interp(x, [x1,y1], [x2,y2])
		self.map = interp1d([self.Vmin, self.Vmax], [0.75*np.pi, 2.25*np.pi])

		# Create the canvas, for the gauge
		self.canvas = tk.Canvas(self.master, 
			width=size, 
			height=size)
		# Pack the canvas
		self.canvas.pack()
		# Make the chart
		self.make_chart(self.canvas, 
			self.x, 
			self.y)


	########################################################################## CREATE THE GAUGE ELEMENTS
	def make_chart(self, master, x1, y1):
		'''
		Assembles the elements in the gauge chart.
		Returns: None
		'''

		# Load the image on the canvas
		master.create_image(x1, y1, 
			image=self.img)
		# Font for text
		font = ("Purisa", 12)

		# Circle at the centre of the gauge
		master.create_oval(x1-10, y1-10, x1+10, y1+10, 
			fill='red',
			width=3)

		# Title for the gauge
		master.create_text(x1, y1+30, 
			fill="white", 
			font=font, 
			text=self.title)

		# Background for the value text box
		master.create_rectangle(x1-20, y1+40, x1+20, y1+60, 
			fill='black')

		# Value of the dial
		self.value_lbl = master.create_text(x1, y1+50, 
			fill="white", 
			font=font, 
			text=self.value)

		# Numbers circling the chart
		for i in np.linspace(self.Vmin, self.Vmax, num=10): 	
			x2, y2 = self.coords(self.map(i))
			master.create_text(x2, y2, 
				fill="white", 
				font=font, 
				text=int(i))

		# Make the line for the dial
		x2, y2 = self.coords(self.map( self.value ))
		self.line = master.create_line(x1, y1, x2, y2, 
			fill="red", 
			width=3)

		return None


	########################################################################## DIAL TIP COORDINATES
	def coords(self, theta):
		'''
		Convert a given angle to x-y coordinates of the tip of the dial
		Return: x-y coordinates
		'''
		x2 = self.x + self.dial_length*np.cos(theta)
		y2 = self.y + self.dial_length*np.sin(theta)
		return x2, y2


	########################################################################## CHANGE DIAL POSITION
	def set_dial(self, value):
		'''
		Method to set the dial line to some value
		Return: None
		'''
		x2,y2 = self.coords( self.map(value) )
		self.canvas.coords(self.line, self.x, self.y, x2,y2)
		self.canvas.itemconfigure(self.value_lbl, text=value)

		return None


if __name__ == '__main__':

	root = tk.Tk()

	gauge_frame1 = tk.LabelFrame(root, text='hello')
	gauge_frame1.pack(side=tk.RIGHT)
	mygauge1 = GaugeWidget(gauge_frame1, title="speed", Vmin=20, Vmax=200, value=50)

	def update():
		mygauge1.set_dial( random.randint(mygauge1.Vmin, mygauge1.Vmax) )
		root.after(1000, update)

	root.after(1000, update)

	root.mainloop()