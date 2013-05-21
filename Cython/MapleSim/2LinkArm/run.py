# Written by Travis DeWolf (May, 2013)
import numpy as np
import pyglet
import time

import py2LinkArm

def run(): 
    """Runs and plots a 2 link arm simulation generated by MapleSim."""

    # set up input control signal to simulation
    u = np.ones(2) * .1 
    # set up array to receive output from simulation
    out = np.zeros(3) 

    # create MapleSim sim class 
    sim = py2LinkArm.pySim() 
    # set up initial conditions of the system
    sim.reset(out) 

    ###### Plotting things

    # segment lengths = (.31, .27)m (defined in MapleSim)
    L = np.array([31, 27]) * 3

    # make our window for drawin'
    window = pyglet.window.Window()

    # set up some labels to display time 
    label_time = pyglet.text.Label('time', font_name='Times New Roman', 
        font_size=36, x=window.width//2, y=window.height - 50,
        anchor_x='center', anchor_y='center')
    # and joint angles
    label_values = pyglet.text.Label('values', font_name='Times New Roman', 
        font_size=36, x=window.width//2, y=window.height - 100,
        anchor_x='center', anchor_y='center')

    def update_arm(dt):
        """ Simulate the arm ahead a chunk of time, then find the 
        (x,y) coordinates of each joint, and update labels."""
   
        # simulate arm forward 15ms
        for i in range(1500):
            sim.step(out, u)

        # find new joint (x,y) coordinates, offset to center of screen-ish
        x = np.array([ 0, 
            L[0]*np.cos(out[1]),
            L[0]*np.cos(out[1]) + L[1]*np.cos(out[1]+out[2])]) + window.width/2
        y = np.array([ 0, 
            L[0]*np.sin(out[1]),
            L[0]*np.sin(out[1]) + L[1]*np.sin(out[1]+out[2])]) + 100

        # update line endpoint positions for drawing
        window.jps = np.array([x, y]).astype('int')
        label_time.text = 'time: %.3f'%out[0]
        label_values.text = '(01, 02) = (%.2f, %.2f)'%(out[1], out[2])
 
    update_arm(0) # call once to set up

    @window.event
    def on_draw():
        window.clear()
        label_time.draw()
        label_values.draw()
        for i in range(2): 
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', 
                (window.jps[0][i], window.jps[1][i], 
                 window.jps[0][i+1], window.jps[1][i+1])))

    # set up update_arm function to be called super often
    pyglet.clock.schedule_interval(update_arm, 0.00001)
    pyglet.app.run()

run()
