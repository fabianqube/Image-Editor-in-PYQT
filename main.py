#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
from PIL import Image, ImageFilter

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = 'changed_photos'

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, image_path):
        picture_text.hide()
        pix_map_image = QPixmap(image_path)
        w, h = picture_text.width(), picture_text.height() 
        pix_map_image = pix_map_image.scaled(w, h, Qt.KeepAspectRatio)
        picture_text.setPixmap(pix_map_image)
        picture_text.show()

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)   
        self.image.save(image_path)

    def b_w(self):
        self.image = self.image.convert('L') 
        path = os.path.join(self.dir, self.save_dir, self.filename)  
        self.saveImage()
        self.showImage(path) 

    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90) 
        path = os.path.join(self.dir, self.save_dir, self.filename)  
        self.saveImage()
        self.showImage(path)
    
    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270) 
        path = os.path.join(self.dir, self.save_dir, self.filename)  
        self.saveImage()
        self.showImage(path)

    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        path = os.path.join(self.dir, self.save_dir, self.filename)  
        self.saveImage()
        self.showImage(path)

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        path = os.path.join(self.dir, self.save_dir, self.filename)  
        self.saveImage()
        self.showImage(path)

image = ImageProcessor()

app = QApplication([])
main_window = QWidget()

image_holder = QListWidget()
folder = QPushButton('folder')
case = []
picture_text = QLabel('Picture')
left_b = QPushButton('left')
right_b = QPushButton('right')
mirror_b = QPushButton('mirror')
sharpen_b = QPushButton('sharpen')
b_w_b = QPushButton('b_w')

main_h_line = QHBoxLayout()
v_line_1 = QVBoxLayout()
v_line_2 = QVBoxLayout()
second_h_line = QHBoxLayout()

v_line_1.addWidget(folder)
v_line_1.addWidget(image_holder)
v_line_2.addWidget(picture_text)
second_h_line.addWidget(left_b)
second_h_line.addWidget(right_b)
second_h_line.addWidget(mirror_b)
second_h_line.addWidget(sharpen_b)
second_h_line.addWidget(b_w_b)
main_h_line.addLayout(v_line_1,10)
main_h_line.addLayout(v_line_2,90)
v_line_2.addLayout(second_h_line)

main_window.setLayout(main_h_line)

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    

def filter(files, extensions):
    result = []
    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                result.append(file)
    return result

def showFilenamesList():
    extensions = ['.jpg','.png','.gif']
    chooseWorkdir()
    file_names = filter(os.listdir(workdir),extensions)
    image_holder.clear()
    for file_name in file_names:
        image_holder.addItem(file_name)

def showChosenImage():
    if image_holder.currentRow() >= 0:
        filename = image_holder.currentItem().text()
        image.loadImage(workdir, filename)
        image_path = os.path.join(image.dir, image.filename)
        image.showImage(image_path)

folder.clicked.connect(showFilenamesList)

image_holder.currentRowChanged.connect(showChosenImage)

b_w_b.clicked.connect(image.b_w)
left_b.clicked.connect(image.left)
right_b.clicked.connect(image.right)
mirror_b.clicked.connect(image.mirror)
sharpen_b.clicked.connect(image.sharpen)

main_window.show()
app.exec_()

