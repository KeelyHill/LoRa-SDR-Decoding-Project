/** Payload code */

#include "compile_picker.cpp"

#if DOLISTENER==false

#include <SPI.h>
#include <LoRa.h>

#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3

#define RF95_FREQ 915E6

#define VBATPIN A7

#define LED_WHEN_TRANSMITTING LED_BUILTIN


void setup() {
	pinMode(RFM95_RST, OUTPUT);
	digitalWrite(RFM95_RST, HIGH);

	// while (!Serial);
	Serial.begin(9600);
	delay(100);

	Serial.println("LoRa RX Test");

	// manual reset
	digitalWrite(RFM95_RST, LOW);
	delay(10);
	digitalWrite(RFM95_RST, HIGH);
	delay(10);

	LoRa.setPins(RFM95_CS, RFM95_RST, RFM95_INT);


	if (!LoRa.begin(RF95_FREQ)) {
    	Serial.println("Starting LoRa failed!");
    	while (1);
  	}
	Serial.println("OK LoRa radio init");

	LoRa.setSpreadingFactor(8);
	LoRa.setSignalBandwidth(125E3);
	LoRa.setCodingRate4(5); // 5-8, inclusive
	LoRa.setPreambleLength(8);

	LoRa.enableCrc();
	// LoRa.disableCrc();
}

int16_t packetnum = 0;  // packet counter, we increment per transmission
unsigned long startTransTime;

void loop() {

	// #if CSV_NOT_HUMAN==true
		char radiopacket[36];
		// itoa(packetnum++, radiopacket, 10); // int to string base 10

		float measuredvbat = analogRead(VBATPIN);
		measuredvbat *= 6.6; // 2 * 3.3volts
		measuredvbat /= 1024; // convert to voltage
		int miliVolts = (int)(measuredvbat * 1000); // can be int16_t

		int time_sec = millis() / 1000;

		// make packet
		// sprintf(radiopacket, "%d,%d,%d,abc123xyz", packetnum++, miliVolts, time_sec);

		radiopacket[36-1] = 0; // null termination
		Serial.print("Sending: "); Serial.println(radiopacket);

		digitalWrite(LED_WHEN_TRANSMITTING, HIGH);
		startTransTime = millis();

		LoRa.beginPacket(true); // true for implicitHeader
		// LoRa.print("\x12\x34\x56\x9a\xbc");
		uint8_t pkt[] = {0x12,0x34,0x56,0x9a,0xbc,0x00};
		LoRa.write(pkt, 6);
		// LoRa.print(radiopacket); // use write() for uint8_t
		bool hadSuccess = LoRa.endPacket();

		Serial.print("success?: ");
		Serial.println(hadSuccess);

	// #else
		// char radiopacket[14] = "Hello #      "; // 19 long + null termination
		// itoa(packetnum++, radiopacket+7, 10); // int to string base 10
		//
		// // test converting an int to its raw bytes
		// radiopacket[15] = (packetnum >> 24) & 0xFF;
		// radiopacket[16] = (packetnum >> 16) & 0xFF;
		// radiopacket[17] = (packetnum >> 8) & 0xFF;
		// radiopacket[18] = packetnum & 0xFF;
		//
		// Serial.print("Sending: "); Serial.println(radiopacket);
		// radiopacket[19] = 0; // null termination
		//
		// digitalWrite(LED_WHEN_TRANSMITTING, HIGH);
		// startTransTime = millis();
		//
		// rf95.send((uint8_t *)radiopacket, 20);
	// #endif

	// Serial.println("Waiting for packet to complete...");

	digitalWrite(LED_WHEN_TRANSMITTING, LOW);
	Serial.print("Done transmitting, ");
	Serial.print((float)(millis() - startTransTime) / 1000);
	Serial.println(" sec. to complete.\n");

	delay(500);
}

#endif
