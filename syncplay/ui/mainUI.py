from PySide import QtCore, QtGui
from PySide.QtCore import QSettings, Qt
from PySide.QtGui import QApplication, QLineEdit, QCursor, QLabel, QCheckBox, QDesktopServices, QIcon
from syncplay import utils

import os
import sys

class MainDialog(QtGui.QDialog):
    
    def joinRoom(self):
        print "JOIN ROOM: " + self.roomInput.text() 
        self.roomInput.setText("")
        
    def seekPosition(self):
        print "SEEK POSITION: " + self.seekInput.text() 
        self.seekInput.setText("")
        
    def showList(self):
        print "SHOW USER LIST"
        
    def undoseek(self):
        print "UNDO LAST SEEK"
        
    def togglepause(self):
        print "PAUSE/UNPAUSE"
        
    def exitSyncplay(self):
        reply = QtGui.QMessageBox.question(self, "Syncplay",
                "Are you sure you want to exit Syncplay?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            sys.exit()
        
    def setOffset(self):
        newoffset, ok = QtGui.QInputDialog.getText(self,"Set Offset",
                "Offset (+/-):", QtGui.QLineEdit.Normal,
                "")
        if ok and newoffset != '':
            print "SET OFFSET: " + newoffset
        
    def openUserGuide(self):
        self.QtGui.QDesktopServices.openUrl("http://syncplay.pl/guide/")
        
    def addBottomLayout(self, dialog):
        dialog.bottomLayout = QtGui.QHBoxLayout()

        dialog.addRoomBox(MainDialog)
        dialog.addSeekBox(MainDialog)
        dialog.addMiscBox(MainDialog)

        dialog.bottomLayout.addWidget(dialog.roomGroup, Qt.AlignLeft)
        dialog.bottomLayout.addWidget(dialog.seekGroup, Qt.AlignLeft)
        dialog.bottomLayout.addWidget(dialog.miscGroup, Qt.AlignLeft)

        dialog.mainLayout.addLayout(dialog.bottomLayout, Qt.AlignLeft)

    
    def addRoomBox(self, dialog):
        dialog.roomGroup = QtGui.QGroupBox("Room")
        
        dialog.roomInput = QtGui.QLineEdit()
        dialog.roomButton = QtGui.QPushButton("Join room")
        dialog.roomButton.pressed.connect(self.joinRoom)
        dialog.roomLayout = QtGui.QHBoxLayout()
        dialog.roomInput.setMaximumWidth(150)
        
        dialog.roomLayout.addWidget(dialog.roomInput)
        dialog.roomLayout.addWidget(dialog.roomButton)
        
        dialog.roomGroup.setLayout(dialog.roomLayout)
        dialog.roomGroup.setFixedSize(dialog.roomGroup.sizeHint())
        
    def addSeekBox(self, dialog):
        dialog.seekGroup = QtGui.QGroupBox("Seek")
        
        dialog.seekInput = QtGui.QLineEdit()
        dialog.seekButton = QtGui.QPushButton("Seek to position")
        dialog.seekButton.pressed.connect(self.seekPosition)
        
        dialog.seekLayout = QtGui.QHBoxLayout()
        dialog.seekInput.setMaximumWidth(100)
        
        dialog.seekLayout.addWidget(dialog.seekInput)
        dialog.seekLayout.addWidget(dialog.seekButton)
        
        dialog.seekGroup.setLayout(dialog.seekLayout)
        dialog.seekGroup.setFixedSize(dialog.seekGroup.sizeHint())
        
    def addMiscBox(self, dialog):
        dialog.miscGroup = QtGui.QGroupBox("Other Commands")
        
        dialog.showListButton = QtGui.QPushButton("Show list")
        dialog.showListButton.pressed.connect(self.showList)
        dialog.unseekButton = QtGui.QPushButton("Undo last seek")
        dialog.unseekButton.pressed.connect(self.undoseek)
        dialog.pauseButton = QtGui.QPushButton("Toggle pause")
        dialog.pauseButton.pressed.connect(self.togglepause)
        
        dialog.miscLayout = QtGui.QHBoxLayout()
        dialog.miscLayout.addWidget(dialog.showListButton)
        dialog.miscLayout.addWidget(dialog.unseekButton)
        dialog.miscLayout.addWidget(dialog.pauseButton)
        
        dialog.miscGroup.setLayout(dialog.miscLayout)
        dialog.miscGroup.setFixedSize(dialog.miscGroup.sizeHint())
        
        

            
    def addMenubar(self, dialog):
        dialog.menuBar = QtGui.QMenuBar()
        
        dialog.fileMenu = QtGui.QMenu("&File", self)
        dialog.exitAction = dialog.fileMenu.addAction("E&xit")
        dialog.exitAction.triggered.connect(self.exitSyncplay)
        dialog.menuBar.addMenu(dialog.fileMenu)
        
        dialog.advancedMenu = QtGui.QMenu("&Advanced", self)
        dialog.setoffsetAction = dialog.advancedMenu.addAction("Set &Offset")
        dialog.setoffsetAction.triggered.connect(self.setOffset)
        dialog.menuBar.addMenu(dialog.advancedMenu)
        
        dialog.helpMenu = QtGui.QMenu("&Help", self)
        dialog.userguideAction = dialog.helpMenu.addAction("Open User &Guide")
        dialog.userguideAction.triggered.connect(self.openUserGuide)
        
        dialog.menuBar.addMenu(dialog.helpMenu)
        dialog.mainLayout.setMenuBar(dialog.menuBar)
        
    def NewMessage(self, message):
        self.outputbox.moveCursor(QtGui.QTextCursor.End)
        self.outputbox.insertHtml(message)
        self.outputbox.moveCursor(QtGui.QTextCursor.End)

    
    def __init__(self):
        
        super(MainDialog, self).__init__()
        self.QtGui = QtGui
        
        self.setWindowTitle("Syncplay - Main Window")
        self.mainLayout = QtGui.QVBoxLayout()
        
        self.outputbox = QtGui.QTextEdit()
        self.outputbox.setReadOnly(True)
               
        self.mainLayout.addWidget(self.outputbox)
        self.addBottomLayout(self)
        self.addMenubar(self)
        self.setLayout(self.mainLayout)
        self.resize(700,500)
        
        if sys.platform.startswith('linux'):
            resourcespath = utils.findWorkingDir() + "/resources/"
        else:
            resourcespath = utils.findWorkingDir() + "\\resources\\"
        self.setWindowIcon(QtGui.QIcon(resourcespath + "syncplay.png"))
        
        
        self.show()

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = MainDialog()
    sys.exit(app.exec_())
