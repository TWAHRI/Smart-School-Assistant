import Models_classes as Mo
from sqlalchemy.orm import joinedload


data = Mo.data
conn = data.engine.connect()

prof = Mo.Professor(name='jfk', CIN=87687, num_tel=5876796)
cla = Mo.Class(name='II1A', emploi_path='bla')

data.session.add(prof)
data.session.commit()
table = data.Base.metadata.tables['person']
selc_st = table.select().with_only_columns([table.c.type]).where(table.c.person_id == 1)
resl = conn.execute(selc_st)
row = resl.fetchone()
print(row['type'])

b = data.session.query(Mo.Professor).all()
print(b)

stu = Mo.Student(name='jfk', CIN=78979, num_tel=46546)
data.session.add(stu)
data.session.commit()
stu1 = Mo.Student(name='fdfg', CIN=78979, num_tel=46546)
data.session.add(stu1)
data.session.commit()
cla.students.append(stu)
cla.students.append(stu1)

data.session.add(cla)
data.session.commit()
row = data.session.query(Mo.Student).options(joinedload(Mo.Student._class)).filter(Mo.Class.class_id == 1).all()

for stu in row:
    print(stu)


b = data.session.query(Mo.Student).all()
print(b)

table = data.Base.metadata.tables['student']
del_st = table.delete().where(
    table.c.person_id == 2)
conn.execute(del_st)
data.session.commit()
table = data.Base.metadata.tables['person']
del_st = table.delete().where(
    table.c.person_id == 2)
conn.execute(del_st)
data.session.commit()
"""
table = data.Base.metadata.tables['class']
del_st = table.delete().where(
    table.c.class_id == 1)
conn.execute(del_st)
data.session.commit()
"""
b = data.session.query(Mo.Student).all()
print(b)

row = data.session.query(Mo.Student).options(joinedload(Mo.Student._class)).filter(Mo.Class.class_id == 1).all()
print('bla')
for stu in row:
    print(stu)

f = data.session.query(Mo.Student).all()
print(f)
print('bal2')

class1 = data.session.query(Mo.Class).filter(Mo.Class.class_id == 1).first()
stu = Mo.Student(name='jfk', CIN=78979, num_tel=46546)
data.session.add(stu)
data.session.commit()
class1.students.append(stu)
data.session.commit()
row = data.session.query(Mo.Student).options(joinedload(Mo.Student._class)).filter(Mo.Class.class_id == 1).all()
print('bla')
for stu in row:
    print(stu)

reu = Mo.Reunion(name='bhsk')
reu.professors.append(prof)
data.session.add(reu)
data.session.commit()
row = data.session.query(Mo.Professor).options(joinedload(Mo.Professor.reunions)).filter(Mo.Reunion.reunion_id == 1).all()
print('bl')
for p in row:
    print(p)
row = data.session.query(Mo.Reunion).options(joinedload(Mo.Reunion.professors)).filter(Mo.Professor.person_id == 1).all()
print('bl')
for p in row:
    print(p)


table = data.Base.metadata.tables['student']
del_st = table.delete().where(
    table.c.person_id > 0)
conn.execute(del_st)
data.session.commit()

table = data.Base.metadata.tables['professor']
del_st = table.delete().where(
    table.c.person_id > 0)
conn.execute(del_st)
data.session.commit()

c = data.session.query(Mo.Professor).all()

print(c)

table = data.Base.metadata.tables['person']
del_st = table.delete().where(
    table.c.person_id > 0)
conn.execute(del_st)
data.session.commit()

a = data.session.query(Mo.Person).all()
table = data.Base.metadata.tables['class']
del_st = table.delete().where(
    table.c.class_id > 0)
conn.execute(del_st)
data.session.commit()
table = data.Base.metadata.tables['reunion']
del_st = table.delete().where(
    table.c.reunion_id > 0)
conn.execute(del_st)
data.session.commit()

print(a)
