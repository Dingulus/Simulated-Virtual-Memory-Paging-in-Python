import sys

if len(sys.argv) < 1:
    print ("Usage: python filename.py <input.txt>")
    sys.exit(1)

arg1 = sys.argv[1]
mainMemory = []
mainMemoryVPN = []
mainMemoryReferenceBit = []
mainMemoryDirtyBit = []
diskReference = 0
dirtyDiskWrite = 0
pageFaultCounter = 0
refReset = 0

with open(arg1) as f:
    for l in f:
        l = l.split()

        if refReset == 200:
            refReset = 0
            mainMemoryReferenceBit = [0 for value in mainMemoryReferenceBit]
        else:
            refReset += 1

        if (int(l[0]), int(l[1]) >> 9) not in mainMemory:

            #Populates mainMemory if not full. MM can hold 32 entries [0-31]. Considered as a page fault.
            if len(mainMemory) < 32: 
                mainMemory.append((int(l[0]), int(l[1]) >> 9))
                mainMemoryVPN.append(int(l[1]) >> 9)
                mainMemoryReferenceBit.append(1)
                if l[2] == 'W':
                    mainMemoryDirtyBit.append(1)
                else:
                    mainMemoryDirtyBit.append(0)
                    
            else:
                # Look for an unused page
                if 0 in mainMemoryReferenceBit:
                    for i in range(len(mainMemory)):
                        min_val = float('inf')
                        if (mainMemoryReferenceBit[i] == 0) and (mainMemoryVPN[i] <= min_val):
                            min_val = mainMemoryVPN[i]
                            index = i
                
                # Look for an unreferenced page (reference bit is 0) where the dirty bit is 0.
                elif 0 in mainMemoryReferenceBit and 0 in mainMemoryDirtyBit:
                    for i in range(len(mainMemory)):
                        min_val = float('inf')
                        if (mainMemoryReferenceBit[i] == 0) and (mainMemoryDirtyBit == 0) and (mainMemoryVPN[i] <= min_val):
                            min_val = mainMemoryVPN[i]
                            index = i
                
                # Look for an unreferenced page (reference bit is 0) where the dirty bit is 1.
                elif 0 in mainMemoryReferenceBit and 1 in mainMemoryDirtyBit:
                    for i in range(len(mainMemory)):
                        min_val = float('inf')
                        if (mainMemoryReferenceBit[i] == 0) and (mainMemoryDirtyBit == 1) and (mainMemoryVPN[i] <= min_val):
                            min_val = mainMemoryVPN[i]
                            index = i
                
                # Look for a referenced page (reference bit is 1) where the dirty bit is 0.
                elif 1 in mainMemoryDirtyBit and 0 in mainMemoryDirtyBit:
                    for i in range(len(mainMemory)):
                        min_val = float('inf')
                        if (mainMemoryReferenceBit[i] == 1) and (mainMemoryDirtyBit == 0) and (mainMemoryVPN[i] <= min_val):
                            min_val = mainMemoryVPN[i]
                            index = i

                #Look for a page that is both referenced (reference bit is 1) and dirty (dirty bit is 1).
                else:
                    for i in range(len(mainMemory)):
                        min_val = float('inf')
                        if (mainMemoryReferenceBit[i] == 1) and (mainMemoryDirtyBit == 1) and (mainMemoryVPN[i] <= min_val):
                            min_val = mainMemoryVPN[i]
                            index = i
            
                mainMemory[index] = (int(l[0]), int(l[1]) >> 9)
                mainMemoryVPN[index] = int(l[1]) >> 9
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

print(f"# of page faults: {pageFaultCounter}")
print(f"# of disk references: {diskReference}")
print(f"# of dirty disk writes: {dirtyDiskWrite}")
print(f"# of total disk references: {totalDiskReference}")

# for i in range(len(mainMemory)):
#     print(f"{mainMemory[i][0]}, {mainMemoryVPN[i]}, {mainMemoryReferenceBit[i]}, {mainMemoryDirtyBit[i]}")