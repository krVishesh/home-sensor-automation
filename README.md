# Home Sensor Automation System

![IoT Automation](https://img.shields.io/badge/IoT-Automation-blue)
![MicroPython](https://img.shields.io/badge/MicroPython-FFD43B?style=flat&logo=python&logoColor=blue)
![ESP32](https://img.shields.io/badge/ESP32-E7352C?style=flat&logo=espressif&logoColor=white)

A comprehensive IoT-based home automation system built with MicroPython on ESP32, featuring RFID access control, motion detection, servo control, and smart lighting.

## 🌟 Features

- **RFID Access Control**
  - Secure door access using RFID cards
  - Customizable list of authorized tags
  - Servo-controlled door mechanism

- **Motion Detection**
  - PIR sensor integration
  - Real-time motion monitoring
  - Visual LED feedback

- **Smart Lighting**
  - NeoPixel RGB LED control
  - Remote color control via Firebase
  - Customizable lighting presets

- **Fan Control**
  - Remote fan toggle functionality
  - Simple on/off control

- **Wireless Communication**
  - ESP-NOW for local device communication
  - Wi-Fi connectivity for cloud integration
  - Firebase real-time database integration

## 🛠️ Hardware Requirements

- ESP32 Development Board
- MFRC522 RFID Module
- PIR Motion Sensor
- Servo Motors (2x)
- NeoPixel LED Strip (16 LEDs)
- Fan Module
- RFID Cards/Tags
- Jumper Wires
- Power Supply

## 🔧 Software Requirements

- MicroPython
- Required Libraries:
  - `machine`
  - `mfrc522`
  - `network`
  - `espnow`
  - `neopixel`
  - `urequests`

## 📋 Pin Configuration

| Component    | GPIO Pin |
|-------------|----------|
| RFID SCK    | 18       |
| RFID MOSI   | 23       |
| RFID MISO   | 19       |
| RFID CS     | 5        |
| Servo 1     | 25       |
| Servo 2     | 26       |
| PIR Sensor  | 2        |
| Status LED  | 21       |
| Fan Control | 33       |
| NeoPixel    | 14       |

## 🚀 Setup Instructions

1. **Hardware Setup**
   - Connect all components according to the pin configuration
   - Ensure proper power supply to all components
   - Verify RFID module connections

2. **Software Setup**
   - Flash MicroPython to your ESP32
   - Install required libraries
   - Configure your Wi-Fi credentials
   - Set up Firebase project and update the URL in the code

3. **RFID Configuration**
   - Add your authorized RFID tag UIDs to the `allowed_tags` list
   - Format: `"XX:XX:XX:XX:XX"`

## 💡 Usage

- **RFID Access**: Present an authorized RFID card to trigger the door servo
- **Motion Detection**: PIR sensor automatically detects movement
- **Light Control**: 
  - Use Firebase to set custom colors
  - Toggle lights using the control interface
- **Fan Control**: Toggle fan state remotely

## 🔄 Control Interface

The system accepts the following commands via ESP-NOW:
- Button2: Activate Servo2
- Button3: Toggle Fan
- Button4: Turn off NeoPixel
- Joystick1-Button: Fetch color from Firebase
- Joystick2-Button: Reset NeoPixel to white

## ⚠️ Safety Notes

- Ensure proper voltage levels for all components
- Keep RFID cards secure and update the authorized list regularly
- Monitor system temperature during operation
- Use appropriate power supply for the fan

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### RFID Module Issues
- **Problem**: RFID module not detecting cards
  - **Solution**: 
    - Check SPI connections (SCK, MOSI, MISO, CS)
    - Verify power supply (3.3V)
    - Ensure RFID cards are within range (2-5cm)
    - Check if the RFID module is properly initialized

#### Servo Control Problems
- **Problem**: Servos not moving or moving erratically
  - **Solution**:
    - Verify PWM frequency (should be 50Hz)
    - Check power supply (servos may need separate power source)
    - Ensure duty cycle values are within range (20-120)
    - Check for loose connections

#### NeoPixel Issues
- **Problem**: LEDs not lighting up or showing wrong colors
  - **Solution**:
    - Verify data pin connection
    - Check power supply (5V recommended)
    - Ensure proper number of LEDs is set
    - Check for loose connections or damaged LEDs

#### PIR Sensor Problems
- **Problem**: False triggers or no detection
  - **Solution**:
    - Adjust sensitivity potentiometer
    - Ensure proper power supply (3.3V)
    - Check for environmental factors (heat sources, moving objects)
    - Verify connection to correct GPIO pin

#### ESP-NOW Communication Issues
- **Problem**: Devices not communicating
  - **Solution**:
    - Ensure both devices are in ESP-NOW mode
    - Check if MAC addresses are correctly configured
    - Verify both devices are on the same channel
    - Check for interference from other wireless devices

#### Firebase Connection Problems
- **Problem**: Unable to fetch data from Firebase
  - **Solution**:
    - Verify Wi-Fi credentials
    - Check Firebase URL and database rules
    - Ensure proper JSON format in Firebase
    - Check for network connectivity

#### General System Issues
- **Problem**: System not booting or unstable
  - **Solution**:
    - Check power supply stability
    - Verify all ground connections
    - Ensure proper voltage levels (3.3V for ESP32)
    - Check for short circuits
    - Monitor system logs for error messages

### Debugging Tips
1. Use the onboard LED (GPIO 21) to check system status
2. Monitor serial output for error messages
3. Check individual components separately before integration
4. Use a multimeter to verify voltage levels
5. Keep a backup of working configurations

## 📝 License

This project is open-source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Made with ❤️ for IoT enthusiasts