import tkinter as tk 
from tkGauge import *
import random

# Create a tkinter root
root = tk.Tk()

# Create 2 frames and pack them
frame1 = tk.LabelFrame(root, text='hello')
frame1.pack(side=tk.RIGHT)

frame2 = tk.Frame(root)
frame2.pack(side=tk.RIGHT)

# And now create 2 gauges
gauge1 = GaugeWidget(frame1)
gauge2 = GaugeWidget(frame2,
	Vmin=40,
	Vmax=300,
	title="SPEED",
	size=400,
	value=110)

def update():
	'''
	Function that updates the charts with random values.
	'''
	gauge1.set_dial( random.randint(gauge1.Vmin, gauge1.Vmax) )
	gauge2.set_dial( random.randint(gauge2.Vmin, gauge2.Vmax) )
	root.after(1000, update)

root.after(1000, update)

root.mainloop()