def saveData(list):
    file = open('tracker_data', 'w+')
    for data in list:
        file.write("{}\n".format(data))

    file.close()

def getData():
    file = open('tracker_data', 'r')
    data_list = file.read().split('\n')
    data = list(filter(None, data_list))
    file.close()
    return data
