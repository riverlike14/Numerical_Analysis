import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

################################################################################################

pi = np.pi
exp = np.exp
sqrt = np.sqrt
sin = np.sin
cos = np.cos
tan = np.tan

################################################################################################

a, b = 0, 100
h = 0.005
t = np.arange(a, b, h)

################################################################################################

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
ax.grid()

mass, = ax.plot([], [], '-o', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

################################################################################################

def Trapezoid_method(f, a, b, h, y_0):
    n = int((b - a)/h)
    d = len(y_0)
    
    t = np.linspace(a, b, n+1)
    w = np.zeros((d, n+1))
    w[:, 0] = y_0
    
    for i in range(n):
        w[:, i+1] = w[:, i] + (f(t[i], w[:, i]) + f(t[i] + h, w[:, i] + h*f(t[i], w[:, i])))*(h/2)
        
    return t, w

################################################################################################

d = 0.1

def f(t, y):
    y1, y2 = y
    g = 9.81
    l = 1
    return np.array([y2, -g/l*sin(y1) - d*y2])

y_0 = (pi, 1)


t, y = Trapezoid_method(f, a, b, h, y_0)
x1, y1 = y

################################################################################################

def init():
    mass.set_data([], [])
    time_text.set_text('')
    return mass, time_text

def animate(i):
    thisx = [0, sin(x1[i])]
    thisy = [0, -cos(x1[i])]

    mass.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*h))
    return mass, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, int((b - a)/h)),
                              interval=5, blit=True, init_func=init)

plt.show()