// ATTIS - final firmware (ESP32 + ADS1115 + 3x MAX9814)
//
// Reads three MAX9814 microphones through an ADS1115 16-bit ADC (I2C) and
// streams one CSV line per reading over serial:  mic1,mic2,mic3
// Works with attis_direction.py and live_mic_plot.py, and with the Arduino Serial Plotter.
//
// Wiring: ADS1115 SDA/SCL -> ESP32 I2C pins (default GPIO21/GPIO22)
//         Mic 1 -> A0, Mic 2 -> A1, Mic 3 -> A2
//
// Library: Adafruit ADS1X15 (Arduino Library Manager)

#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads;

void setup(void)
{
  Serial.begin(115200);

  // Default gain (GAIN_TWOTHIRDS): +/- 6.144 V range, 1 bit = 0.1875 mV.
  // The MAX9814 idles at ~1.25 V, which reads as ~6600 counts.
  // Never let the inputs exceed VDD + 0.3 V.
  if (!ads.begin())
  {
    Serial.println("Failed to initialize ADS1115.");
    while (1);
  }
}

void loop(void)
{
  int16_t mic1 = ads.readADC_SingleEnded(0);
  int16_t mic2 = ads.readADC_SingleEnded(1);
  int16_t mic3 = ads.readADC_SingleEnded(2);

  Serial.print(mic1);
  Serial.print(",");
  Serial.print(mic2);
  Serial.print(",");
  Serial.println(mic3);
}
