#!/usr/bin/env python

import rospy
from  math import *
import rospkg
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from scipy import integrate
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from modern_control.msg import motion_model_dp
from modern_control.msg import iter_info

G = 9.8  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
M1 = 1.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg

# th1 and th2 are the initial angles (degrees)
# w10 and w20 are the initial angular velocities (degrees per second)
th1 = 20
w1 = 0.0
th2 = 60.0
w2 = 0.0

def derivs(state, t):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    del_ = state[2] - state[0]
    den1 = (M1 + M2)*L1 - M2*L1*cos(del_)*cos(del_)
    dydx[1] = (M2*L1*state[1]*state[1]*sin(del_)*cos(del_) +
               M2*G*sin(state[2])*cos(del_) +
               M2*L2*state[3]*state[3]*sin(del_) -
               (M1 + M2)*G*sin(state[0]))/den1

    dydx[2] = state[3]

    den2 = (L2/L1)*den1
    dydx[3] = (-M2*L2*state[3]*state[3]*sin(del_)*cos(del_) +
               (M1 + M2)*G*sin(state[0])*cos(del_) -
               (M1 + M2)*L1*state[1]*state[1]*sin(del_) -
               (M1 + M2)*G*sin(state[2]))/den2

    return dydx

# initial state
state = np.radians([th1, w1, th2, w2])

# create a time array from 0..100 sampled at 0.05 second steps
dt = 0.5
time_end = 20
t = np.arange(0.0, time_end, dt)
        
if __name__ == '__main__':
    rospy.init_node('motion_model_dp', anonymous=True)
    x_new = integrate.odeint(derivs, state, t)
    a = x_new.shape
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
	for i in xrange(0, int(time_end/dt-1)):
		out = motion_model()
		out2 = iter_info()
		out.theta1 = x_new[:,0].item(i)
		out.theta1dot = x_new[:,1].item(i)
		out.theta2 = x_new[:,2].item(i)
		out.theta2dot = x_new[:,3].item(i)
		out2.dt = dt
		out2.end_time = time_end
		out2.i = i
		pub1 = rospy.Publisher('/states_dp', motion_model, queue_size = 15)
		pub2 = rospy.Publisher('/iter_inform', iter_info, queue_size = 15)
		pub1.publish(out)
		pub2.publish(out2)
		r.sleep()
    rospy.loginfo("Motion model Node Has Shutdown.")
    rospy.signal_shutdown(0)



