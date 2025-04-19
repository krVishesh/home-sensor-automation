from machine import Pin, PWM, SPI
from mfrc522 import MFRC522
import time
import network
import espnow
import neopixel
import json
import urequests

# Initialize SPI and RFID module
spi = SPI(2, baudrate=1000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
rfid = MFRC522(spi, cs=Pin(5, Pin.OUT))
allowed_tags = {"...", "...", "..."} # format of RFID Cards: XX:XX:XX:XX:XX

# Servo setup
servo1 = PWM(Pin(25), freq=50)
servo2 = PWM(Pin(26), freq=50)

def set_servo_angle(servo, angle):
    print(f"Setting servo to {angle} degrees")
    min_duty, max_duty = 20, 120
    duty = int((angle / 180) * (max_duty - min_duty) + min_duty)
    servo.duty(duty)

def activate_servo(servo, angle, duration=2):
    print(f"Activating servo at angle {angle} for {duration} seconds")
    set_servo_angle(servo, angle)
    time.sleep(duration)
    set_servo_angle(servo, 180)  # Reset to default position

# PIR Sensor
pir = Pin(2, Pin.IN)
led_status = Pin(21, Pin.OUT)

# Fan Control
fan = Pin(33, Pin.OUT)

# NeoPixel (16 LEDs on GPIO 14)
neopixel_count = 16
np = neopixel.NeoPixel(Pin(14), neopixel_count)

# ESP-NOW Setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
time.sleep(0.5)
esp = espnow.ESPNow()
esp.active(True)

# Set system status LED ON
led_status.value(1)
print("System Initialized")

# Function to fetch color from Firebase
def fetch_firebase_color():
    try:
        url = "https://iot-data-collection-f7902-default-rtdb.asia-southeast1.firebasedatabase.app/data.json"
        print("Fetching color from Firebase...")
        
        # Add a timeout in case of network issues
        response = urequests.get(url, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            print(f"Received data: {data}")
            
            # Extract color data
            color_data = data.get("color", {})
            red = color_data.get("red", 255)
            green = color_data.get("green", 255)
            blue = color_data.get("blue", 255)
            
            print(f"Extracted color: Red={red}, Green={green}, Blue={blue}")
            return (red, green, blue)
        else:
            print(f"Error: Firebase returned status code {response.status_code}")
            return (100, 100, 100)  # Default to white if fetch fails

    except Exception as e:
        print(f"Error fetching Firebase data: {e}")
        return (100, 0, 0)  # Default to red if fetch fails

# Function to set NeoPixel color
def set_neopixel_color(color):
    print(f"Setting NeoPixel color: {color}")
    for i in range(neopixel_count):
        np[i] = color
    np.write()

# Function to reset NeoPixel to white
def reset_neopixel():
    print("Resetting NeoPixel to white")
    set_neopixel_color((100, 100, 100))  # White

# Function to blink the LED
def blink_led(duration=0.5, times=3):
    for _ in range(times):
        led_status.value(0)  # Turn off LED
        time.sleep(duration)
        led_status.value(1)  # Turn on LED
        time.sleep(duration)

# Switch to Wi-Fi mode
def switch_to_wifi():
    """Disable ESP-NOW and enable Wi-Fi to send data to Firebase."""
    print("Switching to Wi-Fi...")
    blink_led()  # Blink LED when switching to Wi-Fi mode
    
    esp.active(False)  # Disable ESP-NOW
    wlan.disconnect()
    wlan.connect("Capstone", "kya karna hai")
    
    while not wlan.isconnected():
        time.sleep(0.5)
    
    print("Connected to Wi-Fi:", wlan.ifconfig())
    time.sleep(2)

# Switch to ESP-NOW mode
def switch_to_espnow():
    """Disable Wi-Fi and re-enable ESP-NOW."""
    print("Switching back to ESP-NOW...")
    blink_led()  # Blink LED when switching to ESP-NOW mode
    
    wlan.disconnect()  
    wlan.active(False)
    time.sleep(1)

    wlan.active(True)
    esp.active(True)
    time.sleep(1)

print("System Ready. Waiting for data...")

switch_to_espnow()
while True:
    peer_mac, msg = esp.irecv(100)
    if msg:
        try:
            data = json.loads(msg.decode().replace("'", '"'))
            button2 = data.get("Button2", 0)
            button3 = data.get("Button3", 0)
            button4 = data.get("Button4", 0)
            joystick1_btn = data.get("Joystick1-Button", 1)
            joystick2_btn = data.get("Joystick2-Button", 1)
            
            if button2:
                print("Button2 Pressed - Activating Servo2")
                activate_servo(servo2, 90)
            if button3:
                fan.value(not fan.value())  # Toggle Fan
                print(f"Button3 Pressed - Fan State: {fan.value()}")
            if button4:
                print("Button4 Pressed - Setting NeoPixel to Off")
                set_neopixel_color((0, 0, 0))  # Off
            if not joystick1_btn:
                print("Joystick1-Button Pressed - Fetching color from Firebase")
                switch_to_wifi()  # Switch to Wi-Fi mode
                set_neopixel_color(fetch_firebase_color())
                switch_to_espnow()  # Switch back to ESP-NOW mode
            if not joystick2_btn:
                print("Joystick2-Button Pressed - Resetting NeoPixel to White")
                reset_neopixel()
        except Exception as e:
            print(f"Error decoding message: {e}")

    # RFID for Servo1 access
    status, tag_type = rfid.request(rfid.REQIDL)
    if status == rfid.OK:
        status, uid = rfid.anticoll()
        if status == rfid.OK:
            tag_uid = ":".join(f"{i:02X}" for i in uid)
            print(f"RFID Detected: {tag_uid}")
            if tag_uid in allowed_tags:
                print("Authorized Tag - Activating Servo1")
                activate_servo(servo1, 90)
            else:
                print("Unauthorized tag detected:", tag_uid)
    
    # PIR motion detection
    led_status.value(pir.value())
    print(f"PIR State: {pir.value()}")
    time.sleep(0.1)

