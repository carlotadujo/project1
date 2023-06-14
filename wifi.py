import board
import busio
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

ESP32_CS = DigitalInOut(board.ESP_CS)
ESP32_READY = DigitalInOut(board.ESP_BUSY)
ESP32_RESET = DigitalInOut(board.ESP_RESET)

SPI = busio.SPI(board.SCK, board.MOSI, board.MISO)
ESP = adafruit_esp32spi.ESP_SPIcontrol(SPI, ESP32_CS, ESP32_READY, ESP32_RESET)

requests.set_socket(socket, ESP)

def connect():
    print(f"ESP32 status:", ESP.status, "firmware:", ESP.firmware_version.decode('ascii'),
        "HWAddr:", ':'.join([hex(i)[2:] for i in ESP.MAC_address]))

    print('Scanning Wi-Fi networks...')
    for net in ESP.scan_networks():
        print(f"  {net['ssid'].decode('utf-8')} ({net['rssi']} dB)")

    print(f"Connecting to SSID '{secrets['ssid']}'")
    while not ESP.is_connected:
        try:
            ESP.connect_AP(secrets["ssid"], secrets["password"])
        except OSError as e:
            print("Could not connect to AP, retrying: ", e)
            continue

    print(f"Connected to SSID '{ESP.ssid.decode('utf-8')}' ({ESP.rssi} dB)")
    print("IP address:", ESP.pretty_ip(ESP.ip_address))


def get_host_by_name(*args, **kwargs):
    return ESP.pretty_ip(ESP.get_host_by_name(*args, **kwargs))


def ping(*args, **kwargs):
    return ESP.ping(*args, **kwargs)
