from PyQt6.QtGui import *
#QFont, QResizeEvent
from PyQt6.QtWidgets import *
#QApplication, QLabel, QWidget, QToolButton, QFrame, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import *
#QParallelAnimationGroup, QAbstractAnimation, QPropertyAnimation, Qt, QSize
from PyQt6.QtMultimedia import QMediaDevices
from qfluentwidgets import *
import sys
from math import ceil
from win32api import GetSystemPowerStatus
from qframelesswindow import *
import threading
import gc
from pynput import keyboard

class selectDeviceComboBox(ComboBox):
    def __init__(self, deviceType, size, parent=None):
        super().__init__(parent=parent)
        self.setFont(QFont("Segoe UI", 8))
        self.setFixedSize(size)
        self.currentIndexChanged.connect(self.saveValue)
        self.savedValue="None"
        self.oldDeviceList=[]

        self.mediaDevices=QMediaDevices()
        if deviceType.lower()=='input':
            self.mediaDevices.audioInputsChanged.connect(lambda: self.loadDeviceItems(deviceType))
        elif deviceType.lower()=='output':
            self.mediaDevices.audioOutputsChanged.connect(lambda: self.loadDeviceItems(deviceType))
        else:
            raise Exception("Not a valid type of device combo box.")
        self.loadDeviceItems(deviceType)
    
    def saveValue(self):
        self.savedValue=self.currentText()

    def loadDeviceItems(self, deviceType):
        self.deviceList=["None"]

        if str(deviceType).lower()=='input':
            for i in self.mediaDevices.audioInputs():
                self.deviceList.append(i.description())
        elif str(deviceType).lower()=='output':
            for i in self.mediaDevices.audioOutputs():
                self.deviceList.append(i.description())
        else:
            raise Exception("Not a valid type of device combo box--only 'input' or 'output'")

        self.newDeviceList=self.deviceList
        avgCharSize=sum([self.fontMetrics().horizontalAdvance(i) for i in r" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()-_=+[]{}\|:;\"'<>,./?"])/85
        for i in range(len(self.deviceList)):
            if len(self.deviceList[i])>ceil((self.width()-10)/avgCharSize)-3:
                self.newDeviceList[i]=self.deviceList[i][0:ceil((self.width()-10)/avgCharSize)-3]
                self.newDeviceList[i]+="..."
        self.clear()
        self.addItems(self.newDeviceList)
        self.setCurrentIndex(self.findText(self.savedValue) if self.findText(self.savedValue)!=-1 else 0)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        return super().resizeEvent(a0)

    # def resizeEvent(self, event):
    #     self.newDeviceList=[]
    #     avgCharSize=sum([self.fontMetrics().horizontalAdvance(i) for i in r" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()-_=+[]{}\|:;\"'<>,./?"])/85
    #     for i in range(len(self.deviceList)):
    #         if len(self.deviceList[i])>ceil((self.width()-10)/avgCharSize)-3:
    #             self.newDeviceList[i]=self.deviceList[i][0:ceil((self.width()-10)/avgCharSize)-3]
    #             self.newDeviceList[i]+="..."
    #     self.clear()
    #     self.addItems(self.newDeviceList)

class ShortcutListner(threading.Thread):
    def __init__(self, shorcuts:dict()):
        pass

