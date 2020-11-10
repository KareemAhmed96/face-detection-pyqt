import os
project_name = input("pls enter pro name:")
with open("__main__.py" , 'w') as f_h:
    folder_name = "{}.{}".format(project_name , project_name)
    main_obj = "Main{}".format(project_name)
    f_h.write('''from PyQt5.QtWidgets import  QApplication\nfrom {} import {}
\napp = QApplication([])\n#put your main object here\ntmp = {}()\napp.exec_()'''.format(folder_name,main_obj,main_obj))
if len(project_name) != 0:
   if not os.path.isdir(project_name):
       os.makedirs(project_name)
       init_file_path = os.path.join(project_name,"__init__.py")
       with open(init_file_path, "w") as fobj:
           pass
       project_file_path = os.path.join(project_name, "{}.py".format(project_name))
       with open(project_file_path, "w") as fobj:
           fobj.write('''from PyQt5.QtWidgets import  QMainWindow
class {}(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.show()'''.format(main_obj))
       wanted_folders = ["Forms" , "Views" ,"Models","ViewMngr"]
       for folder_name in wanted_folders:
           folder_path = os.path.join(project_name,folder_name)
           os.makedirs(folder_path)
           init_file_path = os.path.join(folder_path , "__init__.py")
           with open(init_file_path , "w") as fobj:
               pass
else:
    print("please enter valid name")