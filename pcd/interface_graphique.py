import sys
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Models.Models_classes as Mo
import os
from shutil import copyfile
from sqlalchemy import select, update

data = Mo.data


class Add_Prof():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.win = QWidget()
        self.err_name = QLabel("")
        self.name = QLineEdit()
        self.err_pn = QLabel("")
        self.phone_num = QLineEdit()
        self.err_cn = QLabel("")
        self.cin = QLineEdit()
        self.fileNames = QStringList()
        self.schedule = QStringList()

    def window(self):

        l1 = QLabel("Name")

        l2 = QLabel("Phone number")

        self.phone_num.setValidator(QIntValidator())
        self.phone_num.setMaxLength(8)

        l3 = QLabel("CIN")

        self.cin.setValidator(QIntValidator())
        self.cin.setMaxLength(8)

        self.err_cn.setIndent(110)
        self.err_pn.setIndent(110)
        self.err_name.setIndent(110)

        dialog = QFileDialog()

        fbox = QFormLayout()
        fbox.addRow(l1, self.name)
        fbox.addRow(self.err_name)
        fbox.addRow(l2, self.phone_num)
        fbox.addRow(self.err_pn)
        fbox.addRow(l3, self.cin)
        fbox.addRow(self.err_cn)
        sub = QPushButton("Submit")
        cancel = QPushButton("Cancel")
        Add_photos = QPushButton("Add Photos")
        Add_schedule = QPushButton("Add Schedule")
        fbox.addRow(Add_schedule)
        fbox.addRow(Add_photos)
        fbox.addRow(sub, cancel)
        Add_photos.clicked.connect(self.Add_photos_clicked)
        Add_schedule.clicked.connect(self.Add_schedule_clicked)
        sub.clicked.connect(self.sub_clicked)
        cancel.clicked.connect(self.cancel_clicked)

        self.win.setLayout(fbox)

        self.win.setWindowTitle("Add Professor")
        self.win.show()
        sys.exit(self.app.exec_())

    def sub_clicked(self):

        test = False
        self.err_cn.setText("")
        self.err_pn.setText("")
        self.err_name.setText("")

        if len(self.cin.text()) != 8:
            self.err_cn.setText("invalid CIN")
            test = True
        if len(self.phone_num.text()) != 8:
            print(test)
            self.err_pn.setText("invalid phone number")
            test = True
        z = re.compile(r"^[\s]*[a-zA-Z][a-zA-Z\s]*[\s]*$")
        if z.match(self.name.text()) is None:
            self.err_name.setText("invalid name")
            test = True
            print(test)
        if self.schedule is None or self.fileNames is None:
            test = True

        if test is False:
            print("ok")
            os.mkdir("/home/amani/Documents/pcd/Data/Schedules/" + str(self.name.text()))
            copyfile(self.schedule[0], "/home/amani/Documents/pcd/Data/Schedules/" + str(self.name.text()) + "/schedule.jpg")
            schedule_path = "/home/amani/Documents/pcd/Data/Schedules/" + \
                os.listdir("/home/amani/Documents/pcd/Data/Schedules/" + str(self.name.text()))[0]
            prof = Mo.Professor(name=str(self.name.text()), CIN=int(self.cin.text()),
                                num_tel=int(self.phone_num.text()), emploi_path=schedule_path)
            data.session.add(prof)
            data.session.commit()
            conn = data.engine.connect()
            table = data.Base.metadata.tables['person']
            selc_st = table.select().with_only_columns([table.c.person_id]).where(table.c.CIN == int(self.cin.text()))
            resl = conn.execute(selc_st)
            row = resl.fetchone()

            pro_id = int(row['person_id'])
            path = "/home/amani/Documents/pcd/Face_recognition/Data/s" + str(pro_id)
            stmt = update(table).where(table.c.person_id == pro_id).values(photo_folder_path=path)
            conn.execute(stmt)
            os.mkdir("/home/amani/Documents/pcd/Face_recognition/Data/s"+str(pro_id))
            i = 0
            for image in self.fileNames:
                i = i+1
                copyfile(image, "/home/amani/Documents/pcd/Face_recognition/Data/s" + str(pro_id) + "/im" + str(i))
            sys.exit(self.app.exec_())
        else:
            self.win.show()

    def Add_photos_clicked(self):
        dialog = QFileDialog()
        dialog.setNameFilter("Images (*.png *.xpm *.jpg)")
        dialog.setFileMode(dialog.ExistingFiles)
        if (dialog.exec_()):
            self.fileNames = dialog.selectedFiles()
        for file in self.fileNames:
            print(file)

    def Add_schedule_clicked(self):
        dialog = QFileDialog()
        dialog.setNameFilter("Images (*.png *.xpm *.jpg)")
        dialog.setFileMode(dialog.ExistingFile)
        if (dialog.exec_()):
            self.schedule = dialog.selectedFiles()
        for file in self.schedule:
            print(file)

    def cancel_clicked(self):

        sys.exit(self.app.exec_())


form = Add_Prof()
form.window()
