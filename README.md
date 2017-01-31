# Public_ModernControl

These are the files for implementing double pendulum using ROS and python framework. The s-function which is the motion model follows
the structure from http://matplotlib.org/examples/animation/double_pendulum_animated.html . use git clone to clone this folder in your
workspace source (src) folder and perform a catkin_make then rosmake -a outside the src folder in the workspace. Once that is sucessfully 
done, run the following commands :

1. rosrun modern_control motion_model_dp.py
in a different terminal run 
2. rosrun modern_control draw_pendulum.py
and you can see the animation work.
