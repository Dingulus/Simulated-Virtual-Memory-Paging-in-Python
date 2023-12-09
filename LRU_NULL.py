import sys

if len(sys.argv) < 1:
    print ("Usage: python filename.py <input.txt>")
    sys.exit(1)

arg1 = sys.argv[1]
mainMemory = []
# mainMemory structure (each element): (Process #, VPN)
mainMemoryVPN = []
mainMemoryReferenceBit = []
mainMemoryDirtyBit = []
diskReference = 0
dirtyDiskWrite = 0
pageFaultCounter = 0
LRU_track = []

with open(arg1) as f:
    for l in f:
        l = l.split()
        if (int(l[0]), int(l[1]) >> 9) not in mainMemory:
            if len(mainMemory) < 32: #Populates mainMemory if not full. MM can hold 32 entries [0-31]. Considered as a page fault.
                mainMemory.append((int(l[0]), int(l[1]) >> 9))
                mainMemoryReferenceBit.append(1)
                mainMemoryVPN.append(int(l[1]) >> 9)
                LRU_track.append(1)
                if l[2] == 'W':
                    mainMemoryDirtyBit.append(1)
                else:
                    mainMemoryDirtyBit.append(0)

            else:
                # Checks for least recent used. If there are more than one, then check dirty bit.
                if LRU_track.count(min(LRU_track)) == 1:
                    index = LRU_track.index(min(LRU_track))
                
                # Check for non dirty pages. If there is one, choose it. If there are non or more than one, move on.
                elif mainMemoryDirtyBit.count(0) == 1:
                    index = mainMemoryDirtyBit.index(0)

                # Check for lowest page number, replace.
                else:
                    index = mainMemoryVPN.index(min(mainMemoryVPN))

                mainMemory[index] = (int(l[0]), int(l[1]) >> 9)
                mainMemoryVPN[index] = int(l[1]) >> 9
                mainMemoryReferenceBit[index] = 1
                LRU_track[index] = 1

                if mainMemoryDirtyBit[index] == 1:
                    dirtyDiskWrite += 1

                if l[2] == 'W':
                    mainMemoryDirtyBit[index] = 1
                else:
                    mainMemoryDirtyBit[index] = 0

            pageFaultCounter += 1
            diskReference += 1
        else:
            index = mainMemory.index((int(l[0]), int(l[1]) >> 9))
            LRU_track[index] += 1

        if l[2] == 'W':
            index = mainMemory.index((int(l[0]), int(l[1]) >> 9))
            mainMemoryDirtyBit[index] = 1

totalDiskReference = diskReference + dirtyDiskWrite

# print(mainMemory)
# print(pageFaultCounter)
# print(mainMemoryReferenceBit)
# print(mainMemoryDirtyBit)
print(f"# of page faults: {pageFaultCounter}")
print(f"# of disk references: {diskReference}")
print(f"# of dirty disk writes: {dirtyDiskWrite}")
print(f"# of total disk references: {totalDiskReference}")