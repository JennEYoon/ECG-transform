# big-endian and little-endian  
By Crystal Bedell  
https://www.techtarget.com/searchnetworking/definition/big-endian-and-little-endian  

What is big-endian and little-endian?
The term endianness describes the order in which computer memory stores a sequence of bytes. Endianness can be either big or small, and the adjectives refer to the value stored first.

Big-endian is an order in which the big end -- the most significant value in the sequence -- is first, at the lowest storage address. Little-endian is an order in which the little end, the least significant value in the sequence, is first.

### The case for big-endian
A big-endian computer would store the two bytes required for the hexadecimal number 4F52 as 4F52 in storage. For example, if 4F is stored at storage address 1000, 52 will be at address 1001. A little-endian system would store them as 524F, with 52 at address 1000 and 4F at 1001.

For people who use languages that read left-to-right, big-endian seems like the natural way to think of storing a string of characters or numbers -- in the same order people expect to see it presented to them. In this way, many people consider big-endian as storing something in a forward fashion, just as they read.

### The case for little-endian
An argument for little-endian order is that as the numeric value increases, additional digits might need to be added to the left. For example, a higher nonexponential number has more digits, so an addition of two numbers often requires moving all the digits of a big-endian ordered number in storage. This addition moves everything to the right.

In a number stored in little-endian fashion, the least significant bytes can stay where they are and new digits are added to the right at a higher address. This means some computer operations might be simpler and faster to perform.
