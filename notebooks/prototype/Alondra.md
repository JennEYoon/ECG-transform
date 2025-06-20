
Alondra, March 18, 2025 

Hello, 
the datasheet of the device measures the signals as:
0x800000 represented the most negative value (-VREF).
0x000000 represented 0V.
0x7FFFFF represented the most positive value (+VREF)

Are you using hexadecimal?
yes

Looks good. If you can send me a file with 8 signals, any length of time, that would be great.  10 seconds to 60 seconds work well.


fig1 

Is the units microvolts?
yes milivolts


Looks good. If you can send me a file with 8 signals, any length of time, that would be great.  10 seconds to 60 seconds work well.

sure, Do you already know how the sensor samples are structured?
Not sure.
Don't know what that means.  I can convert binary numbers to floating point base 10.


Is how the data is received from the device

fig2 Structure of next samples

fig3 ECG message structure  

Do you have a file with outputs from the prototype ecg device?  If I can get a copy I can take a look at it.  I will have questions about the data structure and number formats but maybe easier to understand after I get the file.  If Vadim has a copy, same one may work.

htx.txt file  (10 blocks, 125 sample per half second, 5 second total recording)  
every 125 samples we have a 20 bytes header, that you can ignore for now...

Here the header say is 16 bytes, but right now is: 20

Other detail is that ESP32 is a Little Endian architecture, the bytes are stored in memory in reverse order from what you wrote:

Byte 0 -> F4
Byte 1 -> 12
Byte 2 -> FA
Byte 3 -> FA
Byte 4 -> 44
Byte 5 -> A4
Byte 6 -> 00
Byte 7 -> 00

this is the device ID:  0000A444FAFA12F4

That's a good point. Thanks for letting me know it's Little Endian

What is the time interval for each row?  Or is the time interval one block of numbers? Where there is empty row?

yes, the empty row separates each 125 samples

also I add a "." that means the end of the 125 samples

Is there a time measure? 125 samples per second per signal lead? Or something else?
125 every half second

Ok thanks.  If this file has 8 leads, are they always in the same order? In terms of body contact points V1 ... V6, limb 1, etc?
Or maybe that does not matter at this point?

yes, Jason told me that lead1 is right to left arm, lead2 is right arm to left leg. the others are for the v's

Ok that's great.  I can go from here. Thank you for explaining it to me.  Take care, Jennifer 😊

no problem, have a nice day :)
You too.  🌞sun  

### 5/15 Th update:  
Header bytes are 20 not 16, in updated chip specs.  
Device ID 8 bytes, random init 4 bytes, Unix Date-time 8 bytes.  
OK now everything fits in Feb 19 hex recording.  

Today's 2 hex files, together is 7mb, I think not repeat yesterday's binary file.  
So 15 samples, 10 seconds long, each block ends with "DONE". 125 numbers x 8 channels per half second, 300 hertz per second x 8 channels. Lead 1 to 8 in order, Rt.arm-Lf.arm, Rt.arm-Lf.leg, V1, V2, V3, V4, V5, V6.  

Yesterday's binary unbroken text file, 7mb.  
Can now convert to hex with confidence. 
20 header bytes, 125 samples, 27-byte data (8 channel).  
Each half second sample ends in "DONE"   
"\"\   
I can convert later if Alondra does not convert to hex first.  
14.7 samples, 10 seconds long.

Together will make about 30 samples, each 10 seconds long, taken from one human, Alondra.  
Enough sample size to meet large or large numbers and central tendency minimal threshold.  
Healthy young woman subject, recorded over a 2-day period.  

