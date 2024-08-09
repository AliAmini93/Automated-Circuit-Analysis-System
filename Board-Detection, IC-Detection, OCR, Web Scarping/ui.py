import logging

logger = logging.getLogger('logger_Info')
from PyQt6.QtWidgets import QFileDialog, QAbstractItemView, QPushButton, QTextBrowser, QLabel, QComboBox, QApplication, \
    QMainWindow, QGridLayout, QTextEdit, QWidget, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtWidgets
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QDesktopServices, QFont, QTransform
from PyQt6.QtCore import QUrl
from ic_info.path import Path_Datasheets, Path_UnverifiedFiles, Path_Input
from database import change_database
import os
from ic_info.path import Path_Report

from create_doc import create_doc
from PyQt6.QtWidgets import QMessageBox
import shutil


class MainWindow(QMainWindow):

    def __init__(self, data, pictures_IC):
        self.all_paths = []
        QMainWindow.__init__(self)
        self.data = data
        self.pictures_IC = pictures_IC
        self.ok_clicked = False

        self.setMinimumSize(QSize(1200, 480))
        self.setWindowTitle("گزارش")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout(self)
        central_widget.setLayout(grid_layout)

        self.table = QTableWidget(self)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        stylesheet = """
            QHeaderView::section{background-color: lightblue}
            QAbstractButton{background-color: lightblue}
            """
        self.table.setStyleSheet(stylesheet)

        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels(
            ["وضعیت", "شماره قطعه", "شناسه تراشه", "تصویر", "دسته", "سازنده", "مشخصات فنی", "لینک دیتاشیت", "منبع"])
        self.table.horizontalHeader().setDefaultSectionSize(150)
        self.table.verticalHeader().setDefaultSectionSize(150)

        self.table.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.set_data()

        self.table.resizeColumnsToContents()

        grid_layout.addWidget(self.table, 0, 0, 1, 2)  # Adding the table to the grid
        self.okPushButton = QPushButton('تولید گزارش')

        self.okPushButton.clicked.connect(self.okButtonClicked)

        grid_layout.addWidget(self.okPushButton, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        grid_layout.addItem(spacerItem, 1, 1, 1, 1)

    def set_data(self, ):

        self.table.setRowCount(len(self.data))
        self.numDetect_per_ic = {}
        for pic in self.pictures_IC:
            if pic in self.numDetect_per_ic.keys():
                self.numDetect_per_ic[pic] += 1
            else:
                self.numDetect_per_ic[pic] = 1
        for i in range(self.table.rowCount()):

            comboBox = QComboBox()
            comboBox.wheelEvent = lambda event: None
            comboBox.addItem(' ')
            comboBox.addItem('تایید')
            comboBox.addItem('حذف')
            comboBox.addItem('اصلاح')

            if 'flag' in self.data[i].keys():
                comboBox.setCurrentIndex(self.data[i]['flag'])

            self.table.setCellWidget(i, 0, comboBox)

            item = QTableWidgetItem(self.data[i]['ManufacturerPartNumber'])

            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.table.setItem(i, 1, item)  # setText(data[i][j])
            item = QTableWidgetItem(self.data[i]['textOCR'])
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.table.setItem(i, 2, item)

            tableWidgetItem = QTableWidgetItem()
            tableWidgetItem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.path = (Path_Input + str(self.pictures_IC[i])).replace('\\', '/')

            self.all_paths.append(self.path)
            self.pixmap = QPixmap(self.path).scaledToHeight(100)

            tableWidgetItem.setData(1, self.pixmap)

            zoomPushButton = QPushButton('بزرگنمایی')

            first_pic_index = i - self.numDetect_per_ic[self.pictures_IC[i]] + 1
            zoomPushButton.clicked.connect(lambda checked, j=first_pic_index: self.openImageViewer(j))
            comboBox.currentIndexChanged.connect(
                lambda checked, i=i: self.openICViewer(i, self.table.cellWidget(i, 0).currentIndex()))

            zoomPushButton.setFixedSize(50, 20)
            zoomPushButton.move(100, 100)

            self.table.setSpan(i, 3, self.numDetect_per_ic[self.pictures_IC[i]], 1)
            self.table.setItem(i, 3, tableWidgetItem)
            self.table.setCellWidget(i, 3, zoomPushButton)
            item = QTableWidgetItem(self.data[i]['Category'])
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.table.setItem(i, 4, item)
            item = QTableWidgetItem(self.data[i]['Manufacturer'])
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.table.setItem(i, 5, item)
            textEdit = QTextEdit()
            textEdit.setText(self.data[i]['Description'])

            self.table.setCellWidget(i, 6, textEdit)

            textBrowser = QTextBrowser()
            textBrowser.setOpenLinks(False)
            if '_id' in self.data[i].keys() and self.data[i]['DataSheetUrl'] == '':
                DataSheetUrl = Path_Datasheets + str(self.data[i]['_id']) + '.pdf'
            else:
                DataSheetUrl = self.data[i]['DataSheetUrl']

            link = '<br><a href="{}">لینک دیتاشیت</a></br>'.format((DataSheetUrl).replace('\\', '/'))

            textBrowser.insertHtml(link)

            textBrowser.anchorClicked.connect(self.handle_links)
            textBrowser.show()
            self.table.setCellWidget(i, 7, textBrowser)
            item = QTableWidgetItem(self.data[i]['source'])
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)

            self.table.setItem(i, 8, item)

    def change_data(self, currentIndex):

        self.table.cellWidget(currentIndex, 0).setCurrentIndex(self.data[currentIndex]['flag'])

        self.table.item(currentIndex, 1).setText(self.data[currentIndex]['ManufacturerPartNumber'])
        self.table.item(currentIndex, 2).setText(self.data[currentIndex]['textOCR'])
        self.table.item(currentIndex, 4).setText(self.data[currentIndex]['Category'])

        self.table.item(currentIndex, 5).setText(self.data[currentIndex]['Manufacturer'])
        self.table.cellWidget(currentIndex, 6).setText(self.data[currentIndex]['Description'])
        link = '<br><a href="{}">لینک دیتاشیت</a></br>'.format(
            (self.data[currentIndex]['DataSheetUrl']).replace('\\', '/'))
        self.table.cellWidget(currentIndex, 7).setText('')
        self.table.cellWidget(currentIndex, 7).setText(link)
        self.table.item(currentIndex, 8).setText(self.data[currentIndex]['source'])

    def handle_links(self, url):
        if not url.scheme():
            url = QUrl.fromLocalFile(url.toString())
        QDesktopServices.openUrl(url)

    def closeEvent(self, event):
        if not self.ok_clicked:
            messageBox = QMessageBox(self, )

            messageBox.setWindowTitle("تایید خروج")
            messageBox.setIcon(QMessageBox.Icon.Question)

            messageBox.setText(
                "آیا مطمئن هستید که میخواهید خارج شوید؟ در صورت خروج گزارش طبق شرایط موجود تولید می شود.")

            buttonoptionA = messageBox.addButton("بله", QMessageBox.ButtonRole.YesRole)
            buttonoptionB = messageBox.addButton("خیر", QMessageBox.ButtonRole.NoRole)
            messageBox.setDefaultButton(buttonoptionA)
            messageBox.exec()

            if messageBox.clickedButton() == buttonoptionA:
                create_doc(self.data, self.pictures_IC)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def okButtonClicked(self):

        messageBox = QMessageBox(self, )

        messageBox.setWindowTitle("اخطار")
        messageBox.setIcon(QMessageBox.Icon.Warning)

        messageBox.setText(
            "ستون مربوط به وضعیت باید تکمیل شود")
        buttonoptionA = messageBox.addButton("باشه", QMessageBox.ButtonRole.AcceptRole)
        messageBox.setDefaultButton(buttonoptionA)
        all_field_filled = True
        for i in range(self.table.rowCount()):
            index = self.table.cellWidget(i, 0).currentIndex()
            if index == 0 or index == 3:
                all_field_filled = False
        if all_field_filled == False:
            messageBox.exec()
            return

        messageBox = QMessageBox(self, )

        messageBox.setWindowTitle("تایید")
        messageBox.setIcon(QMessageBox.Icon.Question)

        messageBox.setText(
            "بعد از تایید بلافاصله رابط گرافیکی برای این برد بسته می شود، آیا همچنان مایل هستید تا تغییرات اعمال شده را نهایی و گزارش را تولید کنید؟")
        buttonoptionA = messageBox.addButton("بله", QMessageBox.ButtonRole.YesRole)
        buttonoptionB = messageBox.addButton("خیر", QMessageBox.ButtonRole.NoRole)
        messageBox.setDefaultButton(buttonoptionA)
        messageBox.exec()

        if messageBox.clickedButton() == buttonoptionA:
            self.ok_clicked = True
            for i in range(self.table.rowCount()):
                true_index = []

                index = self.table.cellWidget(i, 0).currentIndex()
                self.data[i]['flag'] = index
            self.data, self.pictures_IC = change_database(self.data, self.pictures_IC)

            create_doc(self.data, self.pictures_IC)
            self.close()
            os.startfile(Path_Report + 'Report.docx')
        else:
            return

    def openImageViewer(self, currentIndex):

        self.viewer = ImageViewer(self.all_paths, currentIndex, self.numDetect_per_ic)
        self.viewer.show()

    def openICViewer(self, currentIndex, combo_index):
        if combo_index == 3:
            self.viewer = FormViewer(self, currentIndex)
            self.viewer.show()


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, images, currentIndex, numDetect_per_ic):
        super().__init__()
        self.setWindowTitle("تصویر تراشه")
        self.images = images
        self.numDetect_per_ic = numDetect_per_ic
        self.currentIndex = currentIndex

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setGeometry(QtCore.QRect(130, 90, 191, 141))
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 8404, 122))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.imageLabel = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)

        self.scrollArea.setWidget(self.imageLabel)

        self.loadImage(self.images[self.currentIndex])
        self.btnZoomIn = QtWidgets.QPushButton("بزرگنمایی")
        self.btnZoomIn.clicked.connect(self.zoomIn)
        self.btnZoomIn.setIcon(QIcon('Icons/zoomin.png'))
        self.btnZoomIn.setStyleSheet("QPushButton { text-align: center; }")
        self.btnZoomOut = QtWidgets.QPushButton("دورنمایی")
        self.btnZoomOut.clicked.connect(self.zoomOut)
        self.btnZoomOut.setIcon(QIcon('Icons/zoomout.png'))
        self.btnZoomOut.setStyleSheet("QPushButton { text-align: center; }")
        self.btnRotate = QtWidgets.QPushButton("چرخش")
        self.btnRotate.clicked.connect(self.rotate_image)
        self.btnRotate.setIcon(QIcon('Icons/rotate.png'))
        self.btnRotate.setStyleSheet("QPushButton { text-align: center; }")
        self.btnNext = QtWidgets.QPushButton("تصویر بعدی")
        self.btnNext.clicked.connect(self.nextImage)
        self.btnNext.setIcon(QIcon('Icons/next.png'))
        self.btnNext.setStyleSheet("QPushButton { text-align: center; }")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.scrollArea)
        VBlayout.addWidget(self.btnZoomIn)
        VBlayout.addWidget(self.btnZoomOut)
        VBlayout.addWidget(self.btnRotate)
        VBlayout.addWidget(self.btnNext)

    def loadImage(self, fileName):
        pixmap = QtGui.QPixmap(fileName)
        if not pixmap.isNull():
            self.imageLabel.setPixmap(pixmap.scaled(500, 400))  # , QtCore.Qt.AspectRatioMode.KeepAspectRatio))

    def zoomIn(self):
        size = self.imageLabel.pixmap().size()
        self.imageLabel.setPixmap(self.imageLabel.pixmap().scaled(size * 1.25))

    def zoomOut(self):
        size = self.imageLabel.pixmap().size()
        self.imageLabel.setPixmap(self.imageLabel.pixmap().scaled(size / 1.25))

    def rotate_image(self):
        transform = QTransform()
        transform.rotate(90)
        self.imageLabel.setPixmap(self.imageLabel.pixmap().transformed(transform))

    def nextImage(self):
        self.currentIndex = (self.currentIndex + self.numDetect_per_ic[
            self.images[self.currentIndex].split('/')[-1]]) % len(self.images)

        self.loadImage(self.images[self.currentIndex])


