def getStartLengthList(byte_length,max_length):
    starts = [0]
    count = 1
    while True:
        number = byte_length * count
        if (number > max_length): starts.append(max_length);break
        starts.append(number)
        count += 1
    return starts