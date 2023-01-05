from DShotPIO import DShotPIO, DSHOT_SPEEDS
from machine import ADC
import utime

# Util function to remap one range into another
def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def example():
    # Read in from a potentiometer to get target speed
    potentiometerPin = ADC(28)
    # Create the DShot object 
    dshot = DShotPIO(stateMachineID=0, outputPin=4, dshotSpeed=DSHOT_SPEEDS.DSHOT300)

    # Most ESCs need a period of zero throttle to arm
    for _ in range(100):
        dshot.sendThrottleCommand(48)
        utime.sleep(0.01)

    while True():
        # Get the potentiometer value and remap it to 48 - 2047
        potentiometerValue = potentiometerPin.read_u16()
        target = int(remap(potentiometerValue, 0, 65536, 48, 2047))

        # Drastically changing the throttle will cause problems on a physical motor
        # This is a simple way to slowly increase or decrease throttle towards a target
        if(target > throttle):
            throttle += 1
        elif(target < throttle):
            throttle -= 1
        
        # Send the throttle command to the ESC
        # This only sends one throttle command to the ESC, they need to be constantly sent or the ESC will turn off
        dshot.sendThrottleCommand(throttle)

        # Only send the control signal once every 10ms
        # I don't actually know how often the signal should be sent, but this seems to work
        utime.sleep(0.01)

example()