with open("test_data.txt") as f:
    for l in f:
        l = l.split()
        print(int(l[1]) >> 9)