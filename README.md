# Huffman compression

allan.sioson@gmail.com

This is my implementation of Huffman coding as a class python. Driver programs
are provided to demonstrate compression and decompression.

The huff file has the following format:

    1. Header (1028 bytes)
       a. size of original file (4 bytes, little-endian)
       b. frequency counts of 256 byte values ((4 bytes, little-endian) x 256)
    2. Compressed data using huffman coding

