# Initial Design Ideas

### Pi 4 (Robot Brain)
- High-level decision making
- runs ros
- processes sensor data
- path planning, mapping, localization
- sends out velocity commands

### Arduino
- motor control
- reads encoders
- runs PID (feedback) loops
- talks to motors

### Motor Driver
- takes PWM + digital direction signals
- supplies current + voltage to motors

