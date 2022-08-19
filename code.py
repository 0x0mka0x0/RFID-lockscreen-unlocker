import time
import board
import digitalio
import simpleio
import busio
import mfrc522
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)
sck = board.GP6
mosi = board.GP7
miso = board.GP4
spi = busio.SPI(sck, MOSI=mosi, MISO=miso)

cs = digitalio.DigitalInOut(board.GP5)
rst = digitalio.DigitalInOut(board.GP8)
rfid = mfrc522.MFRC522(spi, cs, rst)
rfid.set_antenna_gain(0x07 << 4)

print("\n***** Scan your RFid tag/card *****\n")

prev_data = ""
prev_time = 0
timeout = 1

while True:
    (status, tag_type) = rfid.request(rfid.REQALL)

    if status == rfid.OK:
        (status, raw_uid) = rfid.anticoll()

        if status == rfid.OK:
            rfid_data = "{:02x}{:02x}{:02x}{:02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])

            if rfid_data != prev_data:
                prev_data = rfid_data

                print("Card detected! UID: {}".format(rfid_data))

                if rfid_data == "762321f8":
                    keyboard.press(Keycode.TWO)
                    time.sleep(0.05)
                    keyboard.release(Keycode.TWO)
                    keyboard.press(Keycode.ZERO)
                    time.sleep(0.05)
                    keyboard.release(Keycode.ZERO)
                    keyboard.press(Keycode.ZERO)
                    time.sleep(0.05)
                    keyboard.release(Keycode.ZERO)
                    keyboard.press(Keycode.ONE)
                    time.sleep(0.05)
                    keyboard.release(Keycode.ONE)
                    
            prev_time = time.monotonic()

    else:
        if time.monotonic() - prev_time > timeout:
            prev_data = ""