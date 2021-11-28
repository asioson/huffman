# Huffman compression

allan.sioson@gmail.com

This is my implementation of Huffman coding as a class in python. Driver programs
are provided to demonstrate compression and decompression.  The compression program
takes in a file (text or binary) and produce a compressed file with the '.huff' 
extension. The huff file is bit 0 padded.

The huff file has the following format:

    1. Header (1028 bytes)
       a. size of original file (4 bytes, little-endian)
       b. frequency counts of 256 byte values ((4 bytes, little-endian) x 256)
    2. Compressed data using huffman coding

Usage :

    ./compress.py file.in

    ./decompress.py file.in.huff


Notes :
 
     python3 is assumed to be located in /usr/local/bin/python3

To make the compress.py and decompress.py executable, execute the following on a Unix/Linux/MacOS bash terminal

     chmod +x compress.py

     chmod +x decompress.py


