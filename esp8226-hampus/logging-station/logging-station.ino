#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

// curl -X GET 192.168.1.9/get-data?token=secret
// curl -X PATCH "192.168.1.9/set-pin-mode?pin=2&pinMode=INPUT&token=secret"

const char* wifi_ssid = "Schwifty";
const char* wifi_password = "1415926535";
const char* token = "secret";


const char* device_id = "";
const char* remote_base_url = "";
const char* remote_token = "Token <token>";

const int ONE_SECOND = 1000;

bool passive_mode = false;
bool post_intervall_period = 15 * 60 * ONE_SECOND;

int time_until_post = 0;



const int NUMBER_OF_PINS = 13;
const int my_pins[] = {16, 5, 4, 0, 2, 14, 12, 13, 15, 3, 1, 10, 9};
bool input_pins[NUMBER_OF_PINS];
bool output_pins[NUMBER_OF_PINS];

void setup() {
    Serial.begin(115200);
    WiFi.begin(wifi_ssid, wifi_password);  //Connect to the WiFi network
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
    if (!passive_mode && time_until_post <= 0) {
        post_measurement();
    }

    server.handleClient(); //Handling of incoming requests
    delay(ONE_SECOND);
    time_until_post -= ONE_SECOND;
}

void print_request() {
    Serial.println("Headers: ");
    for (int i = 0; i < server.headers(); i++) {
        Serial.print("  ");
        Serial.print(server.headerName(i));     //Get the name of the parameter
        Serial.print(": ");
        Serial.print(server.header(i));              //Get the value of the parameter
        Serial.println("");
    }
    Serial.println("Query parameters");
    for (int i = 0; i < server.args(); i++) {
        Serial.print("  ");
        Serial.print(server.argName(i));     //Get the name of the parameter
        Serial.print(": ");
        Serial.print(server.arg(i));              //Get the value of the parameter
        Serial.println("");
    }
    Serial.println("");
}



void set_pin_mode() {
      //print_request();

      if (server.method() == HTTP_PATCH && server.hasArg("pin") && server.hasArg("pinMode")){
          if (server.hasHeader("token") && server.header("token") == token) {
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
          if (server.hasHeader("token") && server.header("token") == token) {
              Serial.println("Token recieved and is correct");
              server.send(200, "text/json", current_pin_values());
          } else {
              Serial.println("Token recieved and is incorrect");
              server.send(401, "text/plain", "bad token");
          }
      } else {
          server.send(400, "text/plain", "bad request");
      }
}


char current_pin_values() {
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
    return buffer

}


void register_device() {}

void get_setup() {}


void post_measurement() {
    Serial.println("Posting measurements...");


    // Check if we are Connected.
    if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status
        HTTPClient http;    //Declare object of class HTTPClient

        http.begin(remote_base_url + "/measurement/");      //Specify request destination
        http.addHeader("Content-Type", "text/json");
        http.addHeader("Token", remote_token);
        http.addHeader("Token", remote_token);
        int httpCode = http.POST(current_pin_values()); //Send the request

        Serial.print("  Measurement: ");
        Serial.println(current_pin_values());

        Serial.print("  Response: ");
        Serial.println(httpCode);
        if (httpCode >= 200 && httpCode > 300) {
            time_until_post = post_intervall_period;
        } else if (httpCode >= 500) {
            time_until_post = post_intervall_period;
        } else {
            time_until_post = post_intervall_period / 15;
        }
    }
}



void edit_settings() {
    print_request();

    if (server.method() == HTTP_PATCH) {
        if (server.hasHeader("token") && server.header("token") == token) {

            if (server.hasHeader("mode")) {
                Serial.println("edit setting : mode");
                if (server.header("mode") == "passive") {
                    passive_mode = true;
                    Serial.println("passive_mode = true");
                    server.send(200, "text/json", '{"passive_mode"=true"}');

                } else if (server.header("mode") == "active") {
                    passive_mode = false;
                    Serial.println("passive_mode = false");
                    Serial.println("Token recieved and is incorrect");
                    server.send(200, "text/json", '{"passive_mode"=false"}');

                } else {
                    server.send(400, "text/plain", "Missing header: mode = [passive/active]");
                }
            }

            // if (server.hasHeader("post_intervall_period")) {
            //     Serial.println("edit setting : post_intervall_period");
            //     if (server.header("post_intervall_period") == "passive") {
            //         post_intervall_period = true;
            //         Serial.println("passive_mode=true");
            //         server.send(200, "text/json", '{"passive_mode"=true"}');

            //     } else {
            //         server.send(400, "text/plain", "Missing header: mode = [passive/active]");
            //     }
            // }


        } else {
            server.send(401, "text/plain", "Unautherized");
        }
    } else {
        server.send(405, "text/plain", "Only POST request allowed");
}




