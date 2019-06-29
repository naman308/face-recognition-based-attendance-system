# face-recognition-based-attendance-system
1.first open admin.py and save your email_id(admin) and password(admin) 
2. change the path variable in  encoding_database.py and attendance.py according to current directory of project
3.run encoding_database.py then it will ask for name and unique id and email id for that name after submitting details it will store your face encoding and details of student in a  different csv file.
4.now run attendance.py it will work between specific time which can be changed through is_time_between function
5.after which email is sent to registered email id of particular student and runing attendance.py
6.if we run file in time other than is_time_between function then it will send mail to all absent student
7. at the end of month it will send message to all registered student there monthly attendance
