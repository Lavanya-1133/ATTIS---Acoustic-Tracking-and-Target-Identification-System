"""
ATTIS - Acoustic Tracking and Target Identification System
Live sound-direction estimation from three microphones.

Reads "mic1,mic2,mic3" lines from the ESP32 (firmware: attis_3mic_ads1115),
removes each mic's DC baseline, plots the corrected signals live and prints
the estimated direction of the sound source at a fixed interval.

Usage:
    python attis_direction.py                  # defaults below
    python attis_direction.py --port COM5 --duration 60
    python attis_direction.py --no-plot        # console output only
"""

import argparse
import time
from math import atan2, cos, degrees, radians, sin

import matplotlib.pyplot as plt
import serial

# ---------------- Configuration ---------------- #
PORT = "COM9"            # ESP32 serial port (check Device Manager)
BAUD = 115200            # must match Serial.begin() in the firmware
TIMEOUT_S = 3            # serial read timeout (s)
RUNTIME_S = 100          # total run time (s)
OUTPUT_INTERVAL_S = 0.5  # how often a direction is printed (s)
MAX_POINTS = 100         # samples shown in the live plot

# Baseline (silence) ADC readings, measured with only_inputs / live_mic_plot.py.
# MAX9814 output idles at ~1.25 V -> ~6600 counts on the ADS1115 (0.1875 mV/bit).
BASELINE_I12 = 6600         # mic 1 and mic 2
BASELINE_I3 = 6700          # mic 3 idles slightly higher
I3_SHIFT_CORRECTION = -75   # extra offset to line mic 3 up with mics 1 and 2

# Mic positions on the triangle, as angles from the +X axis (East).
MIC_ANGLES_DEG = (0, 120, 240)


def baseline_correct(raw):
    """Subtract each mic's idle level so all three are centred on zero."""
    return (
        raw[0] - BASELINE_I12,
        raw[1] - BASELINE_I12,
        raw[2] - BASELINE_I3 + I3_SHIFT_CORRECTION,
    )


def direction_from_intensity(intensities):
    """
    Direction of the source in degrees from +X (0-360), or None if there is no signal.

    Each mic is treated as a vector pointing at its position on the triangle,
    scaled by its intensity; the angle of the vector sum is the estimated direction.
    """
    if not any(intensities):
        return None
    x = sum(i * cos(radians(a)) for i, a in zip(intensities, MIC_ANGLES_DEG))
    y = sum(i * sin(radians(a)) for i, a in zip(intensities, MIC_ANGLES_DEG))
    return (degrees(atan2(y, x)) + 360) % 360


def direction_label(angle):
    """Convert an angle (0 deg = East) to one of 8 compass directions."""
    compass_dirs = [
        "East", "Northeast", "North", "Northwest",
        "West", "Southwest", "South", "Southeast",
    ]
    return compass_dirs[int((angle + 22.5) // 45) % 8]


def read_mics(ser):
    """Read one line from the ESP32 and return three floats, or None if malformed."""
    line = ser.readline().decode(errors="ignore").strip()
    try:
        raw = [float(x) for x in line.split(",")[:3]]
    except ValueError:
        return None
    return raw if len(raw) == 3 else None


def setup_plot():
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title("Live Baseline-Corrected Mic Intensities")
    ax.set_xlabel("Sample Number")
    ax.set_ylabel("Corrected Amplitude")
    ax.set_ylim(-500, 500)
    ax.set_xlim(0, MAX_POINTS)
    lines = [
        ax.plot([], [], color, label=label)[0]
        for color, label in (("r-", "Mic 1"), ("g-", "Mic 2"), ("b-", "Mic 3"))
    ]
    ax.legend(loc="upper right")
    return fig, lines


def live_direction_monitor(port, duration, interval, show_plot, save_plot):
    ser = serial.Serial(port=port, baudrate=BAUD, timeout=TIMEOUT_S)
    time.sleep(2)  # ESP32 resets when the port opens
    print(f"Connected to {port} at {BAUD} baud.")
    print(f"Running for {duration}s, output every {interval}s...\n")

    fig, lines = setup_plot() if show_plot else (None, None)
    history = [[], [], []]

    start_time = time.time()
    last_output_time = start_time

    try:
        while time.time() - start_time < duration:
            raw = read_mics(ser)
            if raw is None:
                continue
            corrected = baseline_correct(raw)

            if show_plot:
                for buf, value, line in zip(history, corrected, lines):
                    buf.append(value)
                    del buf[:-MAX_POINTS]
                    line.set_data(range(len(buf)), buf)
                plt.pause(0.001)

            now = time.time()
            if now - last_output_time >= interval:
                elapsed = now - start_time
                angle = direction_from_intensity(corrected)
                if angle is None:
                    print(f"[{elapsed:6.2f}s] No valid input detected.")
                else:
                    print(
                        f"[{elapsed:6.2f}s] Direction: {direction_label(angle):10s} | "
                        f"Angle: {angle:6.1f} deg | "
                        f"Intensities: {corrected[0]:7.1f} {corrected[1]:7.1f} {corrected[2]:7.1f}"
                    )
                last_output_time = now

    except KeyboardInterrupt:
        print("\nStopped manually by user.")
    finally:
        ser.close()
        print("Serial connection closed.")
        if show_plot:
            if save_plot:
                fig.savefig(save_plot, dpi=300, bbox_inches="tight")
                print(f"Plot saved as {save_plot}")
            plt.ioff()
            plt.show()


def main():
    parser = argparse.ArgumentParser(description="ATTIS live sound-direction estimation")
    parser.add_argument("--port", default=PORT, help=f"serial port (default {PORT})")
    parser.add_argument("--duration", type=float, default=RUNTIME_S, help="run time in seconds")
    parser.add_argument("--interval", type=float, default=OUTPUT_INTERVAL_S,
                        help="seconds between direction printouts")
    parser.add_argument("--no-plot", action="store_true", help="disable the live plot")
    parser.add_argument("--save-plot", metavar="FILE", help="save the final plot to FILE (e.g. plot.png)")
    args = parser.parse_args()

    live_direction_monitor(args.port, args.duration, args.interval,
                           show_plot=not args.no_plot, save_plot=args.save_plot)


if __name__ == "__main__":
    main()
