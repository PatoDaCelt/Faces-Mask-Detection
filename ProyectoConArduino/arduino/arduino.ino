#include<Servo.h>

//Pines
#define BUZZER 12
#define MOTOR 3
#define LED1 8
#define LED2 9

Servo motor;
int option;

void setup() {
  Serial.begin(9600);
  motor.attach(MOTOR);
  pinMode(BUZZER, OUTPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    option = Serial.read();
    //Serial.println(option);

    if (option == 'P') {
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, LOW);
      sonidoCorrecto();
      motor.write(0);
    }

    if (option == 'N') {
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, HIGH);
      sonidoError();
      motor.write(180);
    }
  }
}

void sonidoCorrecto() {
  tone(BUZZER, 1000, 200);  // Tono medio
  delay(250);
  tone(BUZZER, 1500, 200);  // Tono más alto
  delay(250);
  tone(BUZZER, 2000, 300);  // Tono más alto
  delay(350);
  noTone(BUZZER);
}

void sonidoError() {
  tone(BUZZER, 400, 200);  // Tono grave
  delay(250);
  tone(BUZZER, 400, 200);  // Tono grave
  delay(250);
  noTone(BUZZER);
}