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
dirtyDiskWrite = 0
pageFaultCounter = 0
FIFO_tracker = []
FIFO_count = 0

with open(arg1) as f:
    for l in f:
        l = l.split()

        if (int(l[0]), int(l[1]) >> 9) not in mainMemory:
            if len(mainMemory) < 32:
                mainMemory.append((int(l[0]), int(l[1]) >> 9))
                mainMemoryReferenceBit.append(1)
                FIFO_tracker.append(FIFO_count)
                FIFO_count += 1
                if l[2] == 'W':
                    mainMemoryDirtyBit.append(1)
                else:
                    mainMemoryDirtyBit.append(0)

            else:
                index = FIFO_tracker.index(0) #Gets index of oldest task
                mainMemory[index] = (int(l[0]), int(l[1]) >> 9)
                mainMemoryReferenceBit[index] = 1
                FIFO_tracker[index] = 32
                FIFO_tracker = [value - 1 for value in FIFO_tracker]

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