import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation
#Global variables

max=15000 #limit
n=f=0
G=6.67348e-11 # Gravitational constant
dt=86400    #time step, 86400s/1 day

#energy and time variable initiation
E=[]
ttime=[]
years=[]
ttime.append(0)
years.append(0)

#Dictionary of all planets with matrices set up for the variables that change
planets = {
    'Sun':  {
    'mass':1.989e30,
    'radius':np.zeros([2,max]),
    'force':[],
    },
    'Mercury':  {
    'mass':3.285e23,
    'radius':np.zeros([2,max]),
    'velocity':np.zeros([2,max]),
    'force':[],
    },
    'Venus':  {
    'mass':4.87e24,
    'radius':np.zeros([2,max]),
    'velocity':np.zeros([2,max]),
    'force':[],
    },
    'Earth':  {
    'mass':5.972e24,
    'radius':np.zeros([2,max]),
    'velocity':np.zeros([2,max]),
    'force':[],
    },
    'Mars':  {
    'mass':6.39e23,
    'radius':np.zeros([2,max]),
    'velocity':np.zeros([2,max]),
    'force':[],
    },
    'Jupiter':  {
    'mass':1.9e27,
    'radius':np.zeros([2,max]),
    'velocity':np.zeros([2,max]),
    'force':[],
    },
    'Saturn':  {
    'mass':5.69e26,
    'radius':np.zeros([2,max]),
    'velocity':np.zeros([2,max]),
    'force':[],
    },
    }   
    
#Initial velocity and position values for all planets
planets['Mercury']['radius'][0,0] = 57.9e9
planets['Mercury']['velocity'][1,0] = 47400
planets['Venus']['radius'][0,0] = 108.2e9
planets['Venus']['velocity'][1,0] = -35000
planets['Earth']['radius'][0,0] = 149.59787e9
planets['Earth']['velocity'][1,0] = 29800
planets['Mars']['radius'][0,0] = 228.9e9
planets['Mars']['velocity'][1,0] = 24100
planets['Jupiter']['radius'][0,0] = 778.6e9
planets['Jupiter']['velocity'][1,0] = 13100
planets['Saturn']['radius'][0,0] = 1433e9
planets['Saturn']['velocity'][1,0] = 9600


#Force, updated velocity and updaated position functions

def force(mass1,radius1,mass2,radius2,n):
    r=math.sqrt(((radius2[0,n]-radius1[0,n])**2)+((radius2[1,n]-radius1[1,n])**2))
    force=-(G*mass2*mass1/(r**2)) * ((radius1[:,n]-radius2[:,n])/np.linalg.norm(radius1[:,n]-radius2[:,n]))
    return force    
    
def velocity1(velocity,force, mass,dt,n):
    velocity1=velocity[:,n]+(((force[n])/(mass))*dt)
    return velocity1
    
def position(radius, velocity,dt,n):
    position=radius[:,n]+(velocity[:,n+1]*dt)
    return position
    
#energy calculation for the system
def energy(msun,mass,radius,n,velocity,radius1):
    r=math.sqrt(((radius1[0,n]-radius[0,n])**2)+((radius1[1,n]-radius[1,n])**2))
    velocityt=math.sqrt(velocity[0,n]**2+velocity[1,n]**2)    
    energy=0.5*mass*velocityt**2-((G*msun*mass)/r)
    return energy
#calculation of in simulation time period in days and then years
def days(ttime):
    dtime=ttime[n]+1
    return dtime
def year(ttime,years):
    if ttime[n+1]%360==0:
        ttime[n+1]=0
        ytime=years[n]+1
    else:
        ytime=years[n]
    return ytime
 
