import Models_classes as Mo
from sqlalchemy.orm import joinedload


data = Mo.data
conn = data.engine.connect()
hamdy = Mo.Student(name='Hamdy Twahry', CIN=11918936, num_tel=96254959, photo_folder_path='/home/pi/jasper/client/Data/s1')
data.session.add(hamdy)
data.session.commit()
amani = Mo.Student(name='Amani Younsi', CIN=72132540, num_tel=23380399, photo_folder_path='/home/pi/jasper/client/Data/s2')
data.session.add(amani)
data.session.commit()
II2A = Mo.Class(name='II2A', emploi_path='/home/pi/jasper/pcd/Data/Schedules/II2A/schedule.png')
II2A.students.append(hamdy)
data.session.add(II2A)
data.session.commit()

row = data.session.query(Mo.Class).all()
print(row)

stud = data.session.query(Mo.Student).all()
print(stud)


