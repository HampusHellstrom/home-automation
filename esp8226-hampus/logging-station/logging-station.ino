#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

// curl -i -X POST -H 'Content-Type: application/json' -d '{"lamp-on": true}' 192.168.0.186/lamp
// curl -X POST -d '{"lamp-on": true}' http://192.168.0.186/lamp


const char* ssid = "Schwifty";
const char* password = "1415926535";
const char* token = "secret";

const int NUMBER_OF_PINS = 13;
const int my_pins[] = {16, 5, 4, 0, 2, 14, 12, 13, 15, 3, 1, 10, 9};
bool input_pins[NUMBER_OF_PINS];
bool output_pins[NUMBER_OF_PINS];

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);  //Connect to the WiFi network
    while (WiFi.status() != WL_CONNECTED) {  //Wait for connection
        delay(500);
        Serial.println("Waiting to connect...");
    }
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());  //Print the local IP
    server.on("/get-data", get_data); //Associate the handler function to the path
    server.begin(); //Start the server
    Serial.println("Server listening");


}

void activate_input(int pin) {
    pinMode(my_pins[pin], INPUT);    
    input_pins[pin] = true;
}


void loop() {
    server.handleClient(); //Handling of incoming requests
    delay(1000);
}


void get_data() {

      if (server.method() == HTTP_GET){
          if (server.hasArg("token") && server.arg("token") == token) {
              Serial.println("Token recieved and is correct");
              server.send(200, "text/json", "hej");
              
          } else {
              Serial.println("Token recieved and is incorrect");
              server.send(401, "text/plain", "bad token");
          }
      } else {
          server.send(400, "text/plain", "bad request");
      }
}
