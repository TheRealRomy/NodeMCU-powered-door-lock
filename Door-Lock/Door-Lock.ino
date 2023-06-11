#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

const char* ssid = "Java ";
const char* password = "lunaanddexter";
const char* serverAddress = "192.168.100.4";
const int serverPort = 5000;
ESP8266WebServer server(80);
WiFiClient client;
Servo servo;

void handleAnotherTest() {
  rotateServo();
  server.send(200, "text/plain", "Open door request sent!");
}

void rotateServo() {
  servo.write(180);
  delay(500);
  servo.write(0);
  delay(400);
  servo.write(90);
  Serial.println("Rotating");
}

void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");

  while (!client.connect(serverAddress, serverPort)) {
    Serial.println("Connection to server failed. Retrying...");
    delay(2000);
  }

  Serial.println("Connected to server");

  client.println("POST /nodemcu-startup HTTP/1.1");
  client.println();
  client.flush();
  servo.attach(D1);

  server.on("/open-door", handleAnotherTest);
  server.begin();

  Serial.println("Web server started");
}

void loop() {
  server.handleClient();
}
