
def write_data(file_name, data):
    file = open(file_name+".txt",'a')
    file.write(str(data)+'\n')
    file.close()