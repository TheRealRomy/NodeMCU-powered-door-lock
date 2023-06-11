// Libraries
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

// Variables
const char* ssid = "Java ";
const char* password = "lunaanddexter";
const char* serverAddress = "192.168.100.4";
const int serverPort = 5000;

// Objects 
ESP8266WebServer server(80);
WiFiClient client;
Servo servo;

// Functions 
// Open door post request
void handleOpenDoorRequest() {
  rotateServo();
  server.send(200, "text/plain", "Open door request sent!");
}

// Door knob rotation
void rotateServo() {
  servo.write(180);
  delay(500);
  servo.write(0);
  delay(400);
  servo.write(90);
}

void setup() {
  // Setting the NodeMCU in station mode
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  // Wifi connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  // Server connection
  while (!client.connect(serverAddress, serverPort)) {
    delay(2000);
  }

  client.println("POST /nodemcu-startup HTTP/1.1");
  client.println();
  client.flush();
  servo.attach(D1);

  server.on("/open-door", handleOpenDoorRequest);
  server.begin();
}

void loop() {
  server.handleClient();
}
