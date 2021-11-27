#! /usr/local/bin/python3

# huffman.py
# implements huffman class with methods to compresses/ decompress input file
# using huffman coding technique
# author: allan a. sioson <allan.sioson@gmail.com>

import io
import sys
import os.path
import heapq


class huff :


    def __init__(self) :
        self.code = {}
        self.data = 0
        self.dataMask = 0x80
        self.freq = [0] * 256


    def saveBit(self, f, b) :
        if b == 1 :
            self.data = self.data | self.dataMask
        if self.dataMask != 0x01 :
            self.dataMask = self.dataMask >> 1
        else :
            f.write(self.data.to_bytes(1,"little")) 
            self.dataMask = 0x80
            self.data = 0


    def genCode(self, t, b) :
        if t == None : return
        self.genCode(t[1][1], b + [0])
        if t[1][0] != -1 :
            self.code[t[1][0]] = b[:]
        self.genCode(t[1][2], b + [1])


    def makeHuff(self, arr) :
        heapq.heapify(arr)
        while len(arr) != 1 :
            a = heapq.heappop(arr)
            b = heapq.heappop(arr)
            c = [a[0]+b[0],[-1,a,b]]
            heapq.heappush(arr,c)
        return arr[0]


    def genFreqTable(self, ifname) :
        self.freq = [0] * 256
        with io.open(ifname,'rb') as f :
            b = f.read(1)
            while b != b"" :
                self.freq[int.from_bytes(b,"little")] += 1
                b = f.read(1)
        f.close()
        treeList = []
        for i in range(256) :
            if self.freq[i] > 0 :
                treeList.append([self.freq[i], [i,None,None]])
        return treeList


    def encodeFile(self, code, ifsize, ifname, ofname) :
        ofile = io.open(ofname,'wb')
        ofile.write(ifsize.to_bytes(4,"little"))
        for i in range(256) :
            ofile.write(self.freq[i].to_bytes(4,"little"))
        with io.open(ifname,'rb') as ifile :
            b = ifile.read(1)
            while b != b"" :
                for x in code[int.from_bytes(b,"little")] :
                    self.saveBit(ofile, x)
                b = ifile.read(1)
        ifile.close()
        while self.dataMask != 0x80 :
            self.saveBit(ofile,0)
        ofile.close()


    def compress(self, ifname, ofname) :
        ifsize = os.path.getsize(ifname)
        huffTree = self.makeHuff(self.genFreqTable(ifname))
        self.code.clear()
        self.genCode(huffTree,[])
        self.encodeFile(self.code, ifsize, ifname, ofname)
        ofsize = os.path.getsize(ofname)
        print('compressed = {:d}, uncompressed = {:d}'.format(ofsize,ifsize))


    def readBit(self, f) :
        if self.data == -1 :
            self.data = f.read(1)
            if self.data == b"" : return -1
            self.data = int.from_bytes(self.data,"little")
            self.dataMask = 0x80
        if self.data == b"" : return -1
        bit = 1 if ((self.data & self.dataMask) != 0) else 0
        if self.dataMask != 0x01 :
            self.dataMask = self.dataMask >> 1
        else :
            self.data = f.read(1)
            if self.data == b"" : return bit
            self.data = int.from_bytes(self.data,"little")
            self.dataMask = 0x80
        return bit


    def loadFreqTable(self, ifname) :
        self.freq = [0] * 256
        with io.open(ifname,'rb') as f :
            b = f.read(4)
            for i in range(256) :
                b = f.read(4)
                self.freq[i] = int.from_bytes(b,"little")
        f.close()
        treeList = []
        for i in range(256) :
            if self.freq[i] > 0 :
                treeList.append([self.freq[i], [i,None,None]])
        return treeList


    def decodeFile(self, huffTree, ifname, ofname) :
        ofile = io.open(ofname,'wb')
        with io.open(ifname,'rb') as ifile :
            fsize = int.from_bytes(ifile.read(4),"little")
            count = 0
            for i in range(256) : b = ifile.read(4)
            self.data = -1
            bit = self.readBit(ifile)
            ht = huffTree
            while bit != -1 :
                if bit == 0 :
                    ht = ht[1][1]
                else :
                    ht = ht[1][2]
                if ht[1][1] is None and ht[1][2] is None :
                    if count < fsize :
                        ofile.write(ht[1][0].to_bytes(1,"little"))
                        count += 1
                    ht = huffTree
                bit = self.readBit(ifile)
        ifile.close()
        ofile.close()


    def decompress(self, ifname, ofname) :
        huffTree = self.makeHuff(self.loadFreqTable(ifname))
        self.decodeFile(huffTree, ifname, ofname)
        ifsize = os.path.getsize(ifname)
        ofsize = os.path.getsize(ofname)
        print('compressed = {:d}, uncompressed = {:d}'.format(ifsize,ofsize))

