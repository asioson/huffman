#! /usr/local/bin/python3

# decompress.py
# decompresses input file using huffman coding technique
# usage : ./decompress.py file
# author: allan a. sioson <allan.sioson@gmail.com>

from huffman import huff
import sys
import os

def main() :
    if len(sys.argv) != 2 :
        print('usage: ' + sys.argv[0] + ' file.huff')
    else :
        ifname = sys.argv[1]
        if not os.path.exists(ifname) :
            print('error: file "' + ifname + '" not found.')
            return 1
        if ifname[-5:] != '.huff' :
            print('error: file "' + ifname + '" is not huff compressed.')
            return 1
        ofname = ifname[:-5] + '.orig'
        if os.path.exists(ofname) :
            print('error: file "' + ofname + '" exists.')
            return 1
        h = huff()
        h.decompress(ifname, ofname)
    return 0


if __name__ == '__main__' :
    sys.exit(main())
