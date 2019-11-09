#include <dummy.h>
#include "ESP8266WiFi.h"
#include <aREST.h>
/*#include "DHT.h"*/

const char* ssid = "JML2.4Hz";
const char* password = "abcdef12345";

int x = 0;    // variable

void setup() {
  Serial.begin(9600);      // open the serial port at 9600 bps:
  WiFi.begin(ssid,password);

// The port to listen for incoming TCP connections 
#define LISTEN_PORT           80

// Create an instance of the server
aREST rest = aREST();
WiFiServer server(LISTEN_PORT);

  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");    
    }
    Serial.print("");
    Serial.print("WiFi connected");
    rest.set_id("1");
    rest.set_name("hej");
    server.begin();
    Serial.println("Server on");

    Serial.println(WiFi.localIP());
}

void loop() {  

  for(x=0; x< 64; x++){    // only part of the ASCII chart, change to suit

    // print it out in many formats:
    Serial.print("My är ");       // print as an ASCII-encoded decimal - same as "DEC"
    Serial.print(x);
    if( x == 1)
    {
      Serial.print(" korv\n");
    }else
    {
      Serial.print(" korvar\n"); 
    }
    
    delay(1000);            // delay 200 milliseconds
  }
  Serial.println("");      // prints another carriage return
}
