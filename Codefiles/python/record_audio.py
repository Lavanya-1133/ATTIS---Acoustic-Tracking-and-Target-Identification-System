"""
Record audio streamed from the ESP32 over serial and save it as a WAV file.

The ESP32 must send raw binary samples: unsigned 16-bit little-endian values
holding the 12-bit ADC reading (0-4095). By default each sample is centred on
zero and scaled up to signed 16-bit PCM. Use --raw if the firmware already sends
signed 16-bit PCM.

Output file: esp32_recording_YYYYMMDD_HHMMSS.wav (in the current folder)

Usage:
    python record_audio.py                            # 16 kHz, 4 s
    python record_audio.py --rate 16000 --seconds 10
    python record_audio.py --raw
"""

import argparse
import datetime
import time
import wave

import numpy as np
import serial

# ---------------- Configuration ---------------- #
PORT = "COM9"
BAUD = 115200
SAMPLE_RATE = 16000   # must match the sampling rate used in the firmware
RECORD_SECONDS = 4
CHUNK_BYTES = 4096

ADC_MIDPOINT = 2048   # 12-bit ADC midpoint (silence level)
ADC_TO_PCM_SHIFT = 4  # 12-bit -> 16-bit


def adc_to_pcm(chunk):
    """Convert unsigned 12-bit ADC samples (as uint16 LE bytes) to signed 16-bit PCM bytes."""
    samples = np.frombuffer(chunk, dtype="<u2").astype(np.int32)
    pcm = (samples - ADC_MIDPOINT) << ADC_TO_PCM_SHIFT
    return np.clip(pcm, -32768, 32767).astype("<i2").tobytes()


def main():
    parser = argparse.ArgumentParser(description="Record ESP32 serial audio to a WAV file")
    parser.add_argument("--port", default=PORT, help=f"serial port (default {PORT})")
    parser.add_argument("--rate", type=int, default=SAMPLE_RATE, help="sample rate in Hz")
    parser.add_argument("--seconds", type=float, default=RECORD_SECONDS, help="recording length")
    parser.add_argument("--raw", action="store_true",
                        help="write the bytes unchanged (firmware already sends signed 16-bit PCM)")
    args = parser.parse_args()

    ser = serial.Serial(args.port, BAUD, timeout=1)
    time.sleep(2)
    ser.reset_input_buffer()

    filename = f"esp32_recording_{datetime.datetime.now():%Y%m%d_%H%M%S}.wav"
    bytes_needed = int(args.rate * args.seconds) * 2
    bytes_received = 0
    leftover = b""  # odd byte carried over so samples never split across chunks

    with wave.open(filename, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(args.rate)

        print("Recording started...")
        while bytes_received < bytes_needed:
            chunk = ser.read(min(CHUNK_BYTES, bytes_needed - bytes_received))
            if not chunk:
                time.sleep(0.01)
                continue
            bytes_received += len(chunk)

            data = leftover + chunk
            usable = len(data) - len(data) % 2
            data, leftover = data[:usable], data[usable:]
            wav_file.writeframes(data if args.raw else adc_to_pcm(data))

    ser.close()
    print("Recording finished. Saved to:", filename)


if __name__ == "__main__":
    main()
