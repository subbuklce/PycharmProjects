import os, sys
from stat import *
import time
import datetime
import sqlite3

#databasePath = "/home/subrahmanyam/Desktop/Photos.db"
create_schema = "create table photos( photopath text, year int, month int, day int, creationtime datetime);"
insert_schema = "insert into photos(photopath, year, month, day, creationtime) values(\"{}\", {}, {}, {}, {});"
current_month_query = "select photopath from photos where month={};"
current_day_query = "select photopath from photos where day={};"


all_pics = []
current_month = datetime.datetime.now().month
current_day = datetime.datetime.now().day

def current_month_history():
    global databasePath
    sq = sqlite3.connect(databasePath)
    cur = sq.cursor()
    full_current_month_query = current_month_query.format(current_month)
    full_current_day_query = current_day_query.format(current_day)
    cur.execute(full_current_day_query)
    day_rows = cur.fetchall()
    count = len(day_rows)
    print(" The number of pics are {}".len(count))
#    if count == 0:
#        print("unfortunately no photos found for this day.")
#        sq.close()
#        exit(0)
    if count < 5:
        cur.execute(full_current_month_query)
        rows = cur.fetchall()
        print(" The number of pics in this month are {}".len(rows))
        for row in rows:
            #print(row)
            all_pics.append(row)
    else:
        cur.execute(full_current_day_query)
        day_rows = cur.fetchall()
        print("This day pics in history are:")
        print(" This day pics in history are {}".len(day_rows))
        for days in day_rows:
            #print(days[0])
            all_pics.append(days[0])
    sq.close()

    for each_pic in all_pics:
        cmd = "eog \"{}\"".format(each_pic)
        os.system(cmd)
        exit(0)


def Create_database(directory_name):
    sq = sqlite3.connect(databasePath)
    cur = sq.cursor()
    cur.execute(create_schema)
    for dir_paths, dir_names, filenames in os.walk(directory_name):
        for each_file in filenames:
            if ".jpg" in each_file:
                file_path = os.path.join(dir_paths,  each_file)
                creation_time = os.stat(file_path).st_mtime   #modification time
                #print("filename is:", file_path," Time is:", time.ctime(creation_time))
                #all_pics.append(file_path)
                #select datetime(1614490243.5708055,'unixepoch');
                year,month,day=time.localtime(creation_time)[:-6]
                print("Full date is:",year,month,day)
                full_insert_query = insert_schema.format(file_path,year,month,day,creation_time)
                cur.execute(full_insert_query)
    sq.commit()
    sq.close()


def main(directory_name):
    #Create_database(directory_name)
    current_month_history()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage is Photo_parser.py image_location_directory database_name")
        print("python3 Photo_parser.py /mnt/subrahmanyam/Photos Deewali.db")
        exit(0)
    global databasePath
    databasePath = sys.argv[2]
    main(sys.argv[1])
