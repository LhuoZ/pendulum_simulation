#---Imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib as plt
import matplotlib.animation as animation
from scipy.integrate import odeint

def calculate(*args):
    if (x_coordinate_entry['state'] == 'enabled'):
        x = x_coordinate.get()
        y = y_coordinate.get()
        Theta.set(np.arctan(x/y))
        Length.set(np.sqrt(x**2+y**2))
    else:
        x = Theta.get()
        y = Length.get()
        x_coordinate.set(y*np.sin(x))
        y_coordinate.set(y*np.cos(x))


def change_coord1(*args):

    x_coordinate_entry.config(state= "enabled")
    y_coordinate_entry.config(state= "enabled")
    Theta_entry.config(state= "disabled")
    Length_entry.config(state= "disabled")
    check_cart.config(state= "disabled")
    check_polar.config(state= "enabled")
    

def change_coord2(*args):

    x_coordinate_entry.config(state= "disabled")
    y_coordinate_entry.config(state= "disabled")
    Theta_entry.config(state= "enabled")
    Length_entry.config(state= "enabled")
    check_polar.config(state= "disabled")
    check_cart.config(state= "enabled")    



root = Tk()
root.title("Simple Pendulum")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=1, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="text").grid(column=1, columnspan=5, row=1, sticky=W)

x_coordinate = DoubleVar()
x_coordinate_entry = ttk.Entry(mainframe, width = 20, textvariable = x_coordinate)
x_coordinate_entry.grid(column=3, row=5, columnspan=2, sticky=(W))
ttk.Label(mainframe, text="X coordinate").grid(column=3, row=4, columnspan=2, sticky=W)

y_coordinate = DoubleVar()
y_coordinate_entry = ttk.Entry(mainframe, width = 20, textvariable = y_coordinate)
y_coordinate_entry.grid(column=3, row=7, columnspan=2, sticky=(W))
ttk.Label(mainframe, text="Y coordinate").grid(column=3, row=6, columnspan=2, sticky=W)

Theta = DoubleVar()
Theta_entry = ttk.Entry(mainframe, width = 20, textvariable = Theta)
Theta_entry.grid(column=3, row=10, sticky=(W, E))
ttk.Label(mainframe, text="Theta").grid(column=3, row=9, sticky=W)

Length = DoubleVar()
Length_entry = ttk.Entry(mainframe, width = 20, textvariable = Length)
Length_entry.grid(column=3, row=12, sticky=(W, E))
ttk.Label(mainframe, text="Length").grid(column=3, row=11, sticky=W)

ttk.Button(mainframe, text="Play", command=calculate).grid(column=3, row=2, sticky=W)
ttk.Button(mainframe, text="Reset").grid(column=4, row=2, sticky=W)

coordenada = StringVar()
check_cart = ttk.Checkbutton(mainframe, text='Coordenadas cartesianas', variable= coordenada, onvalue= 'Cartesiana', offvalue= 'Polar', command= change_coord1)
check_cart.grid(column=3, row=3, sticky=W)
check_polar = ttk.Checkbutton(mainframe, text='Coordenadas polares', variable= coordenada, offvalue= 'Cartesiana', onvalue= 'Polar',command= change_coord2)
check_polar.grid(column=3, row=8, sticky=W)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

x_coordinate_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()

#---Constants
g = 9.81        # m/s

#---Variables (initial conditions)
m = 1           # mass in kg
x = 1           # distance to origin on x axis in meters
y = 1           # distance to origin on y axis in meters
theta = 2       # angle formed with the y axis in rad
l = 2           # length of the ideal rope in maters
t = 360         #time that the code will simulate

def theta_derivative (x, t):
    return [x[1], -(g/l)*np.sin(x[0])]

time = np.arange(0, t, 1e-3)

pos, vel = odeint(theta_derivative, [theta, 0], time).T

