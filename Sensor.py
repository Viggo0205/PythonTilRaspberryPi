from gpiozero import DigitalInputDevice
from time import sleep
import socket

# Define UDP server details
UDP_IP = "192.168.103.234"  # Replace with your target IP address
UDP_PORT = 7                # Replace with your desired port number

# Define IR sensor pin
ir_sensor = DigitalInputDevice(17)  # Replace 17 with your GPIO pin

# Sensor Name (you can change this to any name you'd like)
sensor_name = "Sensor1"  # Add the name or identifier of your sensor here

# Function to send a message over UDP
def SendMSG(sensor_state, name):
    msg = f"{{'name': '{name}', 'occupied': {sensor_state}}}"  # Add 'name' to the JSON mess>
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))

print("Testing sensor... Press Ctrl+C to exit.")
try:
    while True:
        # Read the sensor state
        sensor_state = ir_sensor.value  # 0 = obstacle, 1 = no obstacle

        if sensor_state == 0:
            # No obstacle detected
            print("Sensor state: True (Obstacle Detected)")
            SendMSG(sensor_state, sensor_name)  # Send the state over UDP
            sleep(10)  # Wait for 10 seconds when no obstacle is detected
        else:
            # Obstacle detected
            print("Sensor state: False (No Obstacle Detected)")
            SendMSG(sensor_state, sensor_name)  # Send the state over UDP

        # Small delay to avoid excessive CPU usage
        sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting program.")
