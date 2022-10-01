import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "password", database = "attendance_registry")
mycursor = mydb.cursor()

mycursor.execute("create table attendance(Student_ID int not null primary key, Name varchar(50), Time varchar(12), Status varchar(10))")