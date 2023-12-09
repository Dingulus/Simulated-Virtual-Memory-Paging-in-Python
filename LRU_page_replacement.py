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

LRU_counter = 0
LRU_MEM_TIME = []
LRU_SAME_TIME = []


def LRU_FIND_INDEX():
    min_time = min(LRU_MEM_TIME)
    lru_dup = False

    # duplicate last time unit value check
    id = 0
    for t in LRU_MEM_TIME:
        if t == min_time:
            LRU_SAME_TIME.append((index, mainMemoryDirtyBit[index], min_time))
            lru_dup = True
        id += 1

    # duplicate last time unit decision
    if lru_dup is False:
        return LRU_MEM_TIME.index(min_time)
    else:
        dirty_check = True in ((db == 0 or db == 1) for db in [ind[1] for ind in LRU_SAME_TIME])
        if dirty_check:
            return [ind[1] for ind in mainMemory].index(min([ind[1] for ind in mainMemory]))
        else:
            for j in [ind[0] for ind in LRU_SAME_TIME]:
                if mainMemoryDirtyBit[j] == 0:
                    return j

    LRU_SAME_TIME.clear()


with open(arg1) as f:
    for l in f:
        l = l.split()

        if (int(l[0]), int(l[1]) >> 9) not in mainMemory:
            # Main Memory can be filled
            if len(mainMemory) < 32:
                mainMemory.append((int(l[0]), int(l[1]) >> 9))
                mainMemoryReferenceBit.append(1)
                LRU_MEM_TIME.append(LRU_counter)
                if l[2] == 'W':
                    mainMemoryDirtyBit.append(1)
                else:
                    mainMemoryDirtyBit.append(0)

            # Main Memory is Full
            else:
                # Page Replacement Algorithm
                index = LRU_FIND_INDEX()
                mainMemory[index] = (int(l[0]), int(l[1]) >> 9)
                LRU_MEM_TIME[index] += 1
                mainMemoryReferenceBit[index] = 1

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
            LRU_MEM_TIME[index] += 1

        if l[2] == 'W':
            index = mainMemory.index((int(l[0]), int(l[1]) >> 9))
            mainMemoryDirtyBit[index] = 1

        LRU_counter += 1

totalDiskReference = diskReference + dirtyDiskWrite

# print(mainMemory)
# print(pageFaultCounter)
# print(mainMemoryReferenceBit)
# print(mainMemoryDirtyBit)
print(dirtyDiskWrite)
print(diskReference)
print(totalDiskReference)