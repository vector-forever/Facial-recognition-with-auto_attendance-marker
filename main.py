import face_recognition as fc
import time
import numpy as np
import cv2 as cv
import os
from tqdm import tqdm
import xlsxwriter as xls
import datetime
import mysql.connector


def sample_faces():   #Defining a function to loop through every student(actor) names
    global people, test_images, labels   #making it global so we can use it outside function
    people = []
    for name in os.listdir(r"C:\Users\vector forever\facial recogonition\project\photos"):
       people.append(name)    #making a people list of actors names

    DIR = r"C:\Users\vector forever\facial recogonition\project\photos"
    test_images = []
    labels = []
    for person in  tqdm(people,desc= 'Main Encoding: ', total= len(people)):   #using tqdm for the progress bar
        path = os.path.join(DIR, person)
        label = people.index(person)    
        time.sleep(0.00001)
        
        for img in tqdm(os.listdir(path), desc="Unit encoding", leave= False, total= len(os.listdir(path))):
            try:
                img_path = os.path.join(path, img)
                each_img = fc.load_image_file(img_path)    #loading each image from the folder
                each_img = cv.cvtColor(each_img, cv.COLOR_RGB2BGR)    #converting to BGR
                each_img_encode = fc.face_encodings(each_img)[0]    #Collecting the encoding of each image and appening it to a list
                test_images.append(each_img_encode)
                labels.append(label)    #adding index of actors as [0,0,0,0,1,1,1,1 etc...] so it would be easy to identify the recogonized actor
                time.sleep(0.00001)
            except:
                print('-------AN ERROR OCCURED-------')
                break
            
print('')
print("SAMPLES ENCODING IS IN PROGRESS...")
print('')
sample_faces()
print('')
print("SAMPLES ENCODING COMPLETED")
print('')

def get_optimal_font_scale(text, width):    #using this function to get the optimal fontScale so that it can fit images with different resolutions
    for scale in reversed(range(59,10,-1)):
        textSize = cv.getTextSize(text, fontFace=cv.FONT_HERSHEY_TRIPLEX, fontScale=scale/10, thickness=2)
        new_width = textSize[0][0]
        if (new_width <= width):
            return scale/10
        return 0.90

now = datetime.datetime.now()
date = now.strftime("%d-%m-%y")
times = now.strftime("%I:%M")

workbook = xls.Workbook("Attendance registry.xlsx")
worksheet = workbook.add_worksheet(f"Attendance for Date {date}")
worksheet.write(0,0, "Studen ID")
worksheet.write(0,1, "Name of the student")
worksheet.write(0,2, "Time of Joining")
worksheet.write(0,3, "Status")

already_joined = dict()
row,col = 1,0

cap = cv.VideoCapture(0)
while True:
    ret, test0 = cap.read()
    if not ret:
        print("Unable to recive video frame")
        break
    test2 = cv.resize(test0, (0,0), fx=0.25, fy=0.25)
    # test2 = cv.cvtColor(test2, cv.COLOR_BGR2RGB)
    try:
       testencode = fc.face_encodings(test2)[0]
       testloc = fc.face_locations(test0)[0]     #using this in order to find the location of face so that we can draw a rectangle around face in the later stage
       result = fc.compare_faces(test_images, testencode)
       facedist = fc.face_distance(test_images, testencode)    #using this to find the most similar face out of all similar([True]) faces
       facedist = facedist.tolist()    #converting it into a list so that we can find the min, which is the most similar face
       x,y,height, width = 0,0,test2.shape[0], test2.shape[1] 
   
   
       name = 'Unknown'
       if True in result:
           index = labels[facedist.index(min(facedist))]
           name = people[index]
   
       cv.rectangle(test0, (testloc[3], testloc[0]), (testloc[1], testloc[2]), (0,255,0), 2)   #using rectange function to create a rectangle around face
       x,y,height, width = 0,0,test2.shape[0], test2.shape[1]
       cv.rectangle(test0, (testloc[3]-1, testloc[0]-25), (testloc[1]+1, testloc[0]-1), (0,255,0), -1)
       fontScale = 3*(test0.shape[1]//6)
       font_size = get_optimal_font_scale(name, fontScale)
       cv.putText(test0, name, (testloc[3]+6, testloc[0]-6), cv.FONT_HERSHEY_TRIPLEX, font_size-0.4, (0,0,0), 2)
       cv.imshow("face detection", test0)
    
       if True in result:
           if name not in already_joined.keys():
               try:
                   mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "password", database = "attendance_registry")
                   mycursor = mydb.cursor()
   
                   mycursor.execute("create table attendance(Student_ID int not null primary key, Name varchar(50), Time varchar(12), Status varchar(10))")
                   query = "insert into attendance Values(%s, %s, %s, %s)"
                   record = (row, name, times, 'present')
                   mycursor.execute(query, record)
                   mydb.commit()
               except:
                   try:
                      query = "insert into attendance Values(%s, %s, %s, %s)"
                      record = (row, name, times, 'present')
                      mycursor.execute(query, record)
                      mydb.commit()
                   except:
                      mycursor.execute("delete from attendance")
                      query = "insert into attendance Values(%s, %s, %s, %s)"
                      record = (row, name, times, 'present')
                      mycursor.execute(query, record)
                      mydb.commit()
   
               worksheet.write(row,col, row)
               worksheet.write(row,col+1, str(name))
               worksheet.write(row,col+2, str(times))
               worksheet.write(row,col+3, 'Present')
               workbook.close()
               already_joined[name] = 1
               row += 1
       cv.waitKey(1)
    except:
        cv.imshow("face detection", test0)
        cv.waitKey(1)
        #end





