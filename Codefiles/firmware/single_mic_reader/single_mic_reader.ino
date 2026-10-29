// Single-microphone test (ESP32 + 1x MAX9814)
//
// Reads one MAX9814 on GPIO32 and prints each 12-bit ADC value (0-4095) as a
// text line. Used to collect the readings in data/mic_readings.xlsx and to view
// the signal in the Arduino Serial Plotter or a serial terminal (e.g. CoolTerm).
//
// Note: this prints text, not the binary stream that record_audio.py expects.

const int MIC_PIN = 32;

void setup() {
  pinMode(MIC_PIN, INPUT);
  Serial.begin(115200);
}

void loop() {
  int voice = analogRead(MIC_PIN);
  Serial.println(voice);
  delayMicroseconds(62);  // ~16 kHz target rate (actual rate is limited by serial speed)
}
