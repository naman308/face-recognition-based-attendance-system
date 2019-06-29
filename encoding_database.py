import csv
import os
import shutil
import cv2
import numpy as np
import face_recognition as fc
def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
		else:
			shutil.rmtree(directory)
			os.makedirs(directory)
	except OSError:
		print('Error: creating directory'+directory)

v=cv2.VideoCapture(0)
fd=cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

print('press 1 for adding unknown faces')
choice=input('choice:')
if(choice==1):
	print('enter the name for the face')
	name=input('name:')
	print('enter the ID for face')
	faceID=input('faceID:')
	print('enter gaurdians email ID')
	email=input('email:')
	student_list=[]
	student_list.append(name)
	student_list.append(faceID)
	student_list.append(email)
	student_list.append(0)             #today attendance
	student_list.append(0)             # monthly attendance
	count=0
	foldername=str(faceID)+name
	path=r'C:\Users\User\AppData\Local\Programs\Python\Python36\project1/./'+foldername+'/'   #change path according to location of file
	path2=r'C:\Users\User\AppData\Local\Programs\Python\Python36\project1'
	createFolder(path)
	
	while(True):
		check,img=v.read()
		fl=fc.face_locations(img)
		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		face=fd.detectMultiScale(gray,1.5,4)
		#small_img=cv2.resize(img,(0,0),fx=0.25,fy=0.25)
		#rgb_img=img[:,:,::-1]
		if(len(fl)>0):
			[y1,x1,y2,x2]=fl[0]
			cv2.rectangle(img,(x2,y1),(x1,y2),(0,0,255),5)
			count+=1
			os.chdir(path)
			cv2.imwrite(name+str(count)+'.jpg',img[y1:y1+y2,x2:x2+x1])
			e=fc.face_encodings(img,fl)[0]
			name_encoding=list(e)
			name_encoding.insert(0,faceID)
			name_encoding.insert(0,name)
			print(name_encoding)
			os.chdir(path2)
			with open(r'encodings_database_csv','a') as f:
				writer=csv.writer(f)
				writer.writerow(name_encoding)
		cv2.imshow('face_detect',img)
		k=cv2.waitKey(5)
		if(k==ord('q')):
				break
		elif(count>0):
				with open(r'email_database','a') as f:
					writer=csv.writer(f)
					writer.writerow(student_list)
				print('captured')
				break
	v.release()
	cv2.destroyAllWindows()


