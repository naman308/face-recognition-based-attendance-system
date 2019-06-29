import face_recognition as fc
import cv2
import os
import csv
import numpy as np
import datetime
import smtplib
import getpass
import admin
import calendar
known_names=[]
present_today=[]
face_ID=[]
encoding=[]
known_email=[]
def email_info(attend,name,ID,to_email):
	now=datetime.datetime.now()
	subject="attendance report of "+str(now.day)+"/"+str(now.month)+"/"+str(now.year)
	if(attend==True):
		msg=name+" is present today with ID number "+str(ID)
		csvupdate(name,ID,1)
	else:
		msg=name+" is absent today with ID number"+str(ID)
		csvupdate(name,ID,0)
	send_email(subject,msg,to_email)

def send_email(subject,msg,to_email):
	try:
		email=admin.email
		password=admin.password
		server=smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(email,password)
		message='subject:{}\n\n{}'.format(subject,msg)
		server.sendmail(email,to_email,message)
		server.quit()
		print("Sucess:Email sent")
	except:
		print("Email failed")

def monthly_info(name,ID,to_email,attendance):
	now=datetime.datetime.now()
	subject="attendance report of "+str(now.month)+"/"+str(now.year)
	msg=name+" has attendance "+str(attendance)+" with ID number "+str(ID)
	lastdate=calendar.monthrange(now.year,now.month)[1]
	if(int(attendance)/lastdate<0.75):
		msg=msg+'\n'+'your attendance is low'
	send_email(subject,msg,to_email)

def csvupdate(name,ID,num):
	lines=[]
	r=csv.reader(open('email_database'))
	for row in r:
		if(row):
			print(row,'row')
			l=list(row)
			if(l[0]==name and l[1]==str(ID)):
				l[3]=str(num)
				l[4]=str(int(l[4])+num)
			lines.append(l)
	for l in lines:
                with open(r'email_database','w') as f:
                        writer=csv.writer(f)
                        for l in lines:
                                writer.writerow(l)

def monthlyreport():
	with open('email_database','r') as f:
		reader=csv.reader(f)
		for row in reader:
			if(row):
				monthly_info(row[0],row[1],row[2],row[4])

def is_time_between(begin_time,end_time):
	now=datetime.datetime.now()
	t=now.time()
	if((begin_time<=t ) and (end_time>=t)):
		return True
	else:
		return False
def open_directory():                                       
	path=r'C:\Users\User\AppData\Local\Programs\Python\Python36\project1'    #folder name is project1 change path accodring to location
	os.chdir(path)
	with open('encodings_database_csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			if(row):
				list1=[float(y) for y in row if not y.isalpha()]          #list1 contain only numeric value of list
				encoding.append(np.array(list1[1:]))
	with open('email_database','r') as f:
		reader=csv.reader(f)
		for row in reader:
			if(row):
				present_today.append(False)
				known_names.append(row[0])
				face_ID.append(int(row[1]))
				known_email.append(row[2])
open_directory()
t=is_time_between(datetime.time(9,00),datetime.time(11,00))
if(t):
	v=cv2.VideoCapture(0)
	while True:
		r,live=v.read()
		fL=fc.face_locations(live)
		if(len(fL)>0):
			[y1,x1,y2,x2]=fL[0]
			cv2.rectangle(live,(x2,y1),(x1,y2),(0,0,255),5)
			E=fc.face_encodings(live,fL)[0]
			res=fc.compare_faces(encoding,E)
			r=True in res
			print(r)
			if(r==True):
				print(known_names[res.index(True)])
				present_today[res.index(True)]=True
				print('captured')
				print(known_names[res.index(True)],face_ID[res.index(True)],known_email[res.index(True)])
				email_info(True,known_names[res.index(True)],face_ID[res.index(True)],known_email[res.index(True)])
				break
			else:
				print('unknown face')
		cv2.imshow('dfng',live)
		k=cv2.waitKey(5)
		if(k==ord('q')):
			cv2.destroyAllWindows()
			break
	                        #the student who are absent
elif(not t):
	print('attendance time is 9 to 9:30')
	for i in range(len(present_today)):
		if( not present_today[i]):
			email_info(False,known_names[i],face_ID[i],known_email[i])

now=datetime.datetime.now()                              # monthly report
lastdate=calendar.monthrange(now.year,now.month)[1]
if(now.day==lastdate):
	monthlyreport()