class CollapsibleSection(QWidget):
    def __init__(self, headerTitle="", sectionHeight=0, sectionAnimSpeed=500, windowAnimSpeed=500, parent=None):
        super().__init__(parent)
        self.parentWindow=parent
        self.maxContentHeight = sectionHeight
        self.minWindowHeight = []
        self.maxWindowHeight = []

        self.sectionAnimSpeed=sectionAnimSpeed
        self.windowAnimSpeed=windowAnimSpeed

        self.toggleButton = QPushButton(checkable=True, checked=False)
        self.toggleButton.setMinimumHeight(35)
        self.toggleButton.setLayout(QHBoxLayout())

        self.toggleButtonArrow=QLabel()
        a=FluentIcon.ARROW_DOWN.icon().pixmap(QSize(16,16))
        self.arrowIcon=[a,a.transformed(QTransform().scale(1, -1))]
        self.toggleButtonArrow.setPixmap(self.arrowIcon[0])
        self.toggleButtonArrow.setStyleSheet("background-color: rgba(211,205,208,0)")

        self.toggleButtonIcon=QLabel()
        self.toggleButtonIcon.setPixmap(QPixmap(FluentIcon.SETTING.icon().pixmap(QSize(16,16))))
        self.toggleButtonIcon.setStyleSheet("background-color: rgba(211,205,208,0)")

        self.toggleButtonLabel=QLabel(text=headerTitle)
        self.toggleButtonLabel.setStyleSheet("font: 11pt 'Segoe UI'; background-color: rgba(211,205,208,0); color: white;")

        #self.toggleButton.layout().addWidget(self.toggleButtonIcon)
        self.toggleButton.layout().addWidget(self.toggleButtonLabel,Qt.AlignmentFlag.AlignLeft)
        self.toggleButton.layout().addSpacerItem(QSpacerItem(5,1))
        self.toggleButton.layout().addWidget(self.toggleButtonArrow)
        self.toggleButton.layout().setContentsMargins(10,5,10,5)
        self.toggleButton.setStyleSheet("""
        QPushButton{background-color: rgba(211,205,208,0.2); border-radius: 5px;}
        QPushButton:hover{background-color: rgba(211,205,208,0.25); border-radius: 5px;}
        QPushButton:pressed{ background-color: rgba(211,205,208,0.15) ; border-radius: 5px; }
        """)
        #self.toggleButton.layout().setRowStretch(0,0)

        self.toggleButton.clicked.connect(self.on_pressed)

        self.contentFrame = QFrame(maximumHeight=0, minimumHeight=0)
        self.contentFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.contentFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.contentFrame.setStyleSheet("background-color: rgba(211,205,208,0.2); border-radius: 5px;")

        self.widgetLayout=QVBoxLayout(self)
        self.widgetLayout.setSpacing(0)
        self.widgetLayout.setContentsMargins(0,0,0,0)
        self.widgetLayout.addWidget(self.toggleButton)
        self.widgetLayout.addSpacerItem(QSpacerItem(1,10))
        self.widgetLayout.addWidget(self.contentFrame)
        self.widgetLayout.addStretch()

        self.setLayout(self.widgetLayout)

    def on_pressed(self):
        self.minWindowHeight = self.parentWindow.height() if self.minWindowHeight == [] else self.minWindowHeight
        #print(self.minWindowHeight, self.parentWindow.height())

        self.parentWindow.setMaximumSize(QWIDGETSIZE_MAX,QWIDGETSIZE_MAX)
        self.parentWindow.setMinimumSize(0,0)
        ischecked = self.toggleButton.isChecked()
        self.toggleButtonArrow.setPixmap(self.arrowIcon[1 if ischecked else 0])

        self.toggleAnimation=QParallelAnimationGroup()
        contentAnimation=QPropertyAnimation(self.contentFrame, b"maximumHeight")
        contentAnimation.setDuration(self.sectionAnimSpeed)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(self.maxContentHeight)
        self.toggleAnimation.addAnimation(contentAnimation)

        if not ischecked:
            windowAnimation=QPropertyAnimation(self.parentWindow, b"size")
            windowAnimation.setDuration(self.windowAnimSpeed)
            windowAnimation.setStartValue(QSize(self.parentWindow.width(),self.minWindowHeight))
            windowAnimation.setEndValue(QSize(self.parentWindow.width(),self.parentWindow.height()))
            self.toggleAnimation.addAnimation(windowAnimation)

        self.toggleAnimation.setDirection(QAbstractAnimation.Direction.Forward if ischecked else QAbstractAnimation.Direction.Backward)
        self.toggleAnimation.start()
        self.toggleAnimation.finished.connect(self.fixed)

    def fixed(self):
        self.parentWindow.setFixedSize(self.parentWindow.size())
        self.maxWindowHeight = self.parentWindow.height() if self.maxWindowHeight == [] else self.maxWindowHeight
        if int(self.parentWindow.height()) != int(self.minWindowHeight) and not self.toggleButton.isChecked():
            anim=QPropertyAnimation(self.parentWindow, b"size")
            anim.setDuration(50)
            anim.setStartValue(QSize(self.parentWindow.width(),self.parentWindow.height()))
            anim.setEndValue(QSize(self.parentWindow.width(),self.minWindowHeight))
            anim.start()
            self.parentWindow.setFixedHeight(self.minWindowHeight)

    def setContent(self, layout):
        self.contentFrame.setLayout(layout)

