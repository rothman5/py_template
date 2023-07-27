"""Virtual COM Port module."""

import time
import struct
import datetime
import threading
import serial

from .logger import Logger
from .singleton import Singleton

log = Logger()


class VirtualCOMPort(Singleton):
    """Virtual COM Port class."""

    _TaskLock = threading.Lock()

    def __init__(self, portname: str | None = None, baudrate: int = 112500) -> None:
        self.port = serial.Serial(portname, baudrate, timeout=0.5)
        self.open = False
        self.portname = portname
        self.baudrate = baudrate

    def open_port(self) -> bool:
        """Open a COM port with the specified baudrate.

        Args:
            portname (str): The name of the COM port.
            baudrate (int): The data transfer speed.

        Returns:
            bool: Connection state.
        """

        attempt = 1
        while not self.open and attempt <= 10:
            try:
                log.info("Opening %s... #%d", self.portname, attempt)
                self.port = serial.Serial(self.portname, self.baudrate, timeout=0.5)
                if self.port.is_open:
                    self.open = True
                    log.info("Opened %s @ %d bits/s\n", self.portname, self.baudrate)

            except OSError:
                attempt += 1
                time.sleep(1)

    def close_port(self) -> None:
        """Close the COM port if it's open."""
        if self.open:
            self.port.close()
            self.open = False
            log.info("Closed %s successfully.", self.portname)

    def connect(self) -> bool:
        """Connect to the specified COM port.

        Returns:
            bool: Connection state.
        """

        if self.open:
            return True

        if not self.portname:
            return False

        try:
            return self.open_port()

        except KeyboardInterrupt:
            self.close_port()
            return False

    def checksum(self, cmd: str) -> str:
        """Calculate the command checksum then return the hex string representation.

        Args:
            cmd (str): Hex command string.

        Returns:
            str: Checksum as a hex string.
        """

        checksum = 0
        for byte in range(0, len(cmd), 2):
            checksum += int(cmd[byte : byte + 2], 16)

        return checksum.to_bytes(2, "little").hex()

    def transmit(self, cmd: str) -> int:
        """Transmit a command to the COM port.

        Args:
            cmd (str): Command as a hex string (no checksum bytes).

        Returns:
            int: The number of bytes transmitted or -1 (error).
        """

        if not self.open:
            log.error("Unable to begin the transmission since the COM port isn't open.")
            return -1

        with VirtualCOMPort._TaskLock:
            try:
                command = cmd + self.checksum(cmd)
                bytes_transmitted = self.port.write(bytearray.fromhex(command))
                if bytes_transmitted > 0:
                    log.info("tx(%d): %s", bytes_transmitted, command)
                    return bytes_transmitted

                return -1

            except OSError:
                log.error("Unable to transmit the command:\n\t(%s)", command)
                return -1

    def wait_for_bytes(self, size: int) -> bool:
        """Wait for the specified amount of bytes to be available on the COM port.

        Args:
            size (int): The amount of bytes to wait for.

        Returns:
            bool: Whether the amount of bytes are there.
        """

        while self.port.in_waiting < size:
            try:
                pass
            except OSError:
                return False
            except KeyboardInterrupt:
                return False

        return True

    def receive(self, size: int) -> bytes:
        """Receive a response from the COM port.

        Args:
            size (int): _description_

        Returns:
            bytes: _description_
        """

        if not self.open:
            log.error("Unable to begin the reception since the COM port isn't open.")
            return bytes()

        with VirtualCOMPort._TaskLock:
            try:
                if not self.wait_for_bytes(size):
                    return bytes()
                rsp = self.port.read(size)
                log.info("rx(%d): %s\n", len(rsp), rsp.hex())
                return rsp

            except OSError:
                log.error("Failed to receive a response.")
                return bytes()

    def get_config_hex_string(self, values: list[int]) -> str:
        """Take a list of integers and convert it to a hex string.

        Args:
            values (list[int]): Config values.

        Returns:
            str: Config values as a hex string.
        """
        config_string = ""
        for value in values:
            config_string += value.to_bytes(4, "little").hex()

        return config_string

    def get_system_config(self) -> list[int]:
        """Request the system config.

        Returns:
            list[int]: System config values.
        """

        self.transmit("dd03070000")
        config_values = self.receive(42)
        if not config_values:
            return []
        return [
            int.from_bytes(config_values[4:8], "little"),
            int.from_bytes(config_values[8:12], "little"),
            int.from_bytes(config_values[12:16], "little"),
            int.from_bytes(config_values[16:20], "little"),
            int.from_bytes(config_values[20:24], "little"),
            int.from_bytes(config_values[24:28], "little"),
            int.from_bytes(config_values[28:32], "little"),
            int.from_bytes(config_values[32:36], "little"),
            int.from_bytes(config_values[36:40], "little"),
        ]

    def set_system_config(self, values: list[int]) -> None:
        """Send the command to set the system config.

        Args:
            values (list[int]): The new system config values.
        """

        self.set_epoch_time()
        self.transmit("dd032b0001" + self.get_config_hex_string(values))
        self.receive(42)

    def get_epoch_time(self) -> str:
        """Request the epoch time.

        Returns:
            str: Epoch timestamp.
        """

        self.transmit("dd04070000")
        epoch_bytes = self.receive(10)
        if not epoch_bytes:
            return "None"
        epoch = int.from_bytes(epoch_bytes[4:8], "little")
        return datetime.datetime.fromtimestamp(epoch).strftime("%c")

    def set_epoch_time(self) -> None:
        """Send the command to set the epoch timestamp."""

        epoch = int(datetime.datetime.now().timestamp())
        self.transmit("dd040b0001" + epoch.to_bytes(4, "little").hex())
        self.receive(10)

    def format_sd_card(self) -> bool:
        """Format the SD card. i.e., delete all the files.

        Returns:
            bool: Whether the format was succesful.
        """

        self.transmit("dd050600")
        return bool(self.receive(7)[4])

    def set_logging_state(self, state: bool) -> bool:
        """Send the command to force the logging state.

        Args:
            state (bool): Desired logging state.

        Returns:
            bool: Current logging state.
        """

        self.transmit(f"dd060700{int(state):02}")
        return bool(self.receive(7)[4])

    def request_data(self) -> list[float]:
        """Request sensor data.

        Returns:
            list[float]: List of sensor data.
        """

        self.transmit("dd070600")
        data_values = self.receive(46)
        if not data_values:
            return []
        return [
            struct.unpack("f", data_values[4:8]),
            struct.unpack("f", data_values[8:12]),
            struct.unpack("f", data_values[12:16]),
            struct.unpack("f", data_values[16:20]),
            struct.unpack("f", data_values[20:24]),
            struct.unpack("f", data_values[24:28]),
            struct.unpack("f", data_values[28:32]),
            struct.unpack("f", data_values[32:36]),
            struct.unpack("f", data_values[36:40]),
            struct.unpack("f", data_values[40:44]),
        ]
