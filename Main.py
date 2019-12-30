#!/usr/bin/python3
# -*- coding: utf-8 -*-
import PIL
from PIL import Image
import random
import sys
import os
import ctypes
import sys
from PyQt5.QtWidgets import QApplication
import numpy
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction,\
    qApp, QFileDialog, QPushButton
import numpy as np
from scipy import signal
import cv2
from skimage.util import random_noise

from scipy.ndimage import zoom
import math
import warnings
from tkinter import *
from matplotlib import pyplot as plt
from sys import exit
import keyboard

class QImageViewer(QMainWindow):
    def __init__(self):
        super(QImageViewer,self).__init__()

        self.printer = QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)
        self.createActions()
        self.createMenus()
        self.resize(800, 600)
        self.image = ''
        self.btn1.clicked.connect(self.first)
        self.btn2.clicked.connect(self.second)
        self.btn3.clicked.connect(self.third)
        self.btn4.clicked.connect(self.fourth)
        self.btn5.clicked.connect(self.fifth)
        self.btn6.clicked.connect(self.sixth)



    def open(self):
        options = QFileDialog.Options()
        fileName = QFileDialog.getOpenFileName(self, "Open file", QDir.currentPath(), "Image files (*.jpg *.tif *.png)")
        #fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
        self.image = fileName[0]


        if self.image=='':
            return
            QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
        else:
            self.imageLabel.setPixmap(QPixmap(self.image))
            self.scaleFactor = 1.0
            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()
            self.imageLabel.setScaledContents(True)

    def print_(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QMessageBox.about(self, "About Image Viewer",
                          "<p>This <b>Image Viewer</b> example shows how to combine "
                          "QLabel and QScrollArea to display an image. QLabel is "
                          "typically used for displaying text, but it can also display "
                          "an image. QScrollArea provides a scrolling view around "
                          "another widget. If the child widget exceeds the size of the "
                          "frame, QScrollArea automatically provides scroll bars.</p>"
                          "<p>The example demonstrates how QLabel's ability to scale "
                          "its contents (QLabel.scaledContents), and QScrollArea's "
                          "ability to automatically resize its contents "
                          "(QScrollArea.widgetResizable), can be used to implement "
                          "zooming and scaling features.</p>"
                          "<p>In addition the example shows how to use QPainter to "
                          "print an image.</p><p>Image Viewer is the best way to pass your exam if you need</p>")

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.printAct = QAction("&Print...", self, shortcut="Ctrl+P", enabled=False, triggered=self.print_)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
        self.btn1 = QPushButton('Bài Tập 1', self)
        self.btn1.setGeometry(480,100,75,23)
        self.btn2 = QPushButton('Bài Tập 2', self)
        self.btn2.setGeometry(480, 130, 75, 23)
        self.btn3 = QPushButton('Bài Tập 3', self)
        self.btn3.setGeometry(480, 160, 75, 23)
        self.btn4 = QPushButton('Bài Tập 4', self)
        self.btn4.setGeometry(480, 190, 75, 23)
        self.btn5 = QPushButton('Bài Tập 5', self)
        self.btn5.setGeometry(480, 220, 75, 23)
        self.btn6 = QPushButton('Bài Tập 6',self)
        self.btn6.setGeometry(480,250,75,23)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def handleActivated(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                           QDir.currentPath(), "Image files (*.jpg *.tif *.png)")
        self.image = fname[0]
        self.scaleFactor = 1.0
        self.pixmapImage = QtGui.QPixmap(self.image)
        self.imageLabel.setPixmap(self.pixmapImage)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.show()

    def first(self):
        if self.image=='' :
            self.Mbox('Message', 'Vui lòng chọn ảnh để hiển thị',1)
        else:
            img = cv2.imread(self.image)
            plt.subplot(121), plt.imshow(img), plt.title('Display image in sublot')
            plt.xticks([]), plt.yticks([])
            plt.show()

    def Mbox(self, title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    def second(self):
        if(self.image==''):
            self.Mbox('Message', 'Vui chọn ảnh để hiển thị ',1)
        else :
            self.Mbox('Message', 'Vui chọn ảnh khác để hiển thị ', 1)


    def third(self):
        os.startfile('function.txt')

    def fourth(self):
        if self.image != '':

            self.Mbox('Vui lòng nhấn phím để chọn:', '1.cv2.blur() \n'
                                                     '2.cv2.boxFilter() \n'
                                                     '3.cv2.medianBlur() \n'
                                                     '4.cv2.bilateralFilter() \n'
                                                     '5. cv2.GaussianBlur() \n'
                                                     '6. Exit \n', 1)
            while True:
                try:  # used try so that if user pressed other than the given key error will not be shown
                    if keyboard.read_key() == '1':
                        self.cv2blur()

                    elif keyboard.read_key() == '2':
                        self.boxFilter()

                    elif keyboard.read_key() == '3':
                        self.medianBlur()

                    elif keyboard.read_key() == '4':
                        self.bilateralFilter()

                    elif keyboard.read_key() == '5':
                        self.gaussianBur()
                    elif keyboard.read_key() == '6':
                        break

                except:
                    break
        if self.image == '':
            self.Mbox('Message', 'Vui lòng chọn ảnh để hiển thị', 1)
            self.fourth()



    def cv2blur(self):
        img = cv2.imread(self.image)
        blur = cv2.blur(img, (3, 3))
        plt.subplot(121), plt.imshow(blur), plt.title('cv2blur')
        plt.xticks([]), plt.yticks([])
        plt.show()

    def boxFilter(self):
        img = cv2.imread(self.image)
        kernel1 = np.array([[0, 0, 0], [1 / 3, 1 / 3, 1 / 3], [0, 0, 0]])
        kernel2 = np.array([[1 / 3, 0, 0], [1 / 3, 0, 0], [1 / 3, 0, 0]])
        kernel3 = np.array([[1 / 3, 0, 0], [0, 1 / 3, 0], [0, 0, 1 / 3]])
        kernel4 = np.array([[0, 0, 1 / 3], [0, 1 / 3, 0], [1 / 3, 0, 0]])
        blur = cv2.filter2D(img, -1, kernel1)
        blur1 = cv2.filter2D(img, -1, kernel2)
        blur2 = cv2.filter2D(img, -1, kernel3)
        blur3 = cv2.filter2D(img, -1, kernel4)
        plt.subplot(321), plt.imshow(blur), plt.title('Horizontal')
        plt.xticks([]), plt.yticks([])
        plt.subplot(322), plt.imshow(blur1), plt.title('Vertical')
        plt.xticks([]), plt.yticks([])
        plt.subplot(323), plt.imshow(blur2), plt.title('Cross Left')
        plt.xticks([]), plt.yticks([])
        plt.subplot(324), plt.imshow(blur3), plt.title('Cross Right')
        plt.xticks([]), plt.yticks([])
        plt.show()

    def medianBlur(self):
        img = cv2.imread(self.image)
        blur = cv2.medianBlur(img, 11)
        plt.subplot(221), plt.imshow(img), plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(222), plt.imshow(blur), plt.title('Median')
        plt.xticks([]), plt.yticks([])
        plt.show()

    def bilateralFilter(self):
        img = cv2.imread(self.image)
        blur = cv2.bilateralFilter(img, 9, 75, 75)
        plt.subplot(121), plt.imshow(img), plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(blur), plt.title('Filter')
        plt.xticks([]), plt.yticks([])
        plt.show()

    def gaussianBur(self):
        img = cv2.imread(self.image)
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        plt.subplot(121), plt.imshow(img), plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(blur), plt.title('Gaussian Filter')
        plt.xticks([]), plt.yticks([])
        plt.show()

    def fifth(self):
        if(self.image!=''):
            self.Mbox('Vui lòng nhấn phím chọn', '1.Directional Filer \n'
                                             '2.Median Threshold \n'
                                             '3.Exit \n', 1)
            while True:
                try:  # used try so that if user pressed other than the given key error will not be shown
                     if keyboard.read_key() == '1':
                         self.directionalFilter()

                     elif keyboard.read_key() == '2':
                        image = cv2.imread(self.image, 0)
                        kernel = np.ones((5, 5), np.float32) / 25
                        noise_img = self.sp_noise(image, 0.05)
                        new_img = self.medianThreshold(noise_img, kernel, 50)
                        plt.subplot(121), plt.imshow(noise_img), plt.title('SaltPepper')
                        plt.xticks([]), plt.yticks([])
                        plt.subplot(122), plt.imshow(new_img), plt.title('Threshold Median')
                        plt.xticks([]), plt.yticks([])
                        plt.show()
                     else:
                         break


                except:
                     break
        if self.image == '':
            self.Mbox('Message', 'Vui lòng chọn ảnh để hiển thị', 1)
    def median(self):
        img = cv2.imread(self.image)
        image = self.add_gaussian_noise(img, 30)
        blurImg = cv2.medianBlur(img, 5)
        cv2.imwrite('median.jpg', blurImg)
        plt.subplot(221), plt.imshow(image), plt.title("Image corrupted by noise")
        plt.xticks([]), plt.yticks([])
        plt.subplot(222), plt.imshow(blurImg), plt.title("Median Filter")
        plt.show()
    def weigner(self):
        image = cv2.imread(self.image)
        weiImg = signal.wiener(image)
        cv2.imwrite('weiner.jpg', weiImg)
        plt.subplot(221), plt.imshow(image), plt.title("Image")
        plt.xticks([]), plt.yticks([])
        plt.subplot(222), plt.imshow(weiImg), plt.title("Weiner Filter")
        plt.show()
    def sixth(self):
        if self.image != '':
            self.Mbox('Vui lòng nhấn phím để chọn:', '1.Median filter \n'
                                                     '2.Weiner \n'
                                                     '3.Adaptive median \n'
                                                     '4.Exit \n', 1)

            while True:
                try:  # used try so that if user pressed other than the given key error will not be shown
                    if keyboard.read_key() == '1':
                        print("1")
                        self.median()
                    elif keyboard.read_key() == '2':
                        self.weigner()
                    elif keyboard.read_key() == '3':
                        img = PIL.Image.open(self.image).convert('L')
                        image = self.add_gaussian_noise(img, 30)
                        adapImg = self.medianAdaptive(image, 3)
                        cv2.imwrite('adaptiveMedian.jpg', adapImg)
                        plt.subplot(221), plt.imshow(image), plt.title("Image corrupted by noise")
                        plt.xticks([]), plt.yticks([])
                        plt.subplot(222), plt.imshow(adapImg), plt.title("Adaptive Median Filter")
                        plt.show()
                    elif keyboard.read_key() == '4':
                        break
                except:
                    break

        if self.image == '':
            self.Mbox('Message', 'Vui lòng chọn ảnh để hiển thị', 1)


    def directionalFilter(self):
        img = cv2.imread(self.image)
        kernel1 = np.array([[0, 0, 0], [1 / 3, 1 / 3, 1 / 3], [0, 0, 0]])
        kernel2 = np.array([[1 / 3, 0, 0], [1 / 3, 0, 0], [1 / 3, 0, 0]])
        kernel3 = np.array([[1 / 3, 0, 0], [0, 1 / 3, 0], [0, 0, 1 / 3]])
        kernel4 = np.array([[0, 0, 1 / 3], [0, 1 / 3, 0], [1 / 3, 0, 0]])
        images = []
        # Generate noisy images using cv2.randn. Can use your own mean and std.
        for _ in range(20):
            img1 = img.copy()
            cv2.randn(img1, (0, 0, 0), (50, 50, 50))
            images.append(img + img1)

        blur = cv2.filter2D(images[1], -1, kernel1)
        blur1 = cv2.filter2D(images[1], -1, kernel2)
        blur2 = cv2.filter2D(images[1], -1, kernel3)
        blur3 = cv2.filter2D(images[1], -1, kernel4)
        plt.subplot(321), plt.imshow(blur), plt.title('Horizontal')
        plt.xticks([]), plt.yticks([])
        plt.subplot(322), plt.imshow(blur1), plt.title('Vertical')
        plt.xticks([]), plt.yticks([])
        plt.subplot(323), plt.imshow(blur2), plt.title('Cross Left')
        plt.xticks([]), plt.yticks([])
        plt.subplot(324), plt.imshow(blur3), plt.title('Cross Right')
        plt.xticks([]), plt.yticks([])
        plt.show()

    def sp_noise(self, image, prop):
        # Add salt and pepper noise to image
        output = np.zeros(image.shape, np.uint8)
        thred = 1 - prop
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                rdn = random.random()
                if (rdn < prop):
                    output[i][j] = 0
                elif (rdn > thred):
                    output[i][j] = 255
                else:
                    output[i][j] = image[i][j]
        return output

    def medianThreshold(self, old, n, thres):
        new = cv2.filter2D(old, -1, n)
        for i in range(old.shape[0]):
            for j in range(old.shape[1]):
                if abs(old[i, j] - new[i, j]) <= thres:
                    new[i, j] = old[i, j]

        return new

    def add_gaussian_noise(self,img, sigma):
        gauss = numpy.random.normal(0, sigma, numpy.shape(img))
        noisy_img = img + gauss
        noisy_img[noisy_img < 0] = 0
        noisy_img[noisy_img > 255] = 255
        return noisy_img

    def medianAdaptive(self,data,kernel_size):
        temp = []
        indexer = kernel_size
        data_final = []
        data_final = numpy.zeros((len(data), len(data[0])))
        for i in range(len(data)):

            for j in range(len(data[0])):

                for z in range(kernel_size):
                    if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                        for c in range(kernel_size):
                            temp.append(0)
                    else:
                        if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                            temp.append(0)
                        else:
                            for k in range(kernel_size):
                                temp.append(data[i + z - indexer][j + k - indexer])

                temp.sort()
                data_final[i][j] = temp[len(temp) // 2]
                temp = []
        return data_final


if __name__ == '__main__':

    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
