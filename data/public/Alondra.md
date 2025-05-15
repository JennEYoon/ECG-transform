
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

