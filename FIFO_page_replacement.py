import sys

if len(sys.argv) < 1:
    print ("Usage: python filename.py <input.txt>")
    sys.exit(1)

arg1 = sys.argv[1]
mainMemory = []
# mainMemory structure (each element): (Process #, VPN)
mainMemoryReferenceBit = []
mainMemoryDirtyBit = []
diskReference = 0
pageFaultCounter = 0
FIFO_counter = 0

with open(arg1) as f:
    for l in f:
        l = l.split()
        if (int(l[0]), int(l[1]) >> 9) not in mainMemory:
            if len(mainMemory) < 32:
                mainMemory.append((int(l[0]), int(l[1]) >> 9))
                mainMemoryReferenceBit.append(1)
                if l[2] == 'W':
                    mainMemoryDirtyBit.append(1)
                else:
                    mainMemoryDirtyBit.append(0)
            if l[2] == 'W':
                index = mainMemory.index((int(l[0]), int(l[1]) >> 9))
                mainMemoryDirtyBit[index] = 1
            pageFaultCounter += 1
            diskReference += 1
        else:
            pass

print(mainMemory)
print(pageFaultCounter)
print(mainMemoryReferenceBit)
print(mainMemoryDirtyBit)
print(diskReference)