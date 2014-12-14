__author__ = 'ryan'
import os
import ConfigParser

if __name__ == '__main__':
    path = "C:\\new_gdzq_v6\\T0002\\export"
    start_date = '2014-01-01'
    end_date = '2014-12-11'
    cf = ConfigParser.RawConfigParser()
    file_list = []
    for root1, dirs1, files1 in os.walk(path):
        for file_name in files1:
            file_name = file_name.lower()
            file_list.append(file_name.split(".")[0])
    cf.add_section("stocks")
    all_file = ''
    for file_name in file_list:
        cf.add_section(file_name)
        cf.set(file_name, "start", start_date)
        cf.set(file_name, "end", end_date)
        if file_name == file_list[len(file_list) - 1]:
            all_file += file_name
        else:
            all_file += file_name + ","
    cf.set("stocks", "ids", all_file)
    with open('tmp.conf', 'wb') as fp:
        cf.write(fp)

