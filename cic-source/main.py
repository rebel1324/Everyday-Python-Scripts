# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
import re
import os
from os import path
from os import walk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

current_file_card = ""
current_file_image = ""
file_card_data = ""
file_image_data = ""

PNG_HEADER = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
PNG_ENDER = b"\x49\x45\x4E\x44\xAE\x42\x60\x82"


def validateCard(label):
    try:
        global current_file_card
        fileData = open(current_file_card, "rb").read()
        pngStart = fileData.find(PNG_HEADER)
        pngEnd = fileData.find(PNG_ENDER)
        binaryStart = pngEnd + len(PNG_ENDER)
        binaryEnd = len(fileData)

        if (pngStart == pngEnd or pngStart < 0 or pngEnd < 0):
            raise StopIteration

        if (binaryStart > binaryEnd):
            raise StopIteration

        global file_card_data
        file_card_data = fileData[binaryStart:]

        if (len(file_card_data) <= 0):
            file_card_data = ""
            raise ValueError

        return True
    except ValueError as e:
        label.setText("This Image is not a Honey Select Data Image.")
        return False
    except StopIteration as e:
        label.setText("Error occured while parsing the file.")
        return False
    except:
        label.setText("Unable to open the file.")
        return False


def validateImage(label):
    try:
        global current_file_image
        fileData = open(current_file_image, "rb").read()
        pngStart = fileData.find(PNG_HEADER)
        pngEnd = fileData.find(PNG_ENDER)
        binaryStart = pngEnd + len(PNG_ENDER)
        binaryEnd = len(fileData)

        if (pngStart == pngEnd or pngStart < 0 or pngEnd < 0):
            raise StopIteration

        global file_image_data
        file_image_data = fileData[:binaryStart]

        return True
    except ValueError as e:
        label.setText("This Image is a Honey Select Data Image.")
        return False
    except StopIteration as e:
        label.setText("Error occured while parsing the file.")
        return False
    except:
        label.setText("Unable to open the file.")
        return False


def startCheck(label):
    if (file_card_data == ""):
        label.setText("Selected file is not a Honey Select Data Image.")
        return False

    if (current_file_image == ""):
        label.setText("Cannot find a image for the card.")
        return False

    return True


def createNewImage():
    try:
        path, name = os.path.split(current_file_card)
        name = "new_" + name

        f = open(os.path.join(path, name), 'wb')
        f.write(file_image_data + file_card_data)
        f.close()

        return name
    except:
        return False


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(746, 210)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(746, 210))
        MainWindow.setMaximumSize(QtCore.QSize(746, 210))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonCard = QtWidgets.QPushButton(self.centralwidget)
        self.buttonCard.setGeometry(QtCore.QRect(20, 20, 181, 34))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.buttonCard.setFont(font)
        self.buttonCard.setObjectName("buttonCard")
        self.buttonImage = QtWidgets.QPushButton(self.centralwidget)
        self.buttonImage.setGeometry(QtCore.QRect(20, 60, 181, 34))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.buttonImage.setFont(font)
        self.buttonImage.setObjectName("buttonImage")
        self.labelCard = QtWidgets.QLabel(self.centralwidget)
        self.labelCard.setGeometry(QtCore.QRect(210, 20, 491, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.labelCard.setFont(font)
        self.labelCard.setObjectName("labelCard")
        self.labelImage = QtWidgets.QLabel(self.centralwidget)
        self.labelImage.setGeometry(QtCore.QRect(210, 60, 501, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.labelImage.setFont(font)
        self.labelImage.setObjectName("labelImage")
        self.labelResult = QtWidgets.QLabel(self.centralwidget)
        self.labelResult.setGeometry(QtCore.QRect(20, 160, 701, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.labelResult.setFont(font)
        self.labelResult.setObjectName("labelResult")
        self.buttonCommence = QtWidgets.QPushButton(self.centralwidget)
        self.buttonCommence.setGeometry(QtCore.QRect(20, 120, 701, 34))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setBold(False)
        font.setWeight(50)
        self.buttonCommence.setFont(font)
        self.buttonCommence.setObjectName("buttonCommence")
        self._decoLine = QtWidgets.QFrame(self.centralwidget)
        self._decoLine.setGeometry(QtCore.QRect(20, 100, 701, 16))
        self._decoLine.setFrameShape(QtWidgets.QFrame.HLine)
        self._decoLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self._decoLine.setObjectName("_decoLine")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.buttonCard.clicked.connect(self.selectCard)
        self.buttonImage.clicked.connect(self.selectImage)
        self.buttonCommence.clicked.connect(self.selectStart)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def selectStart(self, bool):
        if (startCheck(self.labelResult)):
            name = createNewImage()
            if (name != False):
                self.labelResult.setText("Successfully Saved as " + name)
            else:
                self.labelResult.setText("Failed to save the file.")

    def selectCard(self, bool):
        fileName, _ = QFileDialog.getOpenFileName(
            parent=self.centralwidget,
            caption="Select a Character/Scene File.",
            filter="Honey Select Data Images (*.png)")
        global current_file_card
        global file_card_data
        if fileName:
            current_file_card = fileName

            if (validateCard(self.labelCard)):
                self.labelCard.setText("Loaded Honey Select Data Image.")
        else:
            current_file_card = ""
            file_card_data = ""
            self.labelCard.setText("Select a card to change the image")

    def selectImage(self, bool):
        fileName, _ = QFileDialog.getOpenFileName(
            parent=self.centralwidget,
            caption="Select an image for the Data Image.",
            filter="PNG Images (*.png)")

        global current_file_image
        global file_image_data
        if fileName:
            current_file_image = fileName
            if (validateImage(self.labelImage)):
                self.labelImage.setText("Loaded PNG Image Card.")
        else:
            current_file_image = ""
            file_image_data = ""
            self.labelImage.setText(
                "Select an image to override existing card's image")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Character Card Image Changer"))
        self.buttonCard.setText(_translate("MainWindow", "Select Card.."))
        self.buttonImage.setText(_translate("MainWindow", "Select Image.."))
        self.labelCard.setText(
            _translate("MainWindow", "Select a card to change the image"))
        self.labelImage.setText(
            _translate("MainWindow",
                       "Select an image to override existing card\'s image"))
        self.labelResult.setText(
            _translate("MainWindow", "Waiting for instructions."))
        self.buttonCommence.setText(
            _translate("MainWindow", "Override Card\'s Image"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
