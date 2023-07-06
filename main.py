#---Imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint
from collections import deque

g = 9.81

class Simple_pendulum (Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()        

    def Anim (self, i):
        thisx = [0, self.L*np.sin(self.pos[i])]
        thisy = [0, -self.L*np.cos(self.pos[i])]
        if i == 0:
            self.history_x.clear()
            self.history_y.clear()

        self.history_x.appendleft(thisx[1])
        self.history_y.appendleft(thisy[1])

        self.line.set_data(thisx, thisy)
        self.trace.set_data(self.history_x, self.history_y)
        return self.line, self.trace


    def Animate (self):
        def theta_derivative (x, t, L):
            return [x[1], (-g/L)*np.sin(x[0])]
        self.a = float(self.textAngle.get())
        self.L = float(self.textLength.get())
        L = float(self.textLength.get())
        time = float(self.textTime.get())
        self.t = np.arange(0, time, 0.01)  
        self.history_x, self.history_y = deque(maxlen=len(self.t)), deque(maxlen=len(self.t))
        y0 = [(self.a)*(2*np.pi/360), 0.0]
        self.pos, self.vel = odeint(theta_derivative, y0 , self.t, args = (L,)).T  
        self.ax.set_xlim(-(self.L + 1), self.L + 1)
        self.ax.set_ylim(-(self.L + 1), self.L + 1)
        self.canvas.draw()
        frames = len(self.t)
        self.ani = animation.FuncAnimation(self.fig, self.Anim, frames, blit=False, interval = 1)
        self.canvas.draw()

    def Clear(self):
        self.canvas.get_tk_widget().forget()
        self.ani.event_source.stop()
        self.history_x.clear()
        self.history_y.clear()


    def init_window(self):
        self.master.title("Simple pendulum")
        self.pack(fill='both', expand=1)

        self.labelAngle = Label(self, text = "Angle (º)", width=12)
        self.labelAngle.grid(row=1, column=1)
        self.labelLength = Label(self, text = "Length (m)", width=12)
        self.labelLength.grid(row=1, column=2)
        self.labelTime = Label(self, text = "Time (s)", width=12)
        self.labelTime.grid(row=1, column=3)
        
        self.textAngle = Entry(self, width=12)
        self.textAngle.grid(row=2, column=1)
        self.textLength = Entry(self, width=12)
        self.textLength.grid(row=2, column=2)
        self.textTime = Entry(self, width=12)
        self.textTime.grid(row=2, column=3)

        self.textAngle.insert(0, "45.0")
        self.textLength.insert(0, "1.0")
        self.textTime.insert(0, "5.0")
        self.a = 45.0
        self.L = 1.0  
        self.t = np.arange(0, 5, 0.001)    
        
        self.buttonAnimate = Button(self, text="Animate", command=self.Animate, width=12)
        self.buttonAnimate.grid(row=2, column=4)  
        self.buttonClear = Button(self, text="Clear", command=self.Clear, width=12)
        self.buttonClear.grid(row=2, column=5)  

        self.fig = plt.figure(figsize=(5, 5))    
        self.ax = self.fig.add_subplot(111)  

        self.line, = self.ax.plot([], [], 'o-', lw=2)
        self.trace, = self.ax.plot([], [], '.-', lw=1, ms=2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=1,row=4, columnspan=2) 

root = Tk()
root.geometry("1200x600")
app = Simple_pendulum(root)
mainloop()