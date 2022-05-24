#include<LiquidCrystal.h>
#include <SoftwareSerial.h>


#define splash splash1

#define python Serial

#define RX 3
#define TX 2
SoftwareSerial ard_node(RX, TX);

LiquidCrystal lcd(13, 12, 11, 10, 9, 8);

#define gsr A0




String IncomingData = "";

int gsr_r;
int  dis_t = 550;
int disp = dis_t ;

int py_send = 0;

String prev_Rec = "Neutral";
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  ard_node.begin(115200);
  python.begin(115200);

  LcDSet();

  splash(0, "Initializing");
  splash(1, "Python");
  delay(8000);
  python.println("Ready");
  lcd.clear();


}

void LcDSet() {

  lcd.begin(16, 2);
  splash(0, "Emotion Based");
  splash(1, "Teaching  System");
  delay(3000);
  splash(0, "For Autistic");
  splash(1, "Children's");
  delay(3000);

}

void loop() {
  // put your main code here, to run repeatedly:
  getSensor();

  getPython();


  disp++;
  //  Serial.println(disp);
  if (disp > dis_t) {
    lcd.setCursor(0, 0);
    lcd.print("GSR :       ");
    lcd.setCursor(5, 0);
    lcd.print(gsr_r);
    splash(1, "");
    if (py_send) {
      python.print("GSR:");
      python.println();
      python.print(gsr_r);
      python.println();
    }
    
    ard_node.print(gsr_r);
    ard_node.print(",");
    ard_node.print(prev_Rec);
    ard_node.print(",");
    Serial.println();
    disp = 0;
  }

  delay(2);
}

void getPython() {
  if (python.available())
  {
    IncomingData = python.readStringUntil('$');

    delayMicroseconds(5);
  }
  if (IncomingData.length() > 0) {

    python.println(IncomingData);
    splash(1, IncomingData);
    if (IncomingData == "PyreC") {
      py_send = 1;prev_Rec = "Neutral";
    }
    if (IncomingData == "PyreS") {
      py_send = 0;
    }


    if (IncomingData == "Sad" )
    {
      prev_Rec = "Sad"; py_send = 0;

    }
    else if (IncomingData == "Happy" )
    {
      prev_Rec = "Happy"; py_send = 0;

    }
    else if (IncomingData == "Neutral" )
    {
      prev_Rec = "Neutral";py_send = 1;

    }

    IncomingData = "";

  }

}

void getSensor() {

  gsr_r = analogRead(gsr);

  gsr_r = map(gsr_r, 0, 1023, 100, 0);
  if (gsr_r <= 36) {
    gsr_r = 0;
  }

}
