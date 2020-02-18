#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

// curl -X GET 192.168.1.9/get-data?token=secret
// curl -X PATCH "192.168.1.9/set-pin-mode?pin=2&pinMode=INPUT&token=secret"

const char* ssid = "Schwifty";
const char* password = "1415926535";
const char* token = "secret";

File fsUploadFile;

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
    server.on("/set-pin-mode", set_pin_mode); //Associate the handler function to the path
    server.begin(); //Start the server
    Serial.println("Server listening");

    activate_input(1);
}

void activate_input(int pin) {
    Serial.print("Activating pin: ");
    Serial.print(pin);
    Serial.print(" - ");
    Serial.println(my_pins[pin]);
    pinMode(my_pins[pin], INPUT);    
    input_pins[pin] = true;
}


void loop() {
    server.handleClient(); //Handling of incoming requests
    delay(1000);
}

void print_args() {
    Serial.println("Printing all query parameters");
    for (int i = 0; i < server.args(); i++) {
        Serial.print(server.argName(i));     //Get the name of the parameter
        Serial.print(" = ");
        Serial.print(server.arg(i));              //Get the value of the parameter
        Serial.println("");
    } 
    Serial.println("");
}

void set_pin_mode() {
      //print_args();
      
      if (server.method() == HTTP_PATCH && server.hasArg("pin") && server.hasArg("pinMode")){
          if (server.hasArg("token") && server.arg("token") == token) {
              if (server.arg("pinMode") == "INPUT") {
                  activate_input(server.arg("pin").toInt());
              }
              server.send(200, "text/plain", "Pin has been activated");
          } else {
              Serial.println("Token recieved and is incorrect");
              server.send(401, "text/plain", "bad token");
          }
      } else {
          server.send(400, "text/plain", "bad request");
      }
}

void get_data() {

      if (server.method() == HTTP_GET){
          if (server.hasArg("token") && server.arg("token") == token) {
              Serial.println("Token recieved and is correct");

              char buffer[128];
              int pin_values[NUMBER_OF_PINS];
              for (int pin = 0; pin < NUMBER_OF_PINS; pin++) {
                  if (input_pins[pin] == true) {
                      pin_values[pin] = analogRead(my_pins[pin]);
                  } else {
                      pin_values[pin] = -1;
                  }
              }
              sprintf(buffer, "[%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d]", pin_values[0],pin_values[1],pin_values[2],pin_values[3],pin_values[4],pin_values[5],pin_values[6],pin_values[7],pin_values[8],pin_values[9],pin_values[10],pin_values[11],pin_values[12]);
              server.send(200, "text/json", buffer);
          } else {
              Serial.println("Token recieved and is incorrect");
              server.send(401, "text/plain", "bad token");
          }
      } else {
          server.send(400, "text/plain", "bad request");
      }
}
