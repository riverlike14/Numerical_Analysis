import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

################################################################################################

a, b = 0, 50
h = 0.001
init_cond = (5, 5, 5)

################################################################################################

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-20, 20), ylim=(0, 50))
ax.grid()

mass, = ax.plot([], [], 'o', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

################################################################################################

def RK4(f, a, b, h, y_0):
    n = int((b - a)/h)
    d = len(y_0)
    
    t = np.linspace(a, b, n+1)
    w = np.zeros((d, n+1))
    w[:, 0] = y_0
    
    for i in range(n):
        s_1 = f(t[i], w[:, i])
        s_2 = f(t[i] + h/2, w[:, i] + s_1*h/2)
        s_3 = f(t[i] + h/2, w[:, i] + s_2*h/2)
        s_4 = f(t[i] + h, w[:, i] + s_3*h)        
        
        w[:, i+1] = w[:, i] + (s_1 + 2*s_2 + 2*s_3 + s_4)*h/6
        
    return t, w

################################################################################################

def Lorenz(t, xyz):
    x, y, z = xyz
    s = 10
    r = 28
    b = 8/3
    
    x_ = -s*x + s*y
    y_ = -x*z + r*x - y
    z_ = x*y - b*z
    
    return np.array([x_, y_, z_])

t, w = RK4(Lorenz, a, b, h, init_cond)
x, y, z = w

################################################################################################

def init():
    mass.set_data([], [])
    time_text.set_text('')
    return mass, time_text

def animate(i):
    thisx = [x[i]]
    thisz = [z[i]]
    
    mass.set_data(thisx, thisz)
    time_text.set_text(time_template % (i*h))
    return mass, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, int((b - a)/h)),
                              interval=5, blit=True, init_func=init)

plt.show()