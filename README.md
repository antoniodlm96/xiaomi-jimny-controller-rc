# 🚗 Xiaomi Jimny Controller (Python)

Python script to control the Xiaomi Jimny RC car via Bluetooth Low Energy (BLE).  
This project allows you to remotely control steering and throttle of the car using a keyboard, while communicating directly with the vehicle over BLE.

---

## ✨ Features

- Full control of the car's **steering and speed** via BLE commands.
- Real-time interaction using the **keyboard** (arrow keys or custom bindings).
- Optimized to **only send BLE commands** when a key is actively pressed.
- Easily extendable to support:
  - **Camera streaming**
  - **Remote control over Wi-Fi**
  - **Sensor integration** (e.g. Raspberry Pi, IMU)

---

## 🛠️ Technologies and Libraries

- **Python 3.7+**
- [`bleak`](https://github.com/hbldh/bleak) – BLE communication library for Python.
- [`keyboard`](https://github.com/boppreh/keyboard) – Detects key presses for interactive control.
- `asyncio` – For asynchronous I/O with the BLE device.

---

## ⚙️ How It Works

- The script connects to the Xiaomi Jimny car using its BLE MAC address and characteristic UUID.
- BLE commands are sent as bytes to:
  - Set the **steering direction** (e.g. left, right, center)
  - Control the **motor speed** (e.g. forward, backward, stop)
- These commands are sent **only while a key is pressed**, preventing erratic behavior.

### 🧾 Example Byte Format

A typical BLE command looks like:

[0x3E, 0x04, 0x01]


Where:
- `0x3E` = Steering (center)
- `0x04` = Speed (value can vary)
- `0x01` = Control flag (usually constant)

---

## 📦 Installation

```bash
pip install bleak keyboard
```

🚀 Usage
```
python3 jimny_controller.py
```

⚠️ On Linux or macOS, administrator privileges may be required to detect keyboard events:
```
sudo python3 jimny_controller.py
```