### My message to Alondra, 5/15/2025  
Hi Alondra,  Is there extra 4 bytes at the beginning of each sample that should be removed? I am off by 4 extra bytes.
From previous hex text file, 5 second recording:  
F4 12 FA FA 44 A4 00 00 00 00 00 00 B8 64 B6 67 DC DD C9 3F C0 00 00 FD 7D E9 F1 54 1B 54 A0 C6 80 00 00 80 00 00 80 00 00 3A 7B 5D E1 9D 5A C0 00 00 FD 8A 41 F1 5C D3 54 BA BA 80 00 00 80 00 00 80 00 00 3A 13 C0 E0 D3 77 C0 00 00 FD 89 E2 F1 72 F2 54 F2 85 80 00 00 80 00 00 80 00 00 3A 36 6F E1 FC 85 C0 00 00 FD 84 B9 F1 71 32 50 1B 70 80 00 00 80 00 00 80 00 00 2F 41 47 D9 83 68 C0 00 00 FD 83 77 F1 5E 68 48 8D C7 80 00 00 80 00 00 80 00 00 19 E1 F1 C7 64 E7 C0 00 00 FD 89 96 F1 5B 39 4C 77 40 80 00 00 80 00 00 80 00 00 19 37 E5 C6 35 7F C0 00 00 FD 8B B0 F1 71 7B 55 84 BD 80 00 00 80 00 00 80 00 00 2C BE BE D6 80 19 C0 00 00 FD 84 45 F1 72 B8 56 4D B8 80 00 00 80 00 00 80 00 00 31 FB EC DB C4 8D C0 00 00 FD 81 81 F1 5F EC 56 21 25 80 00 00 80 00 00 80 00 …


After removing 16 bytes at the beginning of each line, and the final "." period, I get 3379 bytes.  In groups of 27 byper per sample x 125 samples should be 3375. remainder = 3379 % 125. I get 4 as remainder.  There is a group of "80 00 00 80 00 00 80 00 00" that repeats every 27th byte, so I know one sample is 27 bytes. But I don't know where the data begins. Either there are 4 extra bytes at the beginning (after 16 header bytes), or 4 extras at the end of 125 samples.

Thanks. If you can convert the binary files you sent me yesterday into hex format, like the first file you sent, that would be good.
This is the first 20 bytes: F4 12 FA FA 44 A4 00 00 00 00 00 00 B8 64 B6 67 DC DD C9 3F.

