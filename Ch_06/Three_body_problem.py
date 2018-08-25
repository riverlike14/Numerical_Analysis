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

mass, = ax.plot([], [], 'o', lw=2)
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

m1 = 1
m2 = 1
m3 = 1
g = 1

y_01 = (-0.970, 0.243) + (-0.466, -0.433)
y_02 = (0.970, -0.243) + (-0.466, -0.433)
y_03 = (0, 0) + (0.932, 0.866)
y_0 = y_01 + y_02 + y_03

def f(t, y):
    x1, y1, v1x, v1y, x2, y2, v2x, v2y , x3, y3, v3x, v3y = y
    
    P1 = (x1, y1, m1)
    P2 = (x2, y2, m2)
    P3 = (x3, y3, m3)
    
    def force(P1, P2, position):
        x1, y1, m1 = P1
        x2, y2, m2 = P2
        if position == 'x':
            return g*m2*(x2 - x1) / sqrt((x2 - x1)**2 + (y2 - y1)**2)**3
        elif position == 'y':
            return g*m2*(y2 - y1) / sqrt((x2 - x1)**2 + (y2 - y1)**2)**3
    
    f1 = [v1x, v1y, force(P1, P2, 'x') + force(P1, P3, 'x'), force(P1, P2, 'y') + force(P1, P3, 'y')]
    f2 = [v2x, v2y, force(P2, P3, 'x') + force(P2, P1, 'x'), force(P2, P3, 'y') + force(P2, P1, 'y')]
    f3 = [v3x, v3y, force(P3, P1, 'x') + force(P3, P2, 'x'), force(P3, P1, 'y') + force(P3, P2, 'y')]
    
    return np.array(f1 + f2 + f3)

t, y = Trapezoid_method(f, a, b, h, y_0)
x1, y1, _, _, x2, y2, _, _, x3, y3, _, _ = y

################################################################################################

def init():
    mass.set_data([], [])
    time_text.set_text('')
    return mass, time_text

def animate(i):
    thisx = [x1[i], x2[i], x3[i]]
    thisy = [y1[i], y2[i], y3[i]]
    
    mass.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*h))
    return mass, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, int((b - a)/h)),
                              interval=5, blit=True, init_func=init)

plt.show()