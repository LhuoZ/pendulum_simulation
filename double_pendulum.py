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

class Double_pendulum (Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def Anim (self, i):
        thisx = [0, self.L1*np.sin(self.pos_1[i]), self.L1*np.sin(self.pos_1[i])+self.L2*np.sin(self.pos_2[i])]
        thisy = [0, -self.L1*np.cos(self.pos_1[i]), -self.L1*np.cos(self.pos_1[i])-self.L2*np.cos(self.pos_2[i])]
        if i == 0:
            self.history_x.clear()
            self.history_y.clear()

        self.history_x.appendleft(thisx[2])
        self.history_y.appendleft(thisy[2])

        self.line.set_data(thisx, thisy)
        self.trace.set_data(self.history_x, self.history_y)
        return self.line, self.trace

    def Animate (self):
        # Get initial conditions
        self.m1 = float(self.textMass1.get())
        self.m2 = float(self.textMass2.get())
        self.L1 = float(self.textLength1.get())
        self.L2 = float(self.textLength2.get())
        self.a1 = float(self.textAngle1.get())*np.pi/180
        self.a2 = float(self.textAngle2.get())*np.pi/180

        self.time = float(self.textTime.get())
        self.t = np.arange(0, self.time, 0.02)

        self.history_x, self.history_y = deque(maxlen=len(self.t)), deque(maxlen=len(self.t))

        def derivative (x, t):
            """Return the first derivatives of y = theta1, z1, theta2, z2."""
            theta1, z1, theta2, z2 = x

            c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

            theta1dot = z1
            z1dot = (self.m2*g*np.sin(theta2)*c - self.m2*s*(self.L1*z1**2*c + self.L2*z2**2) - (self.m1+self.m2)*g*np.sin(theta1)) / self.L1 / (self.m1 +self.m2*s**2)
            theta2dot = z2
            z2dot = ((self.m1+self.m2)*(self.L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + self.m2*self.L2*z2**2*s*c) / self.L2 / (self.m1 + self.m2*s**2)
            return theta1dot, z1dot, theta2dot, z2dot
        
        y = odeint(derivative, [self.a1, 0, self.a2, 0], self.t)

        self.pos_1, self.pos_2 = y[:,0], y[:,2]

        r = 1

        self.ax.set_xlim(-(self.L1 + self.L2+r), self.L1 + self.L2+r)
        self.ax.set_ylim(-(self.L1 + self.L2+r), self.L1 + self.L2+r)

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
        self.master.title("Double pendulum")
        self.pack(fill='both', expand=1)

        self.labelAngle1 = Label(self, text = "Angle mass 1 (º)", width = 20)
        self.labelAngle1.grid(row=1, column=0)
        self.labelLength1 = Label(self, text = "Length mass 1 (m)", width = 20)
        self.labelLength1.grid(row=1, column=2)
        self.labelMass1 = Label(self, text = "Mass 1 (kg)", width = 20)
        self.labelMass1.grid(row=1, column=4)

        self.labelAngle2 = Label(self, text = "Angle mass 2(º)", width = 20)
        self.labelAngle2.grid(row=2, column=0)
        self.labelLength2 = Label(self, text = "Length mass 2(m)", width = 20)
        self.labelLength2.grid(row=2, column=2)
        self.labelMass2 = Label(self, text = "Mass 2(kg)", width = 20)
        self.labelMass2.grid(row=2, column=4)

        self.textAngle1 = Entry(self, width=20)
        self.textAngle1.grid(row=1, column=1)
        self.textLength1 = Entry(self, width=20)
        self.textLength1.grid(row=1, column=3)
        self.textMass1 = Entry(self, width=20)
        self.textMass1.grid(row=1, column=5)

        self.textAngle2 = Entry(self, width=20)
        self.textAngle2.grid(row=2, column=1)
        self.textLength2 = Entry(self, width=20)
        self.textLength2.grid(row=2, column=3)
        self.textMass2 = Entry(self, width=20)
        self.textMass2.grid(row=2, column=5)

        self.textTime = Label(self, text = "Time (s)",width=20)
        self.textTime.grid(row=3, column=0)
        self.textTime = Entry (self, width = 20)
        self.textTime.grid(row=3, column=1)

        self.textAngle1.insert(0, "45.0")
        self.textLength1.insert(0, "1.0")
        self.textAngle2.insert(0, "45.0")
        self.textLength2.insert(0, "1.0") 
        self.textMass1.insert(0, "1.0")
        self.textMass2.insert(0, "1.0") 
        self.textTime.insert(0, "15.0")
        self.a1 = 45.0
        self.L1 = 1.0  
        self.a2 = 45.0
        self.L2 = 1.0 
        self.m1 = 1.0
        self.m2 = 1.0 
        self.t = np.arange(0, 15, 0.02)  

        self.buttonAnimate = Button(self, text="Animate", command=self.Animate, width=20)
        self.buttonAnimate.grid(row=4, column=4)  
        self.buttonClear = Button(self, text="Clear", command=self.Clear, width=20)
        self.buttonClear.grid(row=4, column=5)  

        self.fig = plt.figure(figsize=(5, 5))    
        self.ax = self.fig.add_subplot(111)  

        self.line, = self.ax.plot([], [], 'o-', lw=2)
        self.trace, = self.ax.plot([], [], '.-', lw=1, ms=2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=0,row=5, columnspan=5) 

root = Tk()
root.geometry("1000x600")
app = Double_pendulum(root)
mainloop()