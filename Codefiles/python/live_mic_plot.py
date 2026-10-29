"""
ATTIS - live plot of the three microphone signals (no direction estimation).

Used to check the wiring and to find each mic's baseline (silence) level.
The baseline values found here are the ones used in attis_direction.py.

Usage:
    python live_mic_plot.py                 # raw ADC values
    python live_mic_plot.py --calibrated    # baseline-corrected, centred on zero
"""

import argparse
import time

import matplotlib.pyplot as plt
import serial

# ---------------- Configuration ---------------- #
PORT = "COM9"
BAUD = 115200
TIMEOUT_S = 1
MAX_POINTS = 100      # samples shown in the plot
RUNTIME_S = 100       # total run time (s)

# Baseline references (see attis_direction.py)
BASELINE_I12 = 6600
BASELINE_I3 = 6700
I3_SHIFT_CORRECTION = -75


def main():
    parser = argparse.ArgumentParser(description="Live plot of the three ATTIS mic signals")
    parser.add_argument("--port", default=PORT, help=f"serial port (default {PORT})")
    parser.add_argument("--duration", type=float, default=RUNTIME_S, help="run time in seconds")
    parser.add_argument("--calibrated", action="store_true",
                        help="subtract the baseline from each mic before plotting")
    args = parser.parse_args()

    ser = serial.Serial(port=args.port, baudrate=BAUD, timeout=TIMEOUT_S)
    time.sleep(2)
    print(f"Connected to {args.port} at {BAUD} baud")

    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel("Sample Window")
    ax.set_xlim(0, MAX_POINTS)
    if args.calibrated:
        ax.set_title("Baseline-Corrected Microphone Intensities (I1, I2, I3)")
        ax.set_ylabel("Corrected Amplitude")
        ax.set_ylim(-500, 500)
        labels = (f"Mic 1 (I1 - {BASELINE_I12})",
                  f"Mic 2 (I2 - {BASELINE_I12})",
                  f"Mic 3 (I3 - {BASELINE_I3} {I3_SHIFT_CORRECTION:+})")
    else:
        ax.set_title("Live Mic Intensities (I1, I2, I3)")
        ax.set_ylabel("Amplitude / Intensity (ADC counts)")
        ax.set_ylim(5000, 9000)
        labels = ("Mic 1 (I1)", "Mic 2 (I2)", "Mic 3 (I3)")

    lines = [ax.plot([], [], color, label=label)[0]
             for color, label in zip(("r-", "g-", "b-"), labels)]
    ax.legend(loc="upper right")

    history = [[], [], []]
    start_time = time.time()
    try:
        while time.time() - start_time < args.duration:
            line = ser.readline().decode(errors="ignore").strip()
            try:
                values = [float(x) for x in line.split(",")[:3]]
            except ValueError:
                continue
            if len(values) != 3:
                continue

            if args.calibrated:
                values = [values[0] - BASELINE_I12,
                          values[1] - BASELINE_I12,
                          values[2] - BASELINE_I3 + I3_SHIFT_CORRECTION]

            for buf, value, plot_line in zip(history, values, lines):
                buf.append(value)
                del buf[:-MAX_POINTS]
                plot_line.set_data(range(len(buf)), buf)
            plt.pause(0.001)

    except KeyboardInterrupt:
        print("\nStopped manually by user.")
    finally:
        ser.close()
        print("Serial connection closed.")
        plt.ioff()
        plt.show()


if __name__ == "__main__":
    main()
