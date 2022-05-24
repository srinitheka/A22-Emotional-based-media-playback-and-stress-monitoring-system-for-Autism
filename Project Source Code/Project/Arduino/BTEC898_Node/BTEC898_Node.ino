#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include "ThingSpeak.h"






#define RX D5
#define TX D6
SoftwareSerial ard_node(RX, TX,  false, 256);
//SoftwareSerial ard_node;




int a, b;

char ssid1[] = "Project";
char password1[] = "1234567890";


unsigned long channelID = 1729769;
const char * writeAPIKey = "SKVCXY2A632JI8T3"; // write API key for your ThingSpeak Channel
const char* server = "api.thingspeak.com";
String th;

int gsr_r;
String prev_Rec = "Neutral";
int tup = 20;

WiFiClient client;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  ard_node.begin (115200);
  //  ard_node.begin (115200, SWSERIAL_8N1, RX, TX, false, 256);

  setupWifi();
  ThingSpeak.begin(client);

}


void setupWifi() {

  Serial.println();
  Serial.println();
  Serial.print(ssid1);
  WiFi.begin(ssid1, password1);
  Serial.print("Connecting to ");

  while (WiFi.status() != WL_CONNECTED)
  {

    delay(800);
    Serial.print(".");


  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(1000);
}

void loop() {

  getArd();


  UpdateServer();

  delay(100);
}

void getArd() {
  String SS = ""; String SSs = "";
  while (ard_node.available() > 0) {

    char S = ard_node.read();
    SS += S;
//    Serial.println(SS);
    delay(10);

  }
  if (SS.length() > 0) {
    Serial.println(SS);
    String gs = getSplitValue(SS , ',', 0);
    String emo =  getSplitValue(SS , ',', 1);
    gsr_r = gs.toInt();
    prev_Rec = String(emo);


    ard_node.flush();

  }
}
void UpdateServer() {

  tup++;
  if (tup >= 250) {

    if (client.connect(server, 80)) {
      ThingSpeak.setField(1, String(gsr_r));
      ThingSpeak.setField(2, String(prev_Rec));


      // write to the ThingSpeak channel
      int x = ThingSpeak.writeFields(channelID, writeAPIKey);
      if (x == 200) {
        Serial.println("Channel update successful.");

      }
      else {
        Serial.println("Problem updating channel. HTTP error code " + String(x));

      }
    }
    tup = 0;
  }

}