inputBoxStyle="""
TextEdit{
    background-color: rgba(0,0,0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 5px;
    font: 14px "Segoe UI", "Microsoft YaHei";
    padding: 0px 3px 0px 5px;
    color: white;
    selection-background-color: #29f1ff;
    selection-color: black;
}
TextEdit:focus{
    background-color: rgba(30, 30, 30, 0.7);
}
TextEdit:disabled{
    color: white;
    background-color: rgba(0,0,0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.0698);
}
"""

lineEditStyle=""""""

class AcrylicDialog(QDialog, FramelessWindow):
    def __init__(self, title="", loadDict=list(), parent=None):
        super().__init__(parent)
        self.personalDict=loadDict
        self.initWindowSettings()
        self.initTitleBar()
        self.initContent()
        self.initButtonBar()
        self.initLayout()

    def initWindowSettings(self):
        self.setFixedSize(400,300)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint|Qt.WindowType.FramelessWindowHint|Qt.WindowType.MSWindowsFixedSizeDialogHint|Qt.WindowType.Window)
        self.titleBar.hide()
        self.windowEffect.enableBlurBehindWindow(self.winId())
        self.windowEffect.addWindowAnimation(self.winId())
        self.windowEffect.setAcrylicEffect(self.winId(), "30303090")
        self.setStyleSheet("background-color: transparent")

    # def keyPressEvent(self, event: QKeyEvent) -> None:
    #     if event==Qt.Key.Key_Escape:
    #         return False

    def initTitleBar(self):
        self.helpBtn=QToolButton()
        self.helpBtn.setStyleSheet("""
        QToolButton{background-color: rgba(255,255,255,0); border-radius: 3px;}
        QToolButton:hover{background-color: rgba(255,255,255,0.15); border-radius: 3px;}
        QToolButton:pressed{ background-color: rgba(255,255,255,0.05) ; border-radius: 3px;}
        """)
        self.helpBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.helpBtn.setIcon(QIcon("resources/question.png"))
        self.helpBtn.setIconSize(QSize(18,18))
        self.helpBtn.clicked.connect(self.help)
        self.helpBtn.setFixedSize(28,28)
        self.helpBtn.setToolTip("Help")
        self.helpBtn.installEventFilter(ToolTipFilter(self.helpBtn, 300, ToolTipPosition.BOTTOM_LEFT))

        self.closeBtn=QToolButton()
        self.closeBtn.setStyleSheet(
        """
        QToolButton{background-color: rgba(255,255,255,0); border-radius: 3px;}
        QToolButton:hover{background-color: rgba(255,255,255,0.15); border-radius: 3px;}
        QToolButton:pressed{ background-color: rgba(255,255,255,0.05) ; border-radius: 3px;}
        """)
        self.closeBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.closeBtn.setIcon(QIcon("resources/close.png"))
        self.closeBtn.setIconSize(QSize(16,16))
        self.closeBtn.clicked.connect(self.chooseClose)
        self.closeBtn.setFixedSize(28,28)
        self.closeBtn.setToolTip("Close")
        self.closeBtn.installEventFilter(ToolTipFilter(self.closeBtn, 300, ToolTipPosition.BOTTOM_LEFT))

        self.warnClose=True

        spacer=QLabel()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
        spacer.setStyleSheet("background-color: rgba(255,255,255,0); border-radius: 3px;")
        self.titleBtnLayout=QGridLayout()
        self.titleBtnLayout.setContentsMargins(0,0,0,0)
        self.titleBtnLayout.setSpacing(0)
        self.titleBtnLayout.addWidget(spacer, 0,2)
        self.titleBtnLayout.addWidget(self.helpBtn, 0,3, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.titleBtnLayout.addItem(QSpacerItem(3,1),0,4)
        self.titleBtnLayout.addWidget(self.closeBtn, 0,5, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.titleBtnLayout.addItem(QSpacerItem(5,5),0,6)

        self.titleBtnLayoutFrame=QFrame()
        self.titleBtnLayoutFrame.setContentsMargins(0,0,0,0)
        #self.titleBtnLayoutFrame.installEventFilter(self)
        self.titleBtnLayoutFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.titleBtnLayoutFrame.setStyleSheet(frameStyleSheet[0])
        self.titleBtnLayoutFrame.setLayout(self.titleBtnLayout)
        self.titleBtnLayoutFrame.setFixedHeight(36)

        self.closeBtn.installEventFilter(self)
        self.helpBtn.installEventFilter(self)
        self.titleBtnLayoutFrame.installEventFilter(self)

    def eventFilter(self, obj, event): #overrides default enter with shift+enter
            if obj == self.titleBtnLayoutFrame:
                if event.type() == QEvent.Type.MouseButtonPress:
                    self.oldPos = event.globalPosition().toPoint()
                    self.setFocus()
                if event.type() == QEvent.Type.MouseMove:
                    delta = QPoint (event.globalPosition().toPoint() - self.oldPos)
                    self.move(self.x() + delta.x(), self.y() + delta.y())
                    self.oldPos = event.globalPosition().toPoint()
                if event.type() == QEvent.Type.Enter:
                    self.titleBtnLayoutFrame.setStyleSheet(frameStyleSheet[1])
                if event.type() == QEvent.Type.Leave:
                    self.titleBtnLayoutFrame.setStyleSheet(frameStyleSheet[0])
            if obj in (self.helpBtn, self.closeBtn):
                if event.type() == QEvent.Type.Enter:
                        self.titleBtnLayoutFrame.setStyleSheet(frameStyleSheet[0])
                if event.type() == QEvent.Type.Leave:
                        self.titleBtnLayoutFrame.setStyleSheet(frameStyleSheet[1])
            return super().eventFilter(obj, event)

    def chooseClose(self):
        # if self.warnClose:
        #     w= InfoBar.warning(
        #         title='WARNING',
        #         content=f"are you sure you want to close? closing will delete unsaved data",
        #         orient=Qt.Orientation.Vertical,
        #         isClosable=False,
        #         position=InfoBarPosition.BOTTOM_RIGHT,
        #         duration=4000,
        #         parent=self
        #     )
        #     w.setCustomBackgroundColor('white', '#202020')
        #     self.warnClose=False
        # else:
            self.reject()

    def help(self):
        w = InfoBar.new(
            icon=FluentIcon.HELP,
            title='',
            content=f"set up abbreviations",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self
        )
        w.setCustomBackgroundColor('white', '#202020') #text, bg

    def initContent(self):
        self.dictHeader=QHBoxLayout()
        self.dictHeader.setSpacing(0)
        replaceHeader=QLabel("Replace")
        replaceHeader.setStyleSheet("font: 12pt 'Segoe UI'; color: white; background: transparent;")
        replaceHeader.setFixedSize(150,20)
        replaceHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        withHeader=QLabel("With")
        withHeader.setStyleSheet("font: 12pt 'Segoe UI'; color: white; background: transparent;")
        withHeader.setFixedSize(150,20)
        withHeader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dictHeader.addWidget(replaceHeader, Qt.AlignmentFlag.AlignLeft)
        self.dictHeader.addItem(QSpacerItem(4,1))
        self.dictHeader.addWidget(withHeader, Qt.AlignmentFlag.AlignLeft)
        self.dictHeader.addItem(QSpacerItem(30,1))

        self.dictTableLayout=QVBoxLayout()
        self.dictTableLayout.addLayout(self.dictHeader)

        for i in self.personalDict:
            print(self.personalDict.index(i))
            rowLayout=QHBoxLayout()
            rowLayout.addWidget(i['ReplaceText'])
            rowLayout.addWidget(i['WithText'])
            rowLayout.addWidget(i['DeleteButton'])

            i['ReplaceText'].textChanged.connect(lambda: self.dictUpdated(self.personalDict.index(i)))
            i['WithText'].textChanged.connect(lambda: self.dictUpdated(self.personalDict.index(i)))
            i['DeleteButton'].clicked.connect(lambda: self.deleteRow(self.personalDict.index(i)))

            self.dictTableLayout.insertLayout(1,rowLayout)

        self.dictTableLayout.addItem(QSpacerItem(1,1,vPolicy=QSizePolicy.Policy.Expanding))

        self.dictTableContainer=QWidget()
        self.dictTableContainer.setStyleSheet("background: transparent;")
        self.dictTableFrame=SmoothScrollArea()
        self.dictTableFrame.setContentsMargins(0,0,0,0)
        #self.dictTableFrame.installEventFilter(self)
        self.dictTableFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.dictTableFrame.setStyleSheet(frameStyleSheet[0])
        self.dictTableFrame.setWidgetResizable(True)

        self.dictTableContainer.setLayout(self.dictTableLayout)
        self.dictTableFrame.setWidget(self.dictTableContainer)

    def addNewRow(self, row):
        newRow=dict()
        newRow['ReplaceText']=LineEdit()
        newRow['ReplaceText'].setFixedWidth(150)
        newRow['ReplaceText'].textChanged.connect(lambda: self.dictUpdated(row))

        newRow["WithText"]=LineEdit()
        newRow['WithText'].setFixedWidth(150)
        newRow['WithText'].textChanged.connect(lambda: self.dictUpdated(row))

        newRow['DeleteButton']=QToolButton()
        newRow['DeleteButton'].setIcon(FluentIcon.CLOSE.icon())
        newRow['DeleteButton'].setIconSize(QSize(15,15))
        newRow['DeleteButton'].setStyleSheet("background: transparent;")
        newRow['DeleteButton'].clicked.connect(lambda: self.deleteRow(row))

        rowLayout=QHBoxLayout()
        rowLayout.addWidget(newRow['ReplaceText'])
        rowLayout.addWidget(newRow['WithText'])
        rowLayout.addWidget(newRow['DeleteButton'])
        self.personalDict.append(newRow)

        self.dictTableLayout.insertLayout(1,rowLayout)

    def deleteRow(self, row):
        print(row)
        print(self.personalDict[row])
        del self.personalDict[row]
        gc.collect()
        for i in [self.dictTableLayout.itemAt(row).itemAt(i).widget() for i in range(self.dictTableLayout.itemAt(row).count())]:
            i.setParent(None)
        self.dictTableLayout.removeItem(self.dictTableLayout.itemAt(row))

        #replace layout with frame
        for i in self.personalDict:
            i['ReplaceText'].disconnect()
            i['WithText'].disconnect()
            i['DeleteButton'].disconnect()
            i['ReplaceText'].textChanged.connect(lambda: self.dictUpdated(self.personalDict.index(i)))
            i['WithText'].textChanged.connect(lambda: self.dictUpdated(self.personalDict.index(i)))
            i['DeleteButton'].clicked.connect(lambda: self.deleteRow(self.personalDict.index(i)))

    def dictUpdated(self, row):
        text=[self.personalDict[row]['ReplaceText'].text(), self.personalDict[row]['WithText'].text()]
        if text[0] and text[1]:
            try:
                self.personalDict[row+1]
            except:
                self.addNewRow(len(self.personalDict))

    def initButtonBar(self):
        self.acceptButton=QPushButton("Save")
        self.acceptButton.clicked.connect(self.accept)
        self.rejectButton=QPushButton("Cancel")
        self.rejectButton.clicked.connect(self.reject)

        self.btnLayout=QHBoxLayout()
        self.btnLayout.addWidget(self.acceptButton)
        self.btnLayout.addWidget(self.rejectButton)

    def initLayout(self):
        mainLayout=QVBoxLayout()
        mainLayout.setSpacing(5)
        mainLayout.addWidget(self.titleBtnLayoutFrame)
        mainLayout.addWidget(self.dictTableFrame)
        self.setLayout(mainLayout)

class TipSlider(QSlider):
    def __init__(self, *args, tip_offset=QPoint(-15, -40)):
        super(QSlider, self).__init__(*args)
        self.tip_offset = tip_offset

        self.style = QApplication.style()
        self.opt = QStyleOptionSlider()

        self.valueChanged.connect(self.show_tip)
        self.enterEvent = self.show_tip
        self.mouseReleaseEvent = self.show_tip

    def show_tip(self, _):
        self.initStyleOption(self.opt)
        rectHandle = self.style.subControlRect(self.style.ComplexControl.CC_Slider, self.opt, self.style.SubControl.SC_SliderHandle)

        pos_local = rectHandle.topLeft() + self.tip_offset
        pos_global = self.mapToGlobal(pos_local)
        QToolTip.showText(pos_global, str(self.value()), self)

class SliderToolTip(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


frameStyleSheet=["""background-color: rgba(255,255,255,0.2); border-radius: 5px;""" , """background-color: rgba(255,255,255,0.15); border-radius: 5px;"""]

"""QDialog {
    background-color: rgb(43, 43, 43);
}

#buttonGroup {
    background-color: rgb(32, 32, 32);
    border-top: 1px solid rgb(29, 29, 29);
    border-left: none;
    border-right: none;
    border-bottom: none;
}

MessageBox #buttonGroup {
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}

#centerWidget {
    border: 1px solid rgb(58, 58, 58);
    border-radius: 10px;
    background-color: rgb(43, 43, 43);
}

QLabel {
    background-color: transparent;
    color: white;
    border: none;
}

QLabel#titleLabel {
    font: 20px 'Segoe UI', 'Microsoft YaHei';
    padding: 0;
}

#contentLabel {
    padding: 0;
    font: 14px 'Segoe UI', 'Microsoft YaHei';
    border: none;
}

QLabel#windowTitleLabel {
    font: 12px 'Segoe UI', 'Microsoft YaHei';
    padding: 6px 6px;
    background-color: rgb(32, 32, 32);
}

#cancelButton {
    background: rgb(45, 45, 45);
    border: 1px solid rgb(48, 48, 48);
    border-top: 1px solid rgb(53, 53, 53);
    border-radius: 5px;
    color: white;
    font: 14px 'Segoe UI', 'Microsoft YaHei';
    padding: 5px 9px 6px 9px;
}

#cancelButton:hover {
    background: rgb(50, 50, 50);
}

#cancelButton:pressed {
    color: rgba(255, 255, 255, 0.63);
    background: rgb(39, 39, 39);
    border: 1px solid rgb(48, 48, 48);
}

#cancelButton:disabled {
    color: rgba(255, 255, 255, 0.63);
    background: rgb(59, 59, 59);
    border: 1px solid rgb(80, 80, 80);
}"""


# class ToolButton(QToolButton):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#     def sizeHint(self):
#         hint = super().sizeHint()
#         if hint.width() & 1:
#             hint.setWidth(hint.width() + 1)
#         if hint.height() & 1:
#             hint.setHeight(hint.height() + 1)
#         return hint

# app = QApplication(sys.argv)
# window = selectDeviceComboBox('input')
# window.show()
# sys.exit(app.exec())