#loop for a number n to the limit set above
while n<max-1:
    #total force from all planets calculation
    for x in planets:
        if x!='Sun':    #for x in planets, so long as it doesnt equal the Sun
            totalforce=0
            for y in planets:
                if x!=y:
                    totalforce+=force(planets[x]['mass'],planets[x]['radius'],planets[y]['mass'],planets[y]['radius'],n)
            planets[x]['force'].append(totalforce)
    #for x in planets calculate the new velocity and positions from the total force
    for x in planets:
        if x!='Sun':
            planets[x]['velocity'][:,n+1]=velocity1(planets[x]['velocity'],planets[x]['force'],planets[x]['mass'],dt,n)
            planets[x]['radius'][:,n+1]=position(planets[x]['radius'],planets[x]['velocity'],dt,n)
    #calculate the energy of the Sun-Earth system
    E.append(energy(planets['Sun']['mass'],planets['Earth']['mass'],planets['Earth']['radius'],n,planets['Earth']['velocity'],planets['Sun']['radius']))
    #increase the time variable by a day, which is dt
    ttime.append(days(ttime))
    years.append(year(ttime,years))
    n+=1
    
#animation (taken from=> https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/)
fig = plt.figure()
ax = fig.add_subplot(111,aspect='equal',xlim=(-150e10, 150e10), ylim=(-150e10, 150e10))
#initialise where the time and energy text will appear
time_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
energy_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
#initialise the planet animation variables, some got colours to make them easier to see
sun, = ax.plot([], [], 'oy')
mercury, = ax.plot([], [], 'ow')
venus, = ax.plot([], [], 'og')
earth, = ax.plot([], [], 'ob')
mars, = ax.plot([], [], 'or')
jupiter, = ax.plot([], [], 'o')
saturn, = ax.plot([], [], 'o')

# initialization function: wipes the plot, then replot the background of each frame, including plot lines to
# make it easier to see the orbits
def init():
    energy_text.set_text('')
    time_text.set_text('')
    #place a dot at (0,0) so the Sun can always be seen
    sun.set_data(planets['Sun']['radius'][0,0],planets['Sun']['radius'][1,0])
    #initialise the data sets for each planet as blank arrays to wipe the dots
    mercury.set_data([], [])
    venus.set_data([], [])
    earth.set_data([], [])
    mars.set_data([], [])
    jupiter.set_data([], [])
    saturn.set_data([], [])
    #plot the orbits of the planets on the background so they stay after each wipe
    plt.plot(planets['Mercury']['radius'][0,:],planets['Mercury']['radius'][1,:])
    plt.plot(planets['Venus']['radius'][0,:],planets['Venus']['radius'][1,:])
    plt.plot(planets['Earth']['radius'][0,:],planets['Earth']['radius'][1,:])
    plt.plot(planets['Mars']['radius'][0,:],planets['Mars']['radius'][1,:])
    plt.plot(planets['Jupiter']['radius'][0,:],planets['Jupiter']['radius'][1,:])
    plt.plot(planets['Saturn']['radius'][0,:],planets['Saturn']['radius'][1,:])
    return energy_text,time_text,mercury,venus,earth,mars,jupiter,saturn,

# animation function.  This is called sequentially
def animate(i):
    #print the energy and time passed at each interval
    energy_text.set_text('energy = %.0f J' % E[i])
    time_text.set_text('time = %.0f year(s) and %.0f days' % (years[i],ttime[i]))
    #plot the dots at each planets new position
    mercury.set_data(planets['Mercury']['radius'][0,i],planets['Mercury']['radius'][1,i])
    venus.set_data(planets['Venus']['radius'][0,i],planets['Venus']['radius'][1,i])
    earth.set_data(planets['Earth']['radius'][0,i],planets['Earth']['radius'][1,i])
    mars.set_data(planets['Mars']['radius'][0,i],planets['Mars']['radius'][1,i])
    jupiter.set_data(planets['Jupiter']['radius'][0,i],planets['Jupiter']['radius'][1,i])
    saturn.set_data(planets['Saturn']['radius'][0,i],planets['Saturn']['radius'][1,i])
    return mercury,venus,earth,mars,jupiter,saturn,energy_text,time_text,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=max, interval=20, blit=True)
plt.xlabel('Meters')
plt.ylabel('Meters')

plt.show()