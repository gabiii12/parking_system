#include <SPI.h>
#include <MFRC522.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

const int SS_PIN = 10;
const int RST_PIN = 9;
const int SERVO_PIN = 8;
const int TRIG_PIN = 6;
const int ECHO_PIN = 7;
const int green_pin = 5;
const int red_pin = 4;

MFRC522 mfrc522(SS_PIN, RST_PIN);
LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo myservo;

long duration;
int distance;

bool servoOpen = false;
bool deniedShown = false;
unsigned long servoStartTime = 0;
unsigned long deniedStartTime = 0;

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  lcd.init();
  lcd.backlight();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(green_pin, OUTPUT);
  pinMode(red_pin, OUTPUT);

  myservo.attach(SERVO_PIN);
  myservo.write(0);

  lcd.setCursor(0, 0);
  lcd.print("Place your card");
}

void ultrasonic() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.034 / 2;

  if (distance > 0 && distance <= 10) {
    digitalWrite(red_pin, HIGH);
    digitalWrite(green_pin, LOW);
  } else {
    digitalWrite(green_pin, HIGH);
    digitalWrite(red_pin, LOW);
  }
}

void loop() {
  ultrasonic();

  if (servoOpen && millis() - servoStartTime >= 3500) {
    myservo.write(0);
    servoOpen = false;
    lcd.clear();
    lcd.print("Place your card");
  }

  if (deniedShown && millis() - deniedStartTime >= 2000) {
    deniedShown = false;
    lcd.clear();
    lcd.print("Place your card");
  }

  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  String cardID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    cardID += String(mfrc522.uid.uidByte[i], HEX);
  }
  cardID.toUpperCase();

  Serial.println(cardID);
  lcd.clear();

  unsigned long startTime = millis();
  while (!Serial.available() && millis() - startTime < 3000) {
    ultrasonic();
  }

  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    String info = "";
    unsigned long waitStart = millis();
    while (!Serial.available() && millis() - waitStart < 1000) {
      ultrasonic();
    }
    if (Serial.available()) {
      info = Serial.readStringUntil('\n');
      info.trim();
    }

    if (msg == "Access Granted") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("ACCESS GRANTED");
      lcd.setCursor(0, 1);
      lcd.print(info);  // student name

      myservo.write(90);
      servoOpen = true;
      servoStartTime = millis();
    } 
    else if (msg == "Access Denied") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("ACCESS DENIED");
      lcd.setCursor(0, 1);
      lcd.print(info);  // "ID UNRECOGNIZED"

      deniedShown = true;
      deniedStartTime = millis();
    }
  } 
  else {
    lcd.clear();
    lcd.print("No response")
    delay(1000);
    lcd.clear();
    lcd.print("Place your card");
  }

  mfrc522.PICC_HaltA();
}
