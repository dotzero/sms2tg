import threading
import time
from queue import Empty, Queue

import serial
from termcolor import colored

from src.conf import SERIAL_PORT

to_request_queue = Queue()
received_response_queue = Queue()
antenna_signal_queue = Queue()
request_check_message_event = threading.Event()


def __read_all_income_text(ser: serial.Serial):
    try:
        line = ser.readline()
    except serial.SerialException as exc:
        # Let the caller handle reconnect
        raise exc

    while len(line) != 0:
        print("SIM868 answer:", colored(line, color="green"))

        line_decoded = line.decode()
        if line_decoded.startswith("+CMTI"):
            request_check_message_event.set()
        elif line_decoded.startswith("+CANT"):
            antenna_signal_queue.put(line_decoded)
        elif line_decoded == "\r\n":
            pass
        else:
            received_response_queue.put(line_decoded)

        try:
            line = ser.readline()
        except serial.SerialException as exc:
            # Let the caller handle reconnect
            raise exc


def __send_one_request(ser: serial.Serial):
    try:
        to_request = to_request_queue.get(block=False)
        print("SIM868 request:", colored(to_request, color="cyan"))
        ser.write((to_request + "\n").encode())
    except Empty:
        pass


def receive_cmd_loop():
    ser = None
    while True:
        try:
            if ser is None or not ser.is_open:
                ser = serial.Serial(SERIAL_PORT, timeout=1, write_timeout=1)
                print("SIM868 serial connected:", SERIAL_PORT)

            __read_all_income_text(ser)
            __send_one_request(ser)
        except serial.SerialException as exc:
            print("SIM868 serial error:", exc)
            try:
                if ser is not None:
                    ser.close()
            finally:
                ser = None
            # brief backoff before reconnecting
            time.sleep(1)
