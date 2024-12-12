from gpiozero import DigitalInputDevice
from time import sleep
import socket
from cryptography.fernet import Fernet

# Generate or provide a key (ensure the same key is used on the receiver side)
key =b'G4UJyewVp1Tw5PLd5RgN4wYf-F7GAgA_lT3-Yj4oDfU='
cipher_suite = Fernet(key)

# Define UDP server details
UDP_IP = "255.255.255.255"  # Use broadcast address
UDP_PORT = 5000             # Replace with your desired port number

# Define IR sensor pin
ir_sensor = DigitalInputDevice(17)  # Replace 17 with your GPIO pin

# Sensor Name (you can change this to any name you'd like)
sensor_name = "Sensor1"  # Add the name or identifier of your sensor here

# Function to send a message over UDP
def SendMSG(sensor_state, name):
    msg = f"{{'name': '{name}', 'occupied': {sensor_state}}}"  # Add 'name' to >
    encrypted_msg = cipher_suite.encrypt(msg.encode())  # Encrypt the message
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Enable br>
        sock.sendto(encrypted_msg, (UDP_IP, UDP_PORT))  # Send encrypted data

print("Testing sensor... Press Ctrl+C to exit.")
try:
    while True:
        # Read the sensor state
        sensor_state = ir_sensor.value  # 0 = obstacle, 1 = no obstacle

        if sensor_state == 0:
            # Obstacle detected
            print("Sensor state: True (Obstacle Detected)")
            SendMSG(sensor_state, sensor_name)  # Send the state over UDP
            sleep(2)  # Wait for 2 seconds before checking again
        else:
            # No obstacle detected
            print("Sensor state: False (No Obstacle Detected)")
            SendMSG(sensor_state, sensor_name)  # Send the state over UDP
            sleep(2)

        # Small delay to avoid excessive CPU usage
        sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting program.")

