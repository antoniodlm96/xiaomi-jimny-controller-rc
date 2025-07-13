import asyncio
import keyboard
from bleak import BleakClient

# BLE device address and characteristic UUID
ADDRESS = "9B947988-8931-F761-091F-026912A95ECE" 
UUID_WRITE = "4fbbffe3-c59c-478d-bb99-d6e06367e344"

# Initial values
angle = 0x3E   # initial steering angle (0x3E is straight)
speed = 0x04   # initial speed (0x04 is neutral/stopped)

# Steering angle limits and step
MIN_ANGLE = 0x00
MAX_ANGLE = 0x70
ANGLE_STEP = 0x05

# Speed limits and step
MIN_SPEED = 0x00
MAX_SPEED = 0x09
SPEED_STEP = 0x01

FIXED_BYTE = 0x00  # third byte (seems fixed based on reverse engineering)

# Function to send a command to the BLE device
async def send_command(client, angle_val, speed_val):
    command = bytes([angle_val, speed_val, FIXED_BYTE])
    await client.write_gatt_char(UUID_WRITE, command)
    print(f"Sent command: {command.hex()}  (angle={angle_val - 52}, speed={speed_val})")

# Main control loop
async def control_loop():
    global angle, speed

    async with BleakClient(ADDRESS) as client:
        if not client.is_connected:
            print("❌ Not connected to the car.")
            return

        print("✅ Connected. ←/→ to steer | ↑/↓ to accelerate/brake | ESC to exit")

        while True:
            sent_dir = False
            sent_acc = False

            # Reset speed to neutral if no acceleration key is pressed
            if not keyboard.is_pressed("up") and not keyboard.is_pressed("down"):
                speed = 0x04

            # Steering left
            if keyboard.is_pressed("left"):
                angle = max(MIN_ANGLE, angle - ANGLE_STEP)
                sent_dir = True

            # Steering right
            if keyboard.is_pressed("right"):
                angle = min(MAX_ANGLE, angle + ANGLE_STEP)
                sent_dir = True

            # Accelerating
            if keyboard.is_pressed("up"):
                speed = min(MAX_SPEED, speed + SPEED_STEP)
                sent_acc = True

            # Braking / reversing
            if keyboard.is_pressed("down"):
                speed = max(MIN_SPEED, speed - SPEED_STEP)
                sent_acc = True

            # Exit condition
            if keyboard.is_pressed("esc"):
                print("🛑 Exiting...")
                await send_command(client, 0x3E, 0x04)  # Stop the car (neutral angle and speed)
                break

            # Send steering command if direction changed
            if sent_dir:
                await send_command(client, angle, 0x04)

            # Send speed command if acceleration/braking occurred
            if sent_acc:
                await send_command(client, angle, speed)

            await asyncio.sleep(0.1)  # Small delay to prevent flooding the BLE device

# Run the control loop
asyncio.run(control_loop())

