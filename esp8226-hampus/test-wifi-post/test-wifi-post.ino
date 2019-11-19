#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

ESP8266WebServer server(80);

// curl -i -X POST -H 'Content-Type: application/json' -d '{"lamp-on": true}' 192.168.0.186/lamp
// curl -X POST -d '{"lamp-on": true}' http://192.168.0.186/lamp



const char* ssid = "Schwifty";
const char* password = "1415926535";

void setup() {

    Serial.begin(115200);
    WiFi.begin(ssid, password);  //Connect to the WiFi network

    while (WiFi.status() != WL_CONNECTED) {  //Wait for connection

        delay(500);
        Serial.println("Waiting to connect...");

    }

    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());  //Print the local IP

    server.on("/lamp", handleLamp); //Associate the handler function to the path

    server.begin(); //Start the server
    Serial.println("Server listening");

}

void loop() {

    server.handleClient(); //Handling of incoming requests

    send_report()

    LowPower.sleep(1000);


}


void SendReport() {

    // Check if we are Connected.
    if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status
      HTTPClient http;    //Declare object of class HTTPClient

      http.begin("http://useotools.com/");      //Specify request destination
      http.addHeader("Content-Type", "application/x-www-form-urlencoded", false, true);
      int httpCode = http.POST("type=get_desire_data&"); //Send the request

      Serial.println(httpCode);   //Print HTTP return code
      http.writeToStream(&Serial);  // Print the response body

}

}

void handleLamp() { //Handler for the body path

      if (server.hasArg("plain")== false){ //Check if body received

            server.send(200, "text/plain", "Body not received");
            return;

      }

      String message = "Body received:\n";
             message += server.arg("plain");
             message += "\n";

      server.send(200, "text/plain", message);
      Serial.println(message);
}
