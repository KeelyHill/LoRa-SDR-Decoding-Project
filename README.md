# LoRa SDR Decoding Project

Decoding LoRa signals from an Adafruit module with GNURadio and RTL-SDR.

**Paper abstract**  
LoRa is a recently created patented physical layer protocol for small, low power devices. Networks are being deployed world wide as LoRa WAN (link layer). The attack surface is growing. This project begins by performing range tests of a consumer module physical (PHY) layer. Depending on the settings, up to 5 Km was achieved to transmit a frame -- at the expense of speed. 1 Km was achieved at a more reasonable rate. Along the way, how LoRa functions is discussed. Next and inexpensive RTL-SDR (software defined radio) was used to record raw transmissions from the official PHY module. These transmissions were then attempted (and successfully) demodulated and decoded using GNU Radio and the experimental gr-lora out-of-tree module from Bastille Research. Some common radio vulnerabilities are discussed in relationship with LoRa as a conclusion.

A semester project for Digital Forensics.

Copyright&copy; 2018 Keely Hill  
License: MIT
