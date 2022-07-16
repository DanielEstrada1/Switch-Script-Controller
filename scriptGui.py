import sys,os,serial,time
from PyQt6.QtWidgets import (QMenu,QMainWindow, QApplication, QPushButton, QWidget, QGridLayout, 
QLabel,QLineEdit, QListWidget, QListWidgetItem, QFileDialog, QButtonGroup, QAbstractItemView,
QMessageBox, QPlainTextEdit, QVBoxLayout)
from PyQt6.QtGui import QIcon, QAction,QIntValidator, QDoubleValidator, QRegularExpressionValidator
from PyQt6.QtCore import Qt, QRegularExpression, QObject, QThread, pyqtSignal
from decimal import Decimal, DecimalException, InvalidOperation
from serial import SerialException


class inputButton(QPushButton):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.initUI()
    
    def initUI(self):
        self.setCheckable(True)

class dpadButtons(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.btnGroup = QButtonGroup(self)

        self.btnDpadU = inputButton("↑", self)
        self.btnDpadL = inputButton("←", self)
        self.btnDpadD = inputButton("↓", self)
        self.btnDpadR = inputButton("→", self)
        self.btnDpadUR = inputButton("↗", self)
        self.btnDpadUL = inputButton("↖", self)
        self.btnDpadDL = inputButton("↙", self)
        self.btnDpadDR = inputButton("↘", self)

        grid.addWidget(self.btnDpadUL, 0, 0)
        grid.addWidget(self.btnDpadU, 0, 1)
        grid.addWidget(self.btnDpadUR, 0, 2)
        grid.addWidget(self.btnDpadR, 1, 2)
        grid.addWidget(self.btnDpadDR, 2, 2)
        grid.addWidget(self.btnDpadD, 2, 1)
        grid.addWidget(self.btnDpadDL, 2, 0)
        grid.addWidget(self.btnDpadL, 1, 0)

        self.btnGroup.addButton(self.btnDpadU)
        self.btnGroup.addButton(self.btnDpadL)
        self.btnGroup.addButton(self.btnDpadD)
        self.btnGroup.addButton(self.btnDpadR)
        self.btnGroup.addButton(self.btnDpadUR)
        self.btnGroup.addButton(self.btnDpadUL)
        self.btnGroup.addButton(self.btnDpadDL)
        self.btnGroup.addButton(self.btnDpadDR)

        self.btnGroup.buttonClicked.connect(self.check_buttons)
        self.btnGroup.setExclusive(False)

    def check_buttons(self,button):
        for x in self.btnGroup.buttons():
            if x is not button:
                x.setChecked(False)

class inputsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.inputButtonGroup = QButtonGroup(self)
        self.inputButtonGroup.setExclusive(False)
        self.btnA = inputButton("A", self)
        self.inputButtonGroup.addButton(self.btnA)
        self.btnB = inputButton("B", self)
        self.inputButtonGroup.addButton(self.btnB)
        self.btnX = inputButton("X", self)
        self.inputButtonGroup.addButton(self.btnX)
        self.btnY = inputButton("Y", self)
        self.inputButtonGroup.addButton(self.btnY)
        self.btnL = inputButton("L", self)
        self.inputButtonGroup.addButton(self.btnL)
        self.btnZL = inputButton("ZL", self)
        self.inputButtonGroup.addButton(self.btnZL)
        self.btnR = inputButton("R", self)
        self.inputButtonGroup.addButton(self.btnR)
        self.btnZR = inputButton("ZR", self)
        self.inputButtonGroup.addButton(self.btnZR)
        self.btnLC = inputButton("Left Click", self)
        self.inputButtonGroup.addButton(self.btnLC)
        self.btnRC = inputButton("Right Click", self)
        self.inputButtonGroup.addButton(self.btnRC)
        self.btnP = inputButton("+", self)
        self.inputButtonGroup.addButton(self.btnP)
        self.btnM = inputButton("-", self)
        self.inputButtonGroup.addButton(self.btnM)
        self.btnC = inputButton("Capture", self)
        self.inputButtonGroup.addButton(self.btnC)
        self.btnH = inputButton("Home", self)
        self.inputButtonGroup.addButton(self.btnH)

        grid.addWidget(self.btnA, 0, 0)
        grid.addWidget(self.btnB, 0, 1)
        grid.addWidget(self.btnX, 0, 2)
        grid.addWidget(self.btnY, 0, 3)
        grid.addWidget(self.btnL, 1, 0)
        grid.addWidget(self.btnZL, 1, 1)
        grid.addWidget(self.btnR, 1, 2)
        grid.addWidget(self.btnZR, 1, 3)
        grid.addWidget(self.btnLC, 2, 0)
        grid.addWidget(self.btnRC, 2, 1)
        grid.addWidget(self.btnP, 2, 2)
        grid.addWidget(self.btnM, 2, 3)
        grid.addWidget(self.btnC, 3, 0)
        grid.addWidget(self.btnH, 3, 1)

        inputValidator = QIntValidator(0,255,self)

        lX = QLabel('Left Stick X Value (0-255): ')
        self.lxValue = QLineEdit()
        self.lxValue.setValidator(inputValidator)
        self.lxValue.textChanged.connect(self.testStickInput)
        lY = QLabel('Left Stick Y Value (0-255): ')
        self.lyValue = QLineEdit()
        self.lyValue.setValidator(inputValidator)
        self.lyValue.textChanged.connect(self.testStickInput)
        rX = QLabel('Right Stick X Value (0-255): ')
        self.rxValue = QLineEdit()
        self.rxValue.setValidator(inputValidator)
        self.rxValue.textChanged.connect(self.testStickInput)
        rY = QLabel('Right Stick Y Value (0-255): ')
        self.ryValue = QLineEdit()
        self.ryValue.setValidator(inputValidator)
        self.ryValue.textChanged.connect(self.testStickInput)

        grid.addWidget(lX, 4, 0,1,2)
        grid.addWidget(self.lxValue, 4, 2, 1, 2)
        grid.addWidget(lY, 5, 0, 1, 2)
        grid.addWidget(self.lyValue, 5, 2, 1, 2)
        grid.addWidget(rX, 6, 0, 1, 2)
        grid.addWidget(self.rxValue, 6, 2, 1, 2)
        grid.addWidget(rY, 7, 0, 1, 2)
        grid.addWidget(self.ryValue, 7, 2, 1, 2)

        dpadLabel = QLabel('Dpad Buttons:')
        grid.addWidget(dpadLabel, 8, 0,1,2)
        self.hat = dpadButtons()
        grid.addWidget(self.hat, 9, 0, 3, 3)

        durationVal = QDoubleValidator(self)
        regVal = QRegularExpressionValidator(QRegularExpression("^[0-9]*\.[0-9]{2}"))

        durationLabel = QLabel('Input Duration (Seconds):')
        self.durationValue = QLineEdit()
        self.durationValue.setValidator(regVal)
        self.durationValue.textChanged.connect(self.testDouble)

        grid.addWidget(durationLabel,12,0,1,2)
        grid.addWidget(self.durationValue, 12, 2, 1, 2)

        commentLabel = QLabel("Comment")
        self.commentInput = QPlainTextEdit(self)

        grid.addWidget(commentLabel, 13,0)
        grid.addWidget(self.commentInput, 14,0,4,4)
    
    def testStickInput(self):
        sender = self.sender()
        if len(sender.text()) > 1 and int(sender.text()[0]) == 0:
            sender.setText('0')
        
        if len(sender.text()) > 2 and int(sender.text()) > 255:
            sender.setText(sender.text()[0:2])
        
    def testDouble(self):
        sender = self.sender()
        if len(sender.text()) > 1 and sender.text()[0] == '0' and sender.text()[1] != '.':
            sender.setText('0')
       
class DataObj(dict):
    def __init__(self,**kwargs):
        super(DataObj, self).__init__(**kwargs)

class Object(object):
    def __init__(self,data_obj):
        super(Object,self).__init__()
        self.data_obj = data_obj

class customList(QListWidget):
    def __init__(self,parent):
        self.parent = parent
        super().__init__()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            if(self.currentRow()-1 <= 0):
                self.parent.previousSelection = self.item(0)
            else:
                self.parent.previousSelection = self.item(self.currentRow()-1)
        elif event.key() == Qt.Key.Key_Down:
            if(self.currentRow()+1 >= self.count()):
                self.parent.previousSelection = self.item(self.count())
            else:
                self.parent.previousSelection = self.item(self.currentRow()+1)
        return super().keyPressEvent(event)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        openAct = QAction(QIcon('open.png'), '&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open File')
        openAct.triggered.connect(self.file_open)

        saveFile = QAction("&Save File", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)

        newFile = QAction("&New File", self)
        newFile.setShortcut("Ctrl+N")
        newFile.setStatusTip("New File")
        newFile.triggered.connect(self.new_file)

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.instance().quit)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newFile)
        fileMenu.addAction(openAct)
        fileMenu.addAction(saveFile)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        self.initUI()

    def initUI(self):
        self.previousSelection = None
        self.edit = False
        central_widget = QWidget()
        layout = QGridLayout(central_widget)


        self.inputs = inputsWidget()
        self.inputs.setFixedSize(400,600)
        layout.addWidget(self.inputs,0,0)

        self.list = customList(self)
        self.list.setMinimumSize(500,300)
        self.list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.list.model().rowsMoved.connect(self.listCurrent_Changed)
        self.list.itemClicked.connect(self.listClick)
        self.list.installEventFilter(self)
        self.list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.provideContextMenu)

        self.serialList = QListWidget()
        self.serialList.setMinimumSize(500,300)


        layout.addWidget(self.list,0,1,5,1)
        layout.addWidget(self.serialList,0,2,5,1)


        self.serialPortLabel = QLabel(self)
        self.serialPortLabel.setText("Serial Port")
        self.serialPort = QLineEdit(self)
        self.serialPort.setMinimumWidth(150)
        self.serialPort.setMaximumWidth(200)

        self.countLabel = QLabel(self)
        self.countLabel.setText("Count")
        self.countVal = QLineEdit()
        val = QRegularExpressionValidator(QRegularExpression("[1-9][0-9]*"))
        self.countVal.setValidator(val)
        self.countVal.setMinimumWidth(150)
        self.countVal.setMaximumWidth(200)

        self.serialButton = QPushButton(self)
        self.serialButton.setText("Run Script")
        self.serialButton.clicked.connect(self.serialClick)
        self.stopSerialButton = QPushButton(self)
        self.stopSerialButton.setText("Stop Script")
        self.stopSerialButton.clicked.connect(self.serialStop)

        serialLayout = QVBoxLayout()
        serialLayout.addWidget(self.serialPortLabel)
        serialLayout.addWidget(self.serialPort)
        serialLayout.addWidget(self.countLabel)
        serialLayout.addWidget(self.countVal)
        serialLayout.addWidget(self.serialButton)
        serialLayout.addWidget(self.stopSerialButton)
        serialLayout.addStretch()

        layout.addLayout(serialLayout,0,3)



        self.submit = QPushButton('Submit')
        self.submit.setMaximumSize(200,200)
        self.submit.clicked.connect(self.submitClick)

        self.clear = QPushButton('Clear')
        self.clear.setMaximumSize(200,200)
        self.clear.clicked.connect(self.resetBoard)

        layout.addWidget(self.clear,3,0)
        layout.addWidget(self.submit, 4, 0)

        layout.setAlignment(self.inputs, Qt.AlignmentFlag.AlignTop)
        self.setCentralWidget(central_widget)

        self.setGeometry(50,50,1000,700)
        self.setWindowTitle('Switch Script Maker')
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'switch.png'))

        self.show()
    
    def serialStop(self):
        try:
            self.worker.kill()
        except:
            return
  
    def serialClick(self):
        self.serialList.clear()
        scriptItems  = [self.list.item(i) for i in range(self.list.count())]
        instructions = self.buildInstructions(scriptItems)
        count = 0
        if len(self.countVal.text()) == 0:
            count = 1
        else:
            count = int(self.countVal.text())
        
        self.thread = QThread(self)
        self.worker = Worker(scriptItems,instructions,count,self.serialPort.text())
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.error.connect(self.errorHandle)
        self.worker.update.connect(self.updateSerialList)
        self.worker.finished.connect(self.serialFinished)
        self.thread.start()

        self.serialButton.setEnabled(False)
        self.thread.finished.connect(lambda: self.serialButton.setEnabled(True))
        self.thread.exit()

    def errorHandle(self,n):
        self.serialList.addItem(str(n))
    
    def updateSerialList(self,n):
        self.serialList.addItem(n)
        self.serialList.scrollToBottom()
    
    def serialFinished(self):
        self.worker.deleteLater
        self.serialList.addItem("Script is Done")
        self.serialList.scrollToBottom()

    def buildInstructions(self,scriptItems):
        result = []
        for item in scriptItems:
            instructCount = 0
            temp = []
            if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('buttonOut') != 16384:
                temp.append(
                    item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('buttonOut'))
                instructCount += 1
            if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('lxOut') != None:
                temp.append(
                    item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('lxOut'))
                instructCount += 1
            if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('lyOut') != None:
                temp.append(
                    item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('lyOut'))
                instructCount += 1
            if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('rxOut') != None:
                temp.append(
                    item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('rxOut'))
                instructCount += 1
            if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('ryOut') != None:
                temp.append(
                    item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('ryOut'))
                instructCount += 1
            if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('hatOut') != None:
                temp.append(
                    item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('hatOut'))
                instructCount += 1
            temp.append(item.data(Qt.ItemDataRole.UserRole +
                          1).data_obj.get('durationOut'))
            result.append(instructCount)
            result.extend(temp)
        return result

    def provideContextMenu(self, pos):
        item = self.list.itemAt(pos)
        if item is not None:
            self.previousSelection = self.list.currentItem()
            self.edit = True
            menu = QMenu()
            edit = QAction("Edit")
            delete = QAction("Delete")
            menu.addAction(edit)
            menu.addAction(delete)
            action = menu.exec(self.list.mapToGlobal(pos))
            if action is delete:
                item_index = self.list.currentRow()
                self.edit = False
                self.list.takeItem(item_index)
                if self.list.currentRow() != -1:
                    self.list.currentItem().setSelected(False)
                    self.list.setCurrentRow(-1)
            elif action is edit:
                self.resetBoard()
                self.updateBoard(self.list)
    
    def listCurrent_Changed(self):
        self.previousSelection = self.list.currentItem()
        self.edit = False

    def listClick(self,widget):
        sender = self.sender()
        if self.previousSelection != None:
            if self.previousSelection == sender.currentItem():
                self.previousSelection = None
                sender.currentItem().setSelected(False)
                if self.edit:
                    self.edit = False
                    self.resetBoard()
                self.list.setCurrentRow(-1)
                return
            else:
                if self.edit:
                    self.edit = False
                    self.resetBoard()
                self.previousSelection = sender.currentItem()
        else:
            if self.edit:
                self.edit = False
                self.resetBoard()
            self.previousSelection = sender.currentItem()
    
    def submitClick(self):
        #Do input validation
        inputString = ""
        self.listEntry = QListWidgetItem()
        obj = Object(data_obj=DataObj( A = None, B = None, X = None, Y = None,
        L = None, ZL = None, R = None, ZR = None, Left_Click = None, Right_Click = None,
        Plus = None, Minus = None, Capture = None, Home = None, LX = None, LY = None, RX = None, RY = None,
        HAT = None, Duration = None, buttonOut = 16384, lxOut = None, lyOut = None, rxOut = None, 
        ryOut = None, hatOut = None, durationOut = 0, Comment = None ))
        self.listEntry.setData(Qt.ItemDataRole.UserRole+1,obj)

        durationInput = ""

        if self.inputs.durationValue.text():
            text = self.inputs.durationValue.text()
            size = len(text)
            try:
                self.listEntry.data(Qt.ItemDataRole.UserRole+1).data_obj['Duration'] = Decimal(self.inputs.durationValue.text())
                self.listEntry.data(Qt.ItemDataRole.UserRole+1).data_obj['durationOut'] = Decimal(self.inputs.durationValue.text())
            except (InvalidOperation, DecimalException):
                QMessageBox.critical(self,'Error', "Invalid Decimal for duration")
                return
            if size > 30:
                #Check if there is a decimal

                if text[size-3] == '.':
                    durationInput += 'Duration: ' + text[0:3] + "..." + text[size-5:size]
                else:
                    durationInput += 'Duration: ' + text[0:3] + "..." + text[size-2:size-1]
            else:
                durationInput += 'Duration: ' + text
        else:
            QMessageBox.critical(self,'Error',"Duration required")
            return

        if self.inputs.lxValue.text():
            inputString += ('LX:' + self.inputs.lxValue.text() + ' ')
            self.listEntry.data(
                Qt.ItemDataRole.UserRole+1).data_obj['LX'] = self.inputs.lxValue.text()
            self.listEntry.data(
                Qt.ItemDataRole.UserRole+1).data_obj['lxOut'] = 32768 + int(self.inputs.lxValue.text())
        
        if self.inputs.lyValue.text():
            inputString += ('LY:' + self.inputs.lyValue.text() + ' ')
            self.listEntry.data(
                Qt.ItemDataRole.UserRole+1).data_obj['LY'] = self.inputs.lyValue.text()
            self.listEntry.data(
                Qt.ItemDataRole.UserRole+1).data_obj['lyOut'] = 33024 + int(self.inputs.lyValue.text())

        if self.inputs.rxValue.text():
            inputString += ('RX:' + self.inputs.rxValue.text() + ' ')
            self.listEntry.data(
                Qt.ItemDataRole.UserRole+1).data_obj['RX'] = self.inputs.rxValue.text()
            self.listEntry.data(
                Qt.ItemDataRole.UserRole+1).data_obj['rxOut'] = 33280 + int(self.inputs.rxValue.text())

        if self.inputs.ryValue.text():
            inputString += ('RY:' + self.inputs.ryValue.text() + ' ')
            self.listEntry.data(
                Qt.ItemDataRole.UserRole+1).data_obj['RY'] = self.inputs.ryValue.text()
            self.listEntry.data(
                Qt.ItemDataRole.UserRole+1).data_obj['ryOut'] = 33536 + int(self.inputs.ryValue.text())

        
        buttons = self.inputs.inputButtonGroup.buttons()
        buttonsInput = ""
        for x in buttons:
            if x.isChecked():
                self.updateEntry(x.text())
                buttonsInput += x.text() + ' '
        
        buttonsInput += inputString

        dpadInput = ""

        if self.inputs.hat.btnGroup.checkedButton():
            dpadInput += 'DPad:' + self.inputs.hat.btnGroup.checkedButton().text() + ' '
            self.updateHat(self.inputs.hat.btnGroup.checkedButton().text())

        buttonsInput += dpadInput      
        buttonsInput += durationInput

        if self.inputs.commentInput.toPlainText() != "":
            buttonsInput += " Comment: " + self.inputs.commentInput.toPlainText()
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                            1).data_obj['Comment'] = self.inputs.commentInput.toPlainText()

        
        if buttonsInput:
            self.listEntry.setText(buttonsInput)
            if self.edit != True and len(self.list.selectedItems()) == 0:
                self.list.addItem(self.listEntry)
            elif self.edit ==True and len(self.list.selectedItems()) != 0:
                row = self.list.currentRow()
                self.list.takeItem(row)
                self.list.insertItem(row,self.listEntry)
                self.list.setCurrentRow(-1)
                self.edit = False
            elif self.edit != True and len(self.list.selectedItems()) != 0:
                self.list.insertItem(self.list.currentRow(),self.listEntry)
            self.list.scrollToBottom()
            self.resetBoard()

    def resetBoard(self):
        for x in self.inputs.inputButtonGroup.buttons():
            x.setChecked(False)

        for x in self.inputs.hat.btnGroup.buttons():
            x.setChecked(False)
        
        self.inputs.lxValue.setText('')
        self.inputs.lyValue.setText('')
        self.inputs.rxValue.setText('')
        self.inputs.ryValue.setText('')
        self.inputs.durationValue.setText('')
        self.inputs.commentInput.setPlainText('')

    def updateEntry(self,input):
        if(input == 'Y'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['Y'] = 1
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 1
        if(input == 'B'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['B'] = 2
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 2
        if(input == 'A'):
           self.listEntry.data(Qt.ItemDataRole.UserRole +
                               1).data_obj['A'] = 4
           self.listEntry.data(Qt.ItemDataRole.UserRole +
                               1).data_obj['buttonOut'] += 4
        if(input == 'X'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['X'] = 8
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 8
        if(input == 'L'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['L'] = 16
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 16
        if(input == 'R'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['R'] = 32
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 32
        if(input == 'ZL'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['ZL'] = 64
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 64
        if(input == 'ZR'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['ZR'] = 128
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 128
        if(input == '-'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['Minus'] = 256
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 256
        if(input == '+'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['Plus'] = 512
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 512
        if(input == 'Left Click'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['Left_Click'] = 1024
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 1024
        if(input == 'Right Click'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['Right_Click'] = 2048
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 2048
        if(input == 'Home'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['Home'] = 4096
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 4096
        if(input == 'Capture'):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['Capture'] = 8192
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['buttonOut'] += 8192
    
    def updateHat(self,input):
        if(input == "↑"):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['HAT'] = 0
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['hatOut'] = 49152
        if(input == "↗"):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['HAT'] = 1
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                            1).data_obj['hatOut'] = 49153
        if(input == "→"):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['HAT'] = 2
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['hatOut'] = 49154
        if(input == "↘"):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['HAT'] = 3
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['hatOut'] = 49155
        if(input == "↓"):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['HAT'] = 4
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['hatOut'] = 49156
        if(input == "↙"):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['HAT'] = 5
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['hatOut'] = 49157
        if(input == "←"):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['HAT'] = 6
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['hatOut'] = 49158
        if(input == "↖"):
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['HAT'] = 7
            self.listEntry.data(Qt.ItemDataRole.UserRole +
                                1).data_obj['hatOut'] = 49159
    
    def updateBoard(self,sender):
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('Y') != None:
            self.inputs.btnY.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('B') != None:
            self.inputs.btnB.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('A') != None:
            self.inputs.btnA.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('X') != None:
            self.inputs.btnX.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('L') != None:
            self.inputs.btnL.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('R') != None:
            self.inputs.btnR.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('Minus') != None:
            self.inputs.btnM.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('Plus') != None:
            self.inputs.btnP.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('ZL') != None:
            self.inputs.btnZL.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('ZR') != None:
            self.inputs.btnZR.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('Left_Click') != None:
            self.inputs.btnLC.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('Right_Click') != None:
            self.inputs.btnRC.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('Home') != None:
            self.inputs.btnH.setChecked(True)
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('Capture') != None:
            self.inputs.btnC.setChecked(True)
        
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('LX') != None:
            self.inputs.lxValue.setText(str(sender.currentItem().data(
                Qt.ItemDataRole.UserRole+1).data_obj.get('LX')))
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('LY') != None:
            self.inputs.lyValue.setText(str(sender.currentItem().data(
                Qt.ItemDataRole.UserRole+1).data_obj.get('LY')))
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('RX') != None:
            self.inputs.rxValue.setText(str(sender.currentItem().data(
                Qt.ItemDataRole.UserRole+1).data_obj.get('RX')))
        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('RY') != None:
            self.inputs.ryValue.setText(str(sender.currentItem().data(
                Qt.ItemDataRole.UserRole+1).data_obj.get('RY')))

        choice = sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('HAT')
        if choice == 0:
            self.inputs.hat.btnDpadU.setChecked(True)
        elif choice == 1:
            self.inputs.hat.btnDpadUR.setChecked(True)
        elif choice == 2:
            self.inputs.hat.btnDpadR.setChecked(True)
        elif choice == 3:
            self.inputs.hat.btnDpadDR.setChecked(True)
        elif choice == 4:
            self.inputs.hat.btnDpadD.setChecked(True)
        elif choice == 5:
            self.inputs.hat.btnDpadDL.setChecked(True)
        elif choice == 6:
            self.inputs.hat.btnDpadL.setChecked(True)
        elif choice == 7:
            self.inputs.hat.btnDpadUL.setChecked(True)


        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('Duration') != None:
            self.inputs.durationValue.setText(str(sender.currentItem().data(
                Qt.ItemDataRole.UserRole+1).data_obj.get('Duration')))

        if sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('Comment') != None:
            self.inputs.commentInput.setPlainText(str(sender.currentItem().data(Qt.ItemDataRole.UserRole+1).data_obj.get('Comment')))

    def file_open(self):
        data_file_path = os.path.join(os.path.dirname(__file__))
        fname = QFileDialog.getOpenFileName(self, 'Open File', data_file_path,"Text files (*.txt)")
        path = fname[0]
        if path == '':
            return
        else:
            try:
                with open(path, "r") as f:
                    self.list.clear()
                    self.resetBoard()
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        firstSplit = line.split(',',1)
                        instructions = int(firstSplit[0])
                        restOfString = firstSplit[1].split(',', instructions+1)
                        obj = Object(data_obj=DataObj(A=None, B=None, X=None, Y=None,
                                                      L=None, ZL=None, R=None, ZR=None, Left_Click=None, Right_Click=None,
                                                      Plus=None, Minus=None, Capture=None, Home=None, LX=None, LY=None, RX=None, RY=None,
                                                      HAT=None, Duration=None, buttonOut=16384, lxOut=None, lyOut=None, rxOut=None,
                                                      ryOut=None, hatOut=None, durationOut=0, Comment=None))
                        newEntry = QListWidgetItem()
                        newEntry.setData(Qt.ItemDataRole.UserRole+1, obj)
                        if instructions != 0:
                            entryString = ""
                            for x in range(instructions):
                                choice = (int(restOfString[x]) & 49152) >> 14
                                num = int(restOfString[x])
                                if choice == 1:
                                    if num >> 2 & 1 == 1:
                                        entryString += "A "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['A'] = 4
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 4
                                    if num >> 1 & 1 == 1:
                                        entryString += "B "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['B'] = 2
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 2
                                    if num >> 3 & 1 == 1:
                                        entryString += "X "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['X'] = 8
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 8
                                    if num >> 0 & 1 == 1:
                                        entryString += "Y "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['Y'] = 1
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 1
                                    if num >> 4 & 1 == 1:
                                        entryString += "L "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['L'] = 16
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 16
                                    if num >> 6 & 1 == 1:
                                        entryString += "ZL "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['ZL'] = 64
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 64
                                    if num >> 5 & 1 == 1:
                                        entryString += "R "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['R'] = 32
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 32
                                    if num >> 7 & 1 == 1:
                                        entryString += "ZR "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['ZR'] = 128
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 128
                                    if num >> 10 & 1 == 1:
                                        entryString += "Left Click "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['Left_Click'] = 1024
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 1024
                                    if num >> 11 & 1 == 1:
                                        entryString += "Right Click "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['Right_Click'] = 2048
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 2048
                                    if num >> 9 & 1 == 1:
                                        entryString += "+ "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['Plus'] = 512
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 512
                                    if num >> 8 & 1 == 1:
                                        entryString += "- "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['Minus'] = 256
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 256
                                    if num >> 13 & 1 == 1:
                                        entryString += "Capture "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['Capture'] = 8192
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 8192
                                    if num >> 12 & 1 == 1:
                                        entryString += "Home "
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['Home'] = 4096
                                        newEntry.data(Qt.ItemDataRole.UserRole +
                                                      1).data_obj['buttonOut'] += 4096
                                elif choice == 2:
                                    stick = (num & 16383) >> 8
                                    val = num & 255
                                    if stick == 0:
                                        entryString += ('LX:' + str(val) + ' ')
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole+1).data_obj['LX'] = str(val)
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole+1).data_obj['lxOut'] = 32768 + val
                                    if stick == 1:
                                        entryString += ('LY:' +
                                                        str(val) + ' ')
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole+1).data_obj['LY'] = str(val)
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole+1).data_obj['lyOut'] = 33024 + val
                                    if stick == 2:
                                        entryString += ('RX:' +
                                                        str(val) + ' ')
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole+1).data_obj['RX'] = str(val)
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole+1).data_obj['rxOut'] = 33280 + val
                                    if stick == 3:
                                        entryString += ('RY:' +
                                                        str(val) + ' ')
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole+1).data_obj['RY'] = str(val)
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole+1).data_obj['ryOut'] = 33536 + val
                                elif choice == 3:
                                    input = num & 255
                                    if(input == 0):
                                        entryString += "Dpad: ↑ "
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['HAT'] = 0
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['hatOut'] = 49152
                                    if(input == 1):
                                        entryString += "Dpad: ↗ "
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['HAT'] = 1
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['hatOut'] = 49153
                                    if(input == 2):
                                        entryString += "Dpad: → "
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['HAT'] = 2
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['hatOut'] = 49154
                                    if(input == 3):
                                        entryString += "Dpad: ↘ "
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['HAT'] = 3
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['hatOut'] = 49155
                                    if(input == 4):
                                        entryString += "Dpad: ↓ "
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['HAT'] = 4
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['hatOut'] = 49156
                                    if(input == 5):
                                        entryString += "Dpad: ↙ "
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['HAT'] = 5
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['hatOut'] = 49157
                                    if(input == 6):
                                        entryString += "Dpad: ← "
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['HAT'] = 6
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['hatOut'] = 49158
                                    if(input == 7):
                                        entryString += "Dpad: ↖ "
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['HAT'] = 7
                                        newEntry.data(
                                            Qt.ItemDataRole.UserRole + 1).data_obj['hatOut'] = 49159
                            newEntry.data(
                                Qt.ItemDataRole.UserRole+1).data_obj['Duration'] = Decimal(restOfString[instructions])
                            newEntry.data(
                                Qt.ItemDataRole.UserRole+1).data_obj['durationOut'] = Decimal(restOfString[instructions])
                            entryString += "Duration: " + restOfString[instructions] + " "
                            if restOfString[-1] != "":
                                newEntry.data(
                                    Qt.ItemDataRole.UserRole+1).data_obj['Comment'] = restOfString[-1]
                                entryString += "Comment: " + restOfString[-1]
                            newEntry.setText(entryString)
                            self.list.addItem(newEntry)
                        else:
                            entryString = ""
                            newEntry.data(Qt.ItemDataRole.UserRole+1).data_obj['Duration'] = Decimal(restOfString[0])
                            newEntry.data(Qt.ItemDataRole.UserRole+1).data_obj['durationOut'] = Decimal(restOfString[0])
                            entryString += "Duration: " + restOfString[0] + " "
                            if restOfString[-1] != "":
                                newEntry.data(Qt.ItemDataRole.UserRole+1).data_obj['Comment'] = restOfString[-1]
                                entryString += "Comment: " + restOfString[-1]
                            newEntry.setText(entryString)
                            self.list.addItem(newEntry)
            except IOError as e:
                print("Error loading file")
    
    def file_save(self):
        data_file_path = os.path.join(os.path.dirname(__file__))
        name = QFileDialog.getSaveFileName(self, 'Save File', data_file_path)
        path = name[0]
        if path == '':
            return
        else:
            if path[-4:] != ".txt":
                path += ".txt"
            itemsToWrite = [self.list.item(i)
                            for i in range(self.list.count())]
            try:
                with open(path, 'w') as f:
                    for item in itemsToWrite:
                        toWrite = self.buildOutPutString(item)
                        f.write(toWrite)
            except IOError as e:
                print("Error saving file")
    
    def new_file(self):
        self.resetBoard()
        self.list.clear()
        self.edit = False

    def buildOutPutString(self, item):
        output = ""
        instructCount = 0
        if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('buttonOut') != 16384:
            output += str(item.data(Qt.ItemDataRole.UserRole +
                          1).data_obj.get('buttonOut')) + ","
            instructCount += 1
        if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('lxOut') != None:
            output += str(item.data(Qt.ItemDataRole.UserRole +
                          1).data_obj.get('lxOut')) + ","
            instructCount += 1
        if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('lyOut') != None:
            output += str(item.data(Qt.ItemDataRole.UserRole +
                          1).data_obj.get('lyOut')) + ","
            instructCount += 1
        if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('rxOut') != None:
            output += str(item.data(Qt.ItemDataRole.UserRole +
                          1).data_obj.get('rxOut')) + ","
            instructCount += 1
        if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('ryOut') != None:
            output += str(item.data(Qt.ItemDataRole.UserRole +
                          1).data_obj.get('ryOut')) + ","
            instructCount += 1
        if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('hatOut') != None:
            output += str(item.data(Qt.ItemDataRole.UserRole +
                          1).data_obj.get('hatOut')) + ","
            instructCount += 1
        output += str(item.data(Qt.ItemDataRole.UserRole +
                      1).data_obj.get('durationOut')) + ","
        if item.data(Qt.ItemDataRole.UserRole+1).data_obj.get('Comment') != None:
            output += item.data(Qt.ItemDataRole.UserRole +
                                1).data_obj.get('Comment') + "\n"
        else:
            output += "\n"
        output = str(instructCount) + "," + output
        return(output)

class Worker(QObject):
    error = pyqtSignal(SerialException)
    update = pyqtSignal(str)
    finished = pyqtSignal()
    def __init__(self, scriptItems, instructions, count, serialPort, parent=None):
        QObject.__init__(self,parent)
        self.scriptItems = scriptItems
        self.instructions = instructions
        self.count = count
        self.serialPort = serialPort
        self.check = True

    def run(self):
        try:
            with serial.Serial(self.serialPort, 9600) as ser:
                for _ in range(self.count):
                    self.x = 0
                    loc = 0
                    while loc < len(self.instructions) and self.check == True:
                        self.update.emit(self.scriptItems[self.x].text())
                        self.x += 1
                        instructCount = self.instructions[loc]
                        loc += 1
                        if instructCount != 0:
                            ser.write(instructCount.to_bytes(1, 'little'))
                            ser.read()
                            for x in range(instructCount):
                                temp = self.instructions[loc]
                                ser.write((temp & 0xff).to_bytes(1, 'little'))
                                ser.read()
                                ser.write(
                                    ((temp >> 8) & 0xff).to_bytes(1, 'little'))
                                ser.read()
                                loc += 1
                        else:
                            ser.write((1).to_bytes(1, 'little'))
                            ser.read()
                            ser.write((0).to_bytes(1, 'little'))
                            ser.read()
                            ser.write((0).to_bytes(1, 'little'))
                            ser.read()
                        time.sleep(float(self.instructions[loc]))
                        loc += 1
                ser.write((1).to_bytes(1,'little'))
                ser.read()
                ser.write((0).to_bytes(1,'little'))
                ser.read()
                ser.write((0).to_bytes(1,'little'))
                ser.read()
                self.finished.emit()
        except SerialException as e:
            self.error.emit(e)
        
    def kill(self):
        self.check = False


def main():

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

