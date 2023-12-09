import sys
import random

if len(sys.argv) < 1:
    print ("Usage: python filename.py <input.txt>")
    sys.exit(1)

arg1 = sys.argv[1]
mainMemory = []
# mainMemory structure (each element): (Process #, VPN)
mainMemoryReferenceBit = []
mainMemoryDirtyBit = []
diskReference = 0
dirtyDiskWrite = 0
pageFaultCounter = 0

seed_value = 7
random.seed(seed_value)
with open(arg1) as f:
    for l in f:
        l = l.split()

        if (int(l[0]), int(l[1]) >> 9) not in mainMemory:
            # Main Memory can be filled
            if len(mainMemory) < 32:
                mainMemory.append((int(l[0]), int(l[1]) >> 9))
                mainMemoryReferenceBit.append(1)
                if l[2] == 'W':
                    mainMemoryDirtyBit.append(1)
                else:
                    mainMemoryDirtyBit.append(0)

            # Main Memory is Full
            else:
                index = random.randint(0, 31)
                mainMemory[index] = (int(l[0]), int(l[1]) >> 9)
                mainMemoryReferenceBit[index] = 1

                if mainMemoryDirtyBit[index] == 1:
                    dirtyDiskWrite += 1

                if l[2] == 'W':
                    mainMemoryDirtyBit[index] = 1
                else:
                    mainMemoryDirtyBit[index] = 0

            pageFaultCounter += 1
            diskReference += 1

        if l[2] == 'W':
            index = mainMemory.index((int(l[0]), int(l[1]) >> 9))
            mainMemoryDirtyBit[index] = 1

totalDiskReference = diskReference + dirtyDiskWrite

# print(mainMemory)
# print(pageFaultCounter)
# print(mainMemoryReferenceBit)
# print(mainMemoryDirtyBit)
print(dirtyDiskWrite)
print(diskReference)
print(totalDiskReference)