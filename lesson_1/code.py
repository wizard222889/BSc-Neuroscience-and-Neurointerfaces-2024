import time
# import sys, os
# sys.path.append(os.path.join(os.getcwd(), "CapsuleSDK"))

PLATFORM = 'mac'  # 'mac' or 'win'

from CapsuleSDK.Capsule import Capsule
from CapsuleSDK.DeviceLocator import DeviceLocator
from CapsuleSDK.DeviceType import DeviceType
from CapsuleSDK.Device import Device

class EventFiredState:
    def __init__(self): self._awake = False
    def is_awake(self): return self._awake
    def set_awake(self): self._awake = True
    def sleep(self): self._awake = False

device_locator = None
device = None
device_list_event = EventFiredState()
device_conn_event = EventFiredState()

def non_blocking_cond_wait(wake_event: EventFiredState, name: str, total_sleep_time: int):
    print(f"Waiting {name} up to {total_sleep_time}s...")
    steps = int(total_sleep_time * 50)
    for _ in range(steps):
        if device_locator is not None:
            try:
                device_locator.update()
            except Exception:
                pass
        if wake_event.is_awake():
            return True
        time.sleep(0.02)
    return False

def on_device_list(locator, info, fail_reason):
    global device
    chosen = None

    if len(info) == 0:
        print("No devices found.")
        return

    print(f"Found {len(info)} devices.")

    if TARGET_SERIAL is None:
        print(f"Using first device:")
        chosen = info[0]

    else:
        for dev in info:
            print(" device:", dev.get_serial(), dev.get_name())
            if dev.get_serial() == TARGET_SERIAL:
                chosen = dev
                break

    if chosen is None:
        print(f"Target device {TARGET_SERIAL} not found!")
        return

    print()
    print("Connecting to:")
    print("Serial:", chosen.get_serial())
    # TO DO

    # TO DO

    device = Device(locator, chosen.get_serial(), locator.get_lib())
    device_list_event.set_awake()

def on_connection_status_changed(dev, status):
    print("Connection status changed:", status)
    device_conn_event.set_awake()

def main():
    print("Stopping and disconnecting...")
    device.stop()
    device.disconnect()
    print("Done.")

if __name__ == "__main__":
    main()
