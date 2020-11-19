
def write_scores(file_name, score):
    file = open(file_name+".txt",'a')
    file.write(str(score)+'\n')
    file.close()