class FormViewer(QtWidgets.QWidget):
    def __init__(self, mv, currentIndex):

        super().__init__()
        pic_name = mv.pictures_IC[currentIndex]
        self.setWindowTitle("مشخصات تراشه")
        self.imageLabel = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(Path_Input + pic_name)
        if not pixmap.isNull():
            self.imageLabel.setPixmap(pixmap.scaledToHeight(100))

        self.QLabel1 = QLabel('شماره قطعه:')
        self.textEdit1 = QTextEdit()  # QLabel()#

        self.textEdit1.setText(mv.data[currentIndex]['ManufacturerPartNumber'])

        self.QLabel2 = QLabel('شناسه تراشه:')
        self.textEdit2 = QTextEdit()  # QLabel()#
        self.textEdit2.setText(mv.data[currentIndex]['textOCR'])

        self.QLabel3 = QLabel('دسته:')
        self.textEdit3 = QTextEdit()  # QLabel()#
        self.textEdit3.setText(mv.data[currentIndex]['Category'])

        self.QLabel4 = QLabel('سازنده:')
        self.textEdit4 = QTextEdit()  # QLabel()#
        self.textEdit4.setText(mv.data[currentIndex]['Manufacturer'])

        self.QLabel5 = QLabel('مشخصات فنی:')
        self.textEdit5 = QTextEdit()  # QLabel()#
        self.textEdit5.setText(mv.data[currentIndex]['Description'])

        self.QLabel6 = QLabel('لینک دیتاشیت:')
        self.btnBrowse = QtWidgets.QPushButton("browse")
        self.label = QLabel()
        self.btnOk = QtWidgets.QPushButton("تایید")
        self.btnCancel = QtWidgets.QPushButton("انصراف")
        self.btnOk.clicked.connect(lambda: self.edit_IC_info(mv, currentIndex))
        self.btnCancel.clicked.connect(lambda: self.cancel_IC_info(mv, currentIndex))
        self.btnBrowse.clicked.connect(lambda: self.browse(mv, currentIndex))
        self.path = None

        grid_layout = QGridLayout(self)
        grid_layout.addWidget(self.imageLabel, 0, 0)

        grid_layout.addWidget(self.QLabel1, 1, 0)
        grid_layout.addWidget(self.textEdit1, 1, 1, 1, 3)

        grid_layout.addWidget(self.QLabel2, 1, 4)
        grid_layout.addWidget(self.textEdit2, 1, 5, 1, 2)

        grid_layout.addWidget(self.QLabel3, 2, 0)
        grid_layout.addWidget(self.textEdit3, 2, 1, 1, 3)

        grid_layout.addWidget(self.QLabel4, 2, 4)
        grid_layout.addWidget(self.textEdit4, 2, 5, 1, 2)

        grid_layout.addWidget(self.QLabel5, 3, 0)
        grid_layout.addWidget(self.textEdit5, 3, 1, 1, 3)

        grid_layout.addWidget(self.QLabel6, 3, 4)
        grid_layout.addWidget(self.btnBrowse, 3, 5)
        grid_layout.addWidget(self.label, 3, 6)

        grid_layout.addWidget(self.btnOk, 4, 1)
        grid_layout.addWidget(self.btnCancel, 4, 2)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        grid_layout.addItem(spacerItem, 4, 3)

    def browse(self, ):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.pdf)')
        if path != ('', ''):
            self.label.setText(path[0].split('/')[-1])
        self.path = path[0]

    def edit_IC_info(self, mv, currentIndex):
        mv.data[currentIndex]['ManufacturerPartNumber'] = self.textEdit1.toPlainText()

        mv.data[currentIndex]['textOCR'] = self.textEdit2.toPlainText()

        mv.data[currentIndex]['Category'] = self.textEdit3.toPlainText()

        mv.data[currentIndex]['Manufacturer'] = self.textEdit4.toPlainText()

        mv.data[currentIndex]['Description'] = self.textEdit5.toPlainText()
        mv.data[currentIndex]['flag'] = 1
        mv.data[currentIndex]['source'] = 'user'
        if self.path != None:
            mv.data[currentIndex]['DataSheetUrl'] = self.path
            file_name = mv.data[currentIndex]['DataSheetUrl'].split('/')[-1]
            file_name = file_name.replace(' ', '_')
            shutil.copy(mv.data[currentIndex]['DataSheetUrl'], Path_UnverifiedFiles + file_name)
            mv.data[currentIndex]['DataSheetUrl'] = Path_UnverifiedFiles + file_name
        mv.change_data(currentIndex)

        self.close()

    def cancel_IC_info(self, ):
        self.close()


def show_window(data, pictures_IC):
    import sys

    app = QApplication(sys.argv)
    serifFont = QFont("Times New Roman", 10)
    app.setFont(serifFont)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    mw = MainWindow(data, pictures_IC)
    mw.show()

    sys.exit(app.exec())
