#!usr/bin/python

import sys
import random

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]] # [2:] to chop off the "0b" part 

if((len(sys.argv)) < 2):
    raise Exception("Too few arguments")

if not (sys.argv[1].startswith("0x")):
    raise Exception("call id must start with 0x and must be bcd-code (example: 301 = 0x301)")


preamble = 0xaaaaaaaaaaaa1234a30c
rolling_code = random.randint(0, 15)
separator= 0x01
cid = int(sys.argv[1][2:],16)

nb_chiffre_significatif = 0

if cid&0xF00 > 0:
    nb_chiffre_significatif += 1
if cid&0x0F0 > 0:
    nb_chiffre_significatif += 1
if cid&0x00F > 0:
    nb_chiffre_significatif += 1

checksum1 = rolling_code+nb_chiffre_significatif-5

if(checksum1 < 0):
    checksum1 = checksum1+16
    
    
if (((cid&0xF00) >> 8) > (cid&0x00F)):
  checksum2 = ((cid&0xF00) >> 8)-1
elif (((cid&0xF00) >> 8)==0) and (cid&0x00F == 0):
  checksum2 = 0xF
elif ((cid&0x00F) > ((cid&0xF00)>>8)):
  checksum2 = (cid&0x00F)-1

trame = int(preamble)<<72|int(rolling_code)<<68|int(separator)<<60|int(cid)<<48|int(checksum1)<<44|int(checksum2)<<40

print(rolling_code)
print(hex(trame))

newFileBytes = bitfield(trame)
newFileBytes.insert(0,0)

trailing_zeroes = [b'0', b'0', b'0']

data = newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+newFileBytes+trailing_zeroes

data.insert(0,0)

newdata = data[ : -31]

newFile = open("trame.dat", "wb")

newFileByteArray = bytearray(newdata)
newFile.write(newFileByteArray)

