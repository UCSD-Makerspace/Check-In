#include "time.h"
#include <chrono>
#include <thread>
#include <SPI.h>
#include <Adafruit_PN532.h>
#include <Wire.h>
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735
#include <Adafruit_ST7789.h> // Hardware-specific library for ST7789
#include <Fonts/FreeSerif12pt7b.h>
#include <Fonts/FreeSerif18pt7b.h>
#include <Fonts/FreeSerif9pt7b.h>
#include <Fonts/FreeSerif24pt7b.h>

const long gmtOffset_sec = -25200;
const int daylightOffset_sec = 0;
// uint8_t mac_address[] = {0x30,0xc6,0xf7,0x05,0x87,0x20};

#define TFT_CS 5
#define TFT_RST 17 // Or set to -1 and connect to Arduino RESET pin
#define TFT_DC 16
#define GRAY 0x2104
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

// PN532 params

#define PN532_SS (21)
Adafruit_PN532 nfc(PN532_SS);

// Buttons

#define BUT1 36
#define BUT2 39
#define BUT3 34
#define BUT4 35

void setup()
{
    delay(500);
    Serial.begin(115200);

    pinMode(BUT1, INPUT);
    pinMode(BUT2, INPUT);
    pinMode(BUT3, INPUT);
    pinMode(BUT4, INPUT);

    nfc.begin();

    tft.init(240, 320);
    tft.setRotation(3);
    homeScreen();

    nfc.begin();

    uint32_t versiondata = nfc.getFirmwareVersion();
    if (!versiondata)
    {
        Serial.print("Didn't find PN53x board");
        while (1)
            ; // halt
    }
    // Got ok data, print it out!
    Serial.print("Found chip PN5");
    Serial.println((versiondata >> 24) & 0xFF, HEX);
    Serial.print("Firmware ver. ");
    Serial.print((versiondata >> 16) & 0xFF, DEC);
    Serial.print('.');
    Serial.println((versiondata >> 8) & 0xFF, DEC);

    // configure board to read RFID tags
    nfc.SAMConfig();
}

////////////////////////////////////////////////////////
//////////////////////   DISPLAY   /////////////////////
////////////////////////////////////////////////////////

void homeScreen()
{
    tft.setFont(&FreeSerif24pt7b);
    tft.fillScreen(ST77XX_BLACK);
    tft.setCursor(20, 40);
    tft.setTextColor(ST77XX_YELLOW);
    tft.setTextSize(1);
    tft.println("Scan Here!");
    tft.setCursor(20, 80);
    tft.println("---->");
    tft.fillRect(20, 45, tft.width() - 95, 5, ST77XX_BLUE);
    tft.fillRect(tft.width() - 52, 45, 20, 5, ST77XX_BLUE);
}

void loop()
{
    struct tm timeinfo;
    time_t nowSecs;

    uint8_t success;
    uint8_t uid[] = {0, 0, 0, 0, 0, 0, 0, 0}; // Buffer to store the returned UID
    uint8_t uidLength;
    uint64_t idnum = 0;
    // String uidStr;
    char uidStr[30] = "";

    // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
    success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength, 100);

    if (success)
    {
        tft.fillScreen(ST77XX_BLACK);
        tft.setCursor(0, 30);

        tft.setFont(&FreeSerif24pt7b);

        uint32_t szPos;

        for (szPos = 0; szPos < uidLength; szPos++)
        {
            sprintf(uidStr, "%s%02X", uidStr, uid[szPos] & 0xff);
        }
        nowSecs = time(nullptr);
        Serial.println(String(uidStr));

        tft.setTextSize(1);
    }
    delay(10);
}