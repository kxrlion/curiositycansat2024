from math import pi, sqrt , log
from subprocess import list2cmdline
import matplotlib.pyplot as plt
import matplotlib.animation as animation


from time import time
from time import sleep
from urllib.request import urlopen
from matplotlib import style


style.use('fivethirtyeight')

fig = plt.figure()
ax1=fig.add_subplot(1,3,1)
ax2=fig.add_subplot(1,3,2)
ax3=fig.add_subplot(1,3,3)



euler = 2.71828182845904523536
p0 = 1007.75
R = 8.314462
u = 0.0289644
g = 9.81

def animate(i):
    graph_data = open('b90-105.txt','r').read()
    lines=graph_data.split('\n')
    xs=[]
    ax1s=[]
    ax2s=[]
    ax3s=[]
    ax4s=[]
    ax5s=[]
    ax6s=[]
    ax7s=[]
    for line in lines:
        if len(line)>1:
            x,ax1v,ax2v,ax3v,ax4v,ax5v,ax6v,ax7v,ax8v,ax9v=line.split(';')
            xs.append(float(x)-550)
            ax1s.append(float(ax1v))
            ax2s.append(float(ax2v))
            ax3s.append((log( float(ax1s[len(ax1s)-1]) / p0 ) * R * float( ax2s[len(ax2s)-1] +273.15 )) / (-1*u*g))
            ax4s.append(ax3v)
            ax4s.append(ax4v)
            ax5s.append(ax5v)
            ax6s.append(ax6v)
            ax7s.append(ax7v)
            ax7s.append(ax8v)
            ax7s.append(ax9v)
    
    ax1.clear()
    ax1.set_title("Temperature T(p)")
    ax1.plot(ax1s,ax2s)
    
    ax2.clear()
    ax2.set_title("Temperature T(h)")
    ax2.plot(ax3s,ax2s)
    
    ax3.clear()
    ax3.set_title("Height p(h)")
    ax3.plot(ax3s,ax1s)

    #ax1.set_title("Temperature T(p)")
    #ax1.plot(ax1s,ax2s)

    #ax2.set_title("Temperature T(h)")
    #ax2.plot(ax8s,ax2s)

    #ax3.set_title("Pressure p(h)")
    #ax3.plot(ax8s,ax1s)
ani = animation.FuncAnimation(fig,animate,interval = 1000)
plt.show()