F4 12 FA FA 44 A4 00 00 00 00 00 00 B8 64 B6 67 DC DD C9 3F C0 00 00 FD 7D E9 F1 54 1B 54 A0 C6 80 00 00 80 00 00 80 00 00 3A 7B 5D E1 9D 5A C0 00 00 FD 8A 41 F1 5C D3 54 BA BA 80 00 00 80 00 00 80 00 00 3A 13 C0 E0 D3 77 C0 00 00 FD 89 E2 F1 72 F2 54 F2 85 80 00 00 80 00 00 80 00 00 3A 36 6F E1 FC 85 C0 00 00 FD 84 B9 F1 71 32 50 1B 70 80 00 00 80 00 00 80 00 00 2F 41 47 D9 83 68 C0 00 00 FD 83 77 F1 5E 68 48 8D C7 80 00 00 80 00 00 80 00 00 19 E1 F1 C7 64 E7 C0 00 00 FD 89 96 F1 5B 39 4C 77 40 80 00 00 80 00 00 80 00 00 19 37 E5 C6 35 7F C0 00 00 FD 8B B0 F1 71 7B 55 84 BD 80 00 00 80 00 00 80 00 00 2C BE BE D6 80 19 C0 00 00 FD 84 45 F1 72 B8 56 4D B8 80 00 00 80 00 00 80 00 00 31 FB EC DB C4 8D C0 00 00 FD 81 81 F1 5F EC 56 21 25 80 00 00 80 00 00 80 00 00 31 C1 A7 DA E7 60 C0 00 00 FD 8B CE F1 5C 2C 56 0A FE 80 00 00 80 00 00 80 00 00 31 2B E4 D9 7D 60 C0 00 00 FD 91 1B F1 72 E1 56 51 C9 80 00 00 80 00 00 80 00 00 31 51 80 DA 58 0D C0 00 00 FD 86 8A F1 76 1A 56 7A 9D 80 00 00 80 00 00 80 00 00 31 FF FF DB F6 A8 C0 00 00 FD 80 FE F1 62 C9 56 58 8F 80 00 00 80 00 00 80 00 00 31 CD DE DB 67 59 C0 00 00 FD 88 49 F1 58 5C 56 3D F7 80 00 00 80 00 00 80 00 00 31 2A 1A D9 D1 7E C0 00 00 FD 8F 17 F1 6C 19 56 83 82 80 00 00 80 00 00 80 00 00 31 58 13 DA 72 75 C0 00 00 FD 84 FE F1 74 A0 56 A9 EC 80 00 00 80 00 00 80 00 00 32 20 0C DC 4A C6 C0 00 00 FD 7D 4C F1 62 BF 56 8D 31 80 00 00 80 00 00 80 00 00 32 0E E5 DC 20 21 C0 00 00 FD 81 CB F1 53 76 56 5F 23 80 00 00 80 00 00 80 00 00 31 34 28 DA 48 CB C0 00 00 FD 8A C4 F1 63 B4 56 12 17 80 00 00 80 00 00 80 00 00 30 28 DC D9 90 B7 C0 00 00 FD 81 10 F1 6E FD 56 98 6C 80 00 00 80 00 00 80 00 00 32 1D 5F DC 6F CD C0 00 00 FD 76 17 F1 5D E4 56 21 28 80 00 00 80 00 00 80 00 00 38 97 1F E2 1E 8B C0 00 00 FD 78 DC F1 4C 6A 55 CE 8D 80 00 00 80 00 00 80 00 00 3B 0A 63 E3 1D D9 C0 00 00 FD 83 29 F1 57 C2 55 F6 35 80 00 00 80 00 00 80 00 00 3B 01 9A E2 E7 75 C0 00 00 FD 7D BF F1 69 35 56 38 C7 80 00 00 80 00 00 80 00 00 3B B6 7F E4 AB A6 C0 00 00 FD 73 3B F1 5D 53 56 2C B3 80 00 00 80 00 00 80 00 00 3B F9 12 E5 49 03 C0 00 00 FD 73 16 F1 49 15 55 FD DC 80 00 00 80 00 00 80 00 00 3B 67 D8 E3 C7 56 C0 00 00 FD 7E C3 F1 4F F5 56 16 AB 80 00 00 80 00 00 80 00 00 3A FD 9F E2 F8 53 C0 00 00 FD 7D 0C F1 65 55 56 60 97 80 00 00 80 00 00 80 00 00 3B A4 0F E4 9D CF C0 00 00 FD 73 00 F1 5E 93 56 60 FC 80 00 00 80 00 00 80 00 00 3C 11 5C E5 A2 1A C0 00 00 FD 71 63 F1 4A 45 56 32 08 80 00 00 80 00 00 80 00 00 3B A5 48 E4 6E 22 C0 00 00 FD 7B 51 F1 4A B8 56 39 51 80 00 00 80 00 00 80 00 00 3B 1E 2F E3 48 EE C0 00 00 FD 7C AF F1 60 F0 56 85 A4 80 00 00 80 00 00 80 00 00 3B A5 48 E4 AE B9 C0 00 00 FD 72 2C F1 5F 5B 56 93 F2 80 00 00 80 00 00 80 00 00 3C 2D 4E E6 06 A4 C0 00 00 FD 6E D7 F1 4B C7 56 79 B1 80 00 00 80 00 00 80 00 00 3B 7D 6D E4 D8 BE C0 00 00 FD 79 35 F1 48 7F 56 EA EE 80 00 00 80 00 00 80 00 00 36 21 B3 DF 63 FB C0 00 00 FD 7E A3 F1 5F 3B 54 F1 21 80 00 00 80 00 00 80 00 00 2F 99 45 DA 9E 5C C0 00 00 FD 73 AA F1 62 2A 53 9B A6 80 00 00 80 00 00 80 00 00 29 BE D2 D6 C8 44 C0 00 00 FD 75 8C F1 54 C0 4A 16 FB 80 00 00 80 00 00 80 00 00 3C D9 C2 CE 49 D7 C0 00 00 FD 7E 26 F1 4E E5 4A 09 AB 80 00 00 80 00 00 80 00 00 3C 1F C5 CC C9 D2 C0 00 00 FD 84 70 F1 63 04 4A 4C C4 80 00 00 80 00 00 80 00 00 3C 53 92 CD A4 5E C0 00 00 FD 7C 1B F1 69 DD 4A 6F 94 80 00 00 80 00 00 80 00 00 3C BF DF CF 1E B3 C0 00 00 FD 77 C0 F1 5A 82 4A 48 2E 80 00 00 80 00 00 80 00 00 3C 65 A0 CE A2 BD C0 00 00 FD 7F 5C F1 50 CB 49 EB F2 80 00 00 80 00 00 80 00 00 3A 9F 7E CC 3F BB C0 00 00 FD 86 FF F1 61 E7 4A 3D FB 80 00 00 80 00 00 80 00 00 3C 59 28 CE 0A 93 C0 00 00 FD 7F AF F1 6C C9 49 FC 03 80 00 00 80 00 00 80 00 00 43 A9 EE D5 2B 86 C0 00 00 FD 7A 4B F1 5F A6 49 CB 5A 80 00 00 80 00 00 80 00 00 46 40 98 D7 4C 52 C0 00 00 FD 80 00 F1 53 3E 49 A7 44 80 00 00 80 00 00 80 00 00 45 A0 76 D5 B3 72 C0 00 00 FD 8B E0 F1 62 AB 49 D6 33 80 00 00 80 00 00 80 00 00 45 60 C2 D5 98 E6 C0 00 00 FD 87 6D F1 73 22 4A 0F AC 80 00 00 80 00 00 80 00 00 45 DE 69 D7 3F 8E C0 00 00 FD 7E E6 F1 67 42 4A 02 85 80 00 00 80 00 00 80 00 00 45 DD B4 D7 84 2C C0 00 00 FD 80 98 F1 56 E3 49 DA 02 80 00 00 80 00 00 80 00 00 45 43 1C D5 EC 3B C0 00 00 FD 8C C9 F1 60 D7 49 FA E4 80 00 00 80 00 00 80 00 00 44 EC C7 D5 4E E0 C0 00 00 FD 8B 32 F1 74 26 4A 3D D5 80 00 00 80 00 00 80 00 00 45 5C 0A D6 DF 3F C0 00 00 FD 83 62 F1 6D CA 4A 6F E5 80 00 00 80 00 00 80 00 00 43 D5 D7 D6 45 26 C0 00 00 FD 84 25 F1 5D 72 4A 7F 4D 80 00 00 80 00 00 80 00 00 3C BB 0B CF CA 8F C0 00 00 FD 8F FD F1 62 CD 47 42 34 80 00 00 80 00 00 80 00 00 32 85 96 C8 BC F6 C0 00 00 FD 8D 85 F1 74 44 4A 0F AC 80 00 00 80 00 00 80 00 00 34 D0 68 CA AA 86 C0 00 00 FD 85 E4 F1 72 31 4B 65 39 80 00 00 80 00 00 80 00 00 3A CB B1 CF B0 F4 C0 00 00 FD 83 A5 F1 60 AE 4B 3E 82 80 00 00 80 00 00 80 00 00 3A 7E E1 CE C9 22 C0 00 00 FD 8C 72 F1 5E 5B 4B 3B 23 80 00 00 80 00 00 80 00 00 3A 07 81 CD A7 76 C0 00 00 FD 8F 3B F1 72 E3 4B 82 F7 80 00 00 80 00 00 80 00 00 3A 59 54 CE B9 5A C0 00 00 FD 85 9C F1 73 AA 4B 99 15 80 00 00 80 00 00 80 00 00 3A AB 33 CF D6 6B C0 00 00 FD 80 F0 F1 61 03 4B 74 C6 80 00 00 80 00 00 80 00 00 3A 5D 7A CF 26 09 C0 00 00 FD 88 3F F1 59 8F 4B 69 10 80 00 00 80 00 00 80 00 00 39 94 88 CD A4 ED C0 00 00 FD 8C EA F1 6B EC 4B AD 1C 80 00 00 80 00 00 80 00 00 39 A7 1B CE 5E 1E C0 00 00 FD 82 E1 F1 70 77 4B D0 42 80 00 00 80 00 00 80 00 00 3A 15 56 CF D9 51 C0 00 00 FD 7B C0 F1 5E BA 4B B1 1C 80 00 00 80 00 00 80 00 00 39 FE 8F CF 9E 00 C0 00 00 FD 80 D4 F1 53 19 4B 6D 42 80 00 00 80 00 00 80 00 00 38 E4 73 CD C5 14 C0 00 00 FD 87 02 F1 61 A6 4B 86 3B 80 00 00 80 00 00 80 00 00 38 16 73 CD 7C 80 C0 00 00 FD 7C A2 F1 69 40 4B A4 73 80 00 00 80 00 00 80 00 00 3C DA FD D2 91 6B C0 00 00 FD 75 06 F1 59 FF 4B 2E AD 80 00 00 80 00 00 80 00 00 42 D7 C0 D7 91 F3 C0 00 00 FD 78 15 F1 4A EC 4B 05 5D 80 00 00 80 00 00 80 00 00 43 25 53 D6 C8 0C C0 00 00 FD 80 F6 F1 57 65 4B 32 47 80 00 00 80 00 00 80 00 00 42 F2 02 D6 A2 C9 C0 00 00 FD 7A EB F1 65 C5 4B 6C 3C 80 00 00 80 00 00 80 00 00 43 79 62 D8 3F F1 C0 00 00 FD 72 41 F1 59 99 4B 5F 56 80 00 00 80 00 00 80 00 00 43 7D 42 D8 92 B0 C0 00 00 FD 73 67 F1 48 B0 4B 37 9E 80 00 00 80 00 00 80 00 00 42 D5 AA D7 11 1F C0 00 00 FD 7D 57 F1 51 0C 4B 56 B3 80 00 00 80 00 00 80 00 00 42 6F 90 D6 7B A9 C0 00 00 FD 7A 6E F1 62 F4 4B 99 BE 80 00 00 80 00 00 80 00 00 42 E9 D9 D8 02 76 C0 00 00 FD 71 B0 F1 5A E1 4B 9D 41 80 00 00 80 00 00 80 00 00 42 FB 31 D8 A0 94 C0 00 00 FD 72 7A F1 4A 22 4B DA 4B 80 00 00 80 00 00 80 00 00 3E 9B 62 D4 45 34 C0 00 00 FD 7D 2D F1 4E 1F 4B 52 2F 80 00 00 80 00 00 80 00 00 37 C8 42 CE 85 BA C0 00 00 FD 7F 4B F1 64 C5 45 58 54 80 00 00 80 00 00 80 00 00 29 DA 8A C6 EF E3 C0 00 00 FD 6F B2 F1 5B A3 4A F8 C2 80 00 00 80 00 00 80 00 00 30 1F 04 CA C6 2F C0 00 00 FD 6F 3E F1 4A C1 4C AD 39 80 00 00 80 00 00 80 00 00 38 03 87 CF C0 B7 C0 00 00 FD 79 42 F1 49 41 4C A5 AA 80 00 00 80 00 00 80 00 00 38 09 9F CF 00 1C C0 00 00 FD 7C 40 F1 5D 96 4C EC E3 80 00 00 80 00 00 80 00 00 38 69 18 D0 1D 04 C0 00 00 FD 72 43 F1 5E 80 4D 04 47 80 00 00 80 00 00 80 00 00 38 BB 1E D1 4C 64 C0 00 00 FD 6E 7F F1 4D B8 4C E0 FF 80 00 00 80 00 00 80 00 00 38 6E DC D0 9C C4 C0 00 00 FD 76 95 F1 47 0C 4C D0 0C 80 00 00 80 00 00 80 00 00 37 D6 EB CF 37 EF C0 00 00 FD 7D 1B F1 5B 30 4D 14 A7 80 00 00 80 00 00 80 00 00 37 EE E6 CF E7 4B C0 00 00 FD 74 99 F1 61 84 4D 3A ED 80 00 00 80 00 00 80 00 00 38 37 8E D1 3D A1 C0 00 00 FD 6F 4E F1 51 44 4D 1F 01 80 00 00 80 00 00 80 00 00 37 E7 E1 D0 D2 DE C0 00 00 FD 74 F8 F1 46 07 4D 00 D0 80 00 00 80 00 00 80 00 00 37 52 0A CF 62 1E C0 00 00 FD 7D A6 F1 57 72 4C F5 F1 80 00 00 80 00 00 80 00 00 36 B0 E1 CF 37 5F C0 00 00 FD 75 40 F1 61 EB 4D 29 C6 80 00 00 80 00 00 80 00 00 37 02 31 D0 A7 FC C0 00 00 FD 6D A1 F1 52 FA 4C DB 35 80 00 00 80 00 00 80 00 00 3C 4C 40 D5 1D 4D C0 00 00 FD 72 C5 F1 46 27 4C 6F 06 80 00 00 80 00 00 80 00 00 40 A4 9F D7 BF 9A C0 00 00 FD 7D 3A F1 53 DD 4C 99 B4 80 00 00 80 00 00 80 00 00 40 ED C7 D7 FF E5 C0 00 00 FD 77 D3 F1 63 59 4C D3 4B 80 00 00 80 00 00 80 00 00 41 7A CA D9 9C 15 C0 00 00 FD 6F FE F1 58 50 4C C6 E5 80 00 00 80 00 00 80 00 00 41 86 3E D9 F4 F3 C0 00 00 FD 71 81 F1 47 B9 4C 9E 0F 80 00 00 80 00 00 80 00 00 40 DA D7 D8 72 28 C0 00 00 FD 7C D0 F1 50 3F 4C BC C1 80 00 00 80 00 00 80 00 00 40 6E 80 D7 E6 57 C0 00 00 FD 7A BB F1 62 F3 4C FF AF 80 00 00 80 00 00 80 00 00 40 E4 6F D9 70 74 C0 00 00 FD 71 9F F1 5B 0B 4C FD 50 80 00 00 80 00 00 80 00 00 41 15 2C DA 25 3D C0 00 00 FD 71 10 F1 49 5B 4C F2 E1 80 00 00 80 00 00 80 00 00 3F AC DC D8 2C 86 C0 00 00 FD 7C 6A F1 4D 95 4D 76 C5 80 00 00 80 00 00 80 00 00 39 4D 0C D2 5F 31 C0 00 00 FD 7F C3 F1 64 F1 48 EC F0 80 00 00 80 00 00 80 00 00 2E D6 ED CC 6A 02 C0 00 00 FD 70 8E F1 5C B1 49 0B 20 80 00 00 80 00 00 80 00 00 27 E8 B7 C7 D3 32 C0 00 00 FD 6D 55 F1 49 46 4D FE 6D 80 00 00 80 00 00 80 00 00 34 DA 78 D0 12 4F C0 00 00 FD 78 95 F1 47 F8 4E 05 17 80 00 00 80 00 00 80 00 00 35 E6 53 D0 2E 5A C0 00 00 FD 7C 49 F1 5C A9 4E 49 B9 80 00 00 80 00 00 80 00 00 36 54 47 D1 57 62 C0 00 00 FD 72 63 F1 5D F6 4E 61 67 80 00 00 80 00 00 80 00 00 36 BC 81 D2 A4 3F C0 00 00 FD 6E 12 F1 4C 8E 4E 3E FF 80 00 00 80 00 00 80 00 00 36 5E 17 D1 F3 2C C0 00 00 FD 75 A1 F1 45 7A 4E 2F 55 80 00 00 80 00 00 80 00 00 35 AA C4 D0 7A ED C0 00 00 FD 7B A4 F1 58 BE 4E 71 CE 80 00 00 80 00 00 80 00 00 35 C7 2C D1 25 22 C0 00 00 FD 73 4C F1 5F 76 4E 95 76 80 00 00 80 00 00 80 00 00 36 48 29 D2 A8 8C C0 00 00 FD 6E 59 F1 4F DB 4E 78 35 80 00 00 80 00 00 80 00 00 36 21 60 D2 60 7E C0 00 00 FD 74 80 F1 44 8F 4E 5D 3E 80 00 00 80 00 00 80 00 00 35 65 E5 D0 CB 76 C0 00 00 FD 7C FC F1 55 46 4E 7B 76 80 00 00 80 00 00 80 00 00 35 1A E5 D0 DB C0 C0 00 00 FD 75 8E F1 60 24 4E 6A E8 80 00 00 80 00 00 80 00 00 34 B2 08 D1 B1 83 C0 00 00 FD 6D 7D F1 50 C8 4E 69 50 80 00 00 80 00 00 80 00 00 37 8C 20 D4 2B BD C0 00 00 FD 71 54 F1 42 4E 4D D7 A2 80 00 00 80 00 00 80 00 00 3D 55 4E D8 10 65 C0 00 00 FD 7B FE F1 50 28 4D F5 47 80 00 00 80 00 00 80