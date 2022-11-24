# Retekess TD161 Pager system control with Hack RF
https://www.retekess.com/retekess-td161-wireless-paging-system-for-food-truck/

## Introduction

This is a python code that allows control of a restaurant pager system from Retekess (Model TD-161).

## Prerequisites
 - Python 3.8
 - GNU Radio 3.10.x
 - Hack RF

## Use
In command-line, type "python3 retekess_tx.py 0x000", replace '0x000' by the desired pager ID (BCD-coded: 0x010 for pager 10).

See example: https://youtu.be/l9VuGyAM_wk

Other files:
 - fsk_tx.grc was the file used to test transmission
 - fsk_rx.grc was the file used to test reception
 - generate_trame.py output the packet and saved it to a binary file
 - protocol.proto.xml shows example of received packet from the Retekess transmitter, this can be opened in URH (https://github.com/jopohl/urh)

## Modulation
 - Modulation: 2-FSK
 - Carrier frequency: 433.92 MHz
 - Baud rate: 10000

## Packet structure
 - Start (1 bit) : 0
 - Synchronization (12 bytes): 0xAAAAAAAAAAAA
 - Preamble (8 bytes): 0x1234A30C
 - Rolling code (1 byte): 0x0 (needs to be different from last transmission) 
 - Separator (2 bytes): 0x01
 - Pager ID (3 bytes): 0x001 (BCD-coded)
 - Checksum #1 (1 byte)
   - Formula: Rolling code + number of significant byte in pager ID - 5 (if result is smaller than 0, than add 15)
   - Example if rolling code is 2 and pager ID is 0x012: (2+2-5)+15 = 14 = 0xE
  - Checksum #2 (1 byte)
   - If first byte of pager ID is larger than the third byte of pager ID, than: first byte of pager ID - 1
   - If central byte of pager ID is larger than the two other bytes, than: 0xF
   - If third byte of pager ID is larger than the first byte of pager ID, than: third byte of pager ID - 1
   
   The packet is sent ten times back to back for a total of 1500 bits.
  
