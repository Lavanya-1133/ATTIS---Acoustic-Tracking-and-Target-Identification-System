// ATTIS - earlier firmware (ESP32 built-in ADC, no ADS1115)
//
// Reads three MAX9814 microphones directly on the ESP32's 12-bit ADC pins and
// prints them as CSV for the Arduino Serial Plotter:  mic1,mic2,mic3,2000,8000
// The last two values are fixed reference lines that keep the plotter's
// Y axis steady. Python scripts only use the first three values.
//
// Wiring: Mic 1 -> GPIO32, Mic 2 -> GPIO34, Mic 3 -> GPIO35

const int MIC1_PIN = 32;
const int MIC2_PIN = 34;
const int MIC3_PIN = 35;

const int REF_LOW = 2000;
const int REF_HIGH = 8000;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int mic1 = analogRead(MIC1_PIN);
  int mic2 = analogRead(MIC2_PIN);
  int mic3 = analogRead(MIC3_PIN);

  Serial.print(mic1);
  Serial.print(",");
  Serial.print(mic2);
  Serial.print(",");
  Serial.print(mic3);
  Serial.print(",");
  Serial.print(REF_LOW);
  Serial.print(",");
  Serial.println(REF_HIGH);

  delay(50);  // refresh rate of the plot
}
