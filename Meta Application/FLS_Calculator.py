import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
address = 'C:/Users/user/Desktop'
import math
X_lense = 14
Y_lense = 22
class Ui_Calculator(object):
    def setupUi(self, Calculator):
        Calculator.setObjectName("Calculator")
        Calculator.resize(663, 500)
        self.verticalLayoutWidget = QtWidgets.QWidget(Calculator)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 645, 485))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.AllLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.AllLayout.setContentsMargins(0, 0, 0, 0)
        self.AllLayout.setObjectName("AllLayout")
        self.CheckBoxButtons = QtWidgets.QVBoxLayout()
        self.CheckBoxButtons.setObjectName("CheckBoxButtons")
        self.FLS_Calculator = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.FLS_Calculator.setFont(font)
        self.FLS_Calculator.setAlignment(QtCore.Qt.AlignCenter)
        self.FLS_Calculator.setWordWrap(False)
        self.FLS_Calculator.setObjectName("FLS_Calculator")
        self.CheckBoxButtons.addWidget(self.FLS_Calculator)
        self.AllLayout.addLayout(self.CheckBoxButtons)
        ###################################################
        self.Up = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Up.setFont(font)
        self.Up.setObjectName("Up")
        self.AllLayout.addWidget(self.Up)
        ###################################################
        self.Down = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Down.setFont(font)
        self.Down.setObjectName("Down")
        self.AllLayout.addWidget(self.Down)
        ###################################################
        self.Left = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Left.setFont(font)
        self.Left.setObjectName("Left")
        self.AllLayout.addWidget(self.Left)
        ###################################################
        self.Right = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Right.setFont(font)
        self.Right.setObjectName("Right")
        self.AllLayout.addWidget(self.Right)
        ###################################################
        self.IntitalCameraPosition = QtWidgets.QHBoxLayout()
        self.IntitalCameraPosition.setObjectName("IntitalCameraPosition")
        self.PosX = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.PosX.setFont(font)
        self.PosX.setObjectName("PosX")
        self.IntitalCameraPosition.addWidget(self.PosX)
        self.Pos_X = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        reg_ex = QRegExp("^[0-9]*[.]?[0-9]{0,1}$")
        input_validator_Pos_X = QRegExpValidator(reg_ex, self.Pos_X)
        self.Pos_X.setValidator(input_validator_Pos_X)
        self.Pos_X.setText("15")
        self.Pos_X.setObjectName("Pos_X")
        self.IntitalCameraPosition.addWidget(self.Pos_X)
        ###################################################
        self.PosY = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.PosY.setFont(font)
        self.PosY.setObjectName("PosY")
        self.IntitalCameraPosition.addWidget(self.PosY)
        self.Pos_Y = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        input_validator_Pos_Y = QRegExpValidator(reg_ex, self.Pos_Y)
        self.Pos_Y.setValidator(input_validator_Pos_Y)
        self.Pos_Y.setText("4")
        self.Pos_Y.setObjectName("Pos_Y")
        self.IntitalCameraPosition.addWidget(self.Pos_Y)
        self.AllLayout.addLayout(self.IntitalCameraPosition)
        ###################################################
        self.Step = QtWidgets.QHBoxLayout()
        self.Step.setObjectName("Step")
        self.Xstep = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Xstep.setFont(font)
        self.Xstep.setObjectName("Xstep")
        self.Step.addWidget(self.Xstep)
        self.X_step = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        input_validator_X_Step = QRegExpValidator(reg_ex, self.X_step)
        self.X_step.setValidator(input_validator_X_Step)
        self.X_step.setText("4")
        self.X_step.setObjectName("X_step")
        self.Step.addWidget(self.X_step)
        ###################################################
        self.Ystep = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Ystep.setFont(font)
        self.Ystep.setObjectName("Ystep")
        self.Step.addWidget(self.Ystep)
        self.Y_step = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        input_validator_Y_Step = QRegExpValidator(reg_ex, self.Y_step)
        self.Y_step.setValidator(input_validator_Y_Step)
        self.Y_step.setText("5")
        self.Y_step.setObjectName("Y_step")
        self.Step.addWidget(self.Y_step)
        ###################################################
        self.AllLayout.addLayout(self.Step)
        self.BoardLenght = QtWidgets.QHBoxLayout()
        self.BoardLenght.setObjectName("BoardLenght")
        self.LenghtX = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.LenghtX.setFont(font)
        self.LenghtX.setObjectName("LenghtX")
        self.BoardLenght.addWidget(self.LenghtX)
        self.Lenght_X = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        input_validator_Lenght_X = QRegExpValidator(reg_ex, self.Lenght_X)
        self.Lenght_X.setValidator(input_validator_Lenght_X)
        #self.Lenght_X.setText("")
        self.Lenght_X.setObjectName("Lenght_X")
        self.BoardLenght.addWidget(self.Lenght_X)
        ###################################################
        self.LenghtY = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.LenghtY.setFont(font)
        self.LenghtY.setObjectName("LenghtY")
        self.BoardLenght.addWidget(self.LenghtY)
        self.Lenght_Y = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        input_validator_Lenght_Y = QRegExpValidator(reg_ex, self.Lenght_Y)
        self.Lenght_Y.setValidator(input_validator_Lenght_Y)
        #self.Lenght_Y.setText("")
        self.Lenght_Y.setObjectName("Lenght_Y")
        self.BoardLenght.addWidget(self.Lenght_Y)
        self.AllLayout.addLayout(self.BoardLenght)
        ###################################################
        self.Calculate = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Calculate.setFont(font)
        self.Calculate.setObjectName("Calculate")
        self.AllLayout.addWidget(self.Calculate)
        self.Calculate.clicked.connect(self.calculate)
        ###################################################
        self.ClearLog = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ClearLog.setFont(font)
        self.ClearLog.setObjectName("Clear Log")
        self.AllLayout.addWidget(self.ClearLog)
        self.ClearLog.clicked.connect(self.clear_log)
        ###################################################
        self.Help = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Help.setFont(font)
        self.Help.setObjectName("Help")
        self.AllLayout.addWidget(self.Help)
        self.Help.clicked.connect(self.help_me)
        ###################################################
        self.Result = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.Result.setObjectName("Result")
        self.AllLayout.addWidget(self.Result)
        ###################################################
        self.retranslateUi(Calculator)
        QtCore.QMetaObject.connectSlotsByName(Calculator)
    def retranslateUi(self, Calculator):
        _translate = QtCore.QCoreApplication.translate
        Calculator.setWindowTitle(_translate("Calculator", "FLS Calculator"))
        self.FLS_Calculator.setText(_translate("Calculator", "FLS Calculator"))
        self.Up.setText(_translate("Calculator", "Any ports or tall objects up-side the board"))
        self.Down.setText(_translate("Calculator", "Any ports or tall objects down-side the board"))
        self.Left.setText(_translate("Calculator", "Any ports or tall objects left-side the board"))
        self.Right.setText(_translate("Calculator", "Any ports or tall objects right-side the board"))
        self.PosX.setText(_translate("Calculator", "Intial Camera Position X:"))
        self.PosY.setText(_translate("Calculator", "Intial Camera Position Y:"))
        self.Xstep.setText(_translate("Calculator", "X_step:"))
        self.Ystep.setText(_translate("Calculator", "Y_step:"))
        self.LenghtX.setText(_translate("Calculator", "Board\'s Length X:"))
        self.LenghtY.setText(_translate("Calculator", "Board\'s Length Y:"))
        self.Calculate.setText(_translate("Calculator", "Calculate"))
        self.ClearLog.setText(_translate("Calculator", "Clear Log"))
        self.Help.setText(_translate("Calculator", "Help"))
    def calculate(self):
        # Check if the "Right" QCheckBox is checked
        Up_checked = self.Up.isChecked()
        # Check if the "Right" QCheckBox is checked
        Down_checked = self.Down.isChecked()
        # Check if the "Right" QCheckBox is checked
        Right_checked = self.Right.isChecked()
        # Check if the "Right" QCheckBox is checked
        Left_checked = self.Left.isChecked()
        # Get the value of "X_step" QLineEdit
        X_step = self.X_step.text()
        # Get the value of "Y_step" QLineEdit
        Y_step = self.Y_step.text()
        # Get the value of "X0" QLineEdit
        X0 = self.Pos_X.text()
        # Get the value of "Y0" QLineEdit
        Y0 = self.Pos_Y.text()
        # Get the value of "X_board" QLineEdit
        X_board =  self.Lenght_X.text()
        # Get the value of "Y_board" QLineEdit
        Y_board =  self.Lenght_Y.text()   
        if not X_step or not Y_step or not X0 or not Y0 or not X_board or not Y_board:
            self.Result.append('Please fill in all the fields.')
            return
        else:
            X_step = float(X_step)
            Y_step = float(Y_step)
            X0 = float(X0)
            Y0 = float(Y0)
            X_board = float(X_board)
            Y_board = float(Y_board)
    
            if X_step != 4 or Y_step != 5 or X0 !=15 or Y0 !=4 or not 4 < X_board < 50 or not 5 < Y_board < 47:
                self.Result.append('The values do not meet the conditions. Please check and try again.')
                return
        ###############################
        X = [X0 + i*X_step for i in range(0, int((57 - X0)/X_step) + 1)]
        Y = [Y0 + i*Y_step for i in range(0, int((40 - Y0)/Y_step) + 1)]
        Xf = math.ceil(X0 + 2*X_step + X_board - X_lense)
        Yf = math.ceil(Y0 + 2*Y_step + Y_board - Y_lense)
        closest_Xi = max(filter(lambda x: x <= Xf, X))
        closest_Yj = max(filter(lambda y: y <= Yf, Y))
        ##################################################
        nX =  X.index(closest_Xi) + 1 if Xf in X else X.index(closest_Xi) + 2
        nY = math.floor(closest_Yj/Y_step)+1 if Yf in Y else math.floor(Y[Y.index(closest_Yj) + 1]/Y_step)+1
        def ResX_Calculator():     
            CameraStartCoordinateX_OneToLast = X0 + (nX-2)*X_step
            CameraEndCoordinateX_OneToLast = CameraStartCoordinateX_OneToLast + X_lense
            ##################################################
            CircuitEndCoordinateX_OneToLast = X0 + X_step + X_board
            ##################################################
            ResX = CameraEndCoordinateX_OneToLast - CircuitEndCoordinateX_OneToLast
            print('ResX: ',ResX)
            self.Result.append(f'ResX: {ResX}')
            return ResX
        def ResY_Calculator():
            CameraStartCoordinateY_OneToLast = Y0 + (nY-2)*Y_step
            CameraEndCoordinateY_OneToLast = CameraStartCoordinateY_OneToLast + Y_lense
            ##################################################
            CircuitEndCoordinateY_OneToLast = Y0 + Y_step + Y_board
            ##################################################
            ResY = CameraEndCoordinateY_OneToLast - CircuitEndCoordinateY_OneToLast
            print('ResY: ',ResY)
            self.Result.append(f'ResY: {ResY}')
            return ResY
        rx =ResX_Calculator()
        ry =ResY_Calculator()
        if rx>=2:
            X_final = X_step * nX
            if (Down_checked==True and Up_checked==True) or (Down_checked==False and Up_checked==False):
                print(f'You can move the circuit in X direction up to {rx/2} cm.')
                self.Result.append(f'You can move the circuit in X direction up to {rx/2} cm.')
            if Down_checked==False and Up_checked==True:
                print(f'You can move the circuit in X direction up to {rx-2} cm.')
                self.Result.append(f'You can move the circuit in X direction up to {rx-2} cm.')
            if Down_checked==True and Up_checked==False:
                print('Do not move the circuit in X direction.')
                self.Result.append('Do not move the circuit in X direction.')
        else:
            print('Recalculating the ResX...')
            self.Result.append('Recalculating the ResX...')
            nX = nX + 1
            X_final = X_step * nX
            rx = ResX_Calculator()
            if (Down_checked==True and Up_checked==True) or (Down_checked==False and Up_checked==False):
                print(f'You can move the circuit in X direction up to {rx/2} cm.')
                self.Result.append(f'You can move the circuit in X direction up to {rx/2} cm.')
            if Down_checked==False and Up_checked==True:
                print(f'You can move the circuit in X direction {rx/2} cm.')
                self.Result.append(f'You can move the circuit in X direction up to {rx/2} cm.')
            if Down_checked==True and Up_checked==False:
                print(f'You can move the circuit in X direction up to {rx/2} cm.')
                self.Result.append(f'You can move the circuit in X direction up to {rx/2} cm.')
        if ry>=2.5:
            Y_final = (nY-1) * Y_step + 1
            if (Right_checked==True and Left_checked==True) or (Right_checked==False and Left_checked==False):
                print(f'You can move the circuit in Y direction up to {ry/2} cm.')
                self.Result.append(f'You can move the circuit in Y direction up to {ry/2} cm.')
            if Left_checked==True and Right_checked==False:
                print(f'You can move the circuit in Y direction up to {ry-2} cm.')
                self.Result.append(f'You can move the circuit in Y direction up to {ry-2} cm.')
            if Left_checked==False and Right_checked==True:
                print('Do not move the circuit in Y direction.')
                self.Result.append('Do not move the circuit in Y direction.')
        else:
            print('Recalculating the ResY...')
            self.Result.append('Recalculating the ResY...')
            nY = nY + 1
            Y_final = (nY -1)* Y_step + 1
            ry = ResY_Calculator()
            if (Right_checked==True and Left_checked==True) or (Right_checked==False and Left_checked==False):
                print(f'You can move the circuit in Y direction up to {ry/2} cm.')
                self.Result.append(f'You can move the circuit in Y directio up to {ry/2} cm.')
            if Left_checked==True and Right_checked==False:
                print(f'You can move the circuit in Y direction up to {ry/2} cm.')
                self.Result.append(f'You can move the circuit in Y direction up to {ry/2} cm.')
            if Left_checked==False and Right_checked==True:
                print(f'You can move the circuit in Y direction up to {ry/2} cm.')
                self.Result.append(f'You can move the circuit in Y direction up to {ry/2} cm.')

        print("X_final: ", X_final)
        print("Y_final: ", Y_final)
        self.Result.append(f'X_final: {X_final}')
        self.Result.append(f'Y_final: {Y_final}')
    def clear_log(self):
        self.Result.clear()
    def help_me(self):
        hlp = os.path.join(address, "Calculator help.pdf")
        os.startfile(hlp)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Calculator = QtWidgets.QDialog()
    ui = Ui_Calculator()
    ui.setupUi(Calculator)
    Calculator.show()
    sys.exit(app.exec_())

