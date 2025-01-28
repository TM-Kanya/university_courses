# Autonomous Mail Delivery Robot

This folder houses partial code for the 'ROB301: Introduction to Robotics' final project.

## Project Goal

The key objective for this project was to design a control system for a TurtleBot3 Waffle Pi robot to simulate mail delivery on a topological map, where colored paper represents offices and tape forms the closed-loop path to follow.

## Design Methodology: Bayesian Localization
Table 1: Defining variables used for probabilistic inference

| Variable | Definition |
|----------|------------|
| u | Control (direction/action): -1 (move backwards), 0 (stop), 1 (move forwards) |
| z | Measurement (color): Red, purple, orange, brown, white (line). The measurement model is based on the measurement uncertainty associated with the currently detected colour |
| x | State (office): Integer from 2 to 12 |

Using the Raspberry Pi camera on the TurtleBot as a sensor, the code uses two provided ROS nodes:
- `line_idx`: subscribes to the captured grayscale images and publishes the index with the greatest light intensity, theoretically outputting the position of the white tape ‘line.’
- `mean_img_rgb`: subscribes to the captured RGB images and publishes the mean pixel intensity.

The robot follows the line by calculating the difference between the midpoint of the image’s width to the detected position from `line_idx`, and utilizing PID control accordingly ($$u(t)=-k_p[x(t)-x_d] -k_d(\frac{d}{dt}[x(t)-xd])-ki0t[x()-xd]d ]$$). Notably, the proportional term helps decrease rise time, the integration term helps eliminate steady state error, and the derivative term helps decrease overshoot, settling time, and improve stability.

To build the measurement model, the normalized Euclidean distance is calculated for each possible color (red, purple, orange, brown, or line) relative to the detected RGB value using (rdetected-ri)2+(gdetected-gi)2+(bdetected-bi)2i(rdetected-ri)2+(gdetected-gi)2+(bdetected-bi)2, and the color with the smallest distance to the detected RGB is set to be the detected color. 

If the robot is at an office, which is defined to be true when the previous color state was not a line and the current color state is a line (i.e., the robot is just about to ‘leave’ the office), the state prediction is computed using p(xk+1|z0:k) = xkp(xk+1|xk, uk)p(xk|z0:k) and the state is updated using p(xk+1|z0:k+1)= p(zk+1|xk+1)p(xk+1|z0:k)k+1p(xk+1|k+1)p(k+1|z0:k). If the robot has not visited this office before, the robot mimics a delivery by stopping for two seconds before continuing. 
