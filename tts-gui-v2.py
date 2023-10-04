import sys
from PyQt6.QtCore import *
#Qt, QSettings, QByteArray, QPoint, QSize
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *
#QGridLayout, QVBoxLayout, QLabel, QSpacerItem, QWidget, QPushButton, QSizePolicy, QApplication
from keyboard import is_pressed
from qt_customwidgets import *
from qframelesswindow import *
from qfluentwidgets import *
from win32api import GetSystemPowerStatus
from math import ceil
import pyttsx3
from faster_whisper import WhisperModel

#frame size
#print(QGuiApplication.primaryScreen().geometry())
"""

"""
class MainWindow(AcrylicWindow):
    def __init__(self, *args, parent=None):
        super().__init__(*args, parent=parent)
        self.readSettings()
        self.initListener()
        self.initMain()
        self.setFixedSize(500,self.minimumSizeHint().height())
        if self.firstRun:
            self.help()

    def initListener(self):
        pass

    def initMain(self):
        self.setWindowFlags(self.windowFlags()| Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.titleBar.hide()
        self.windowEffect.enableBlurBehindWindow(self.winId())
        self.windowEffect.addWindowAnimation(self.winId())
        self.windowEffect.setAcrylicEffect(self.winId(), "30303090")

        if GetSystemPowerStatus()['SystemStatusFlag']:
            QTimer().singleShot(10,self.powerWarning)

        setTheme(Theme.DARK)

        self.mainLayout=QVBoxLayout()
        self.mainContainer=QWidget()

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
        self.helpBtn.installEventFilter(self)
        self.helpBtn.setToolTip("Help")
        self.helpBtn.installEventFilter(ToolTipFilter(self.helpBtn, 300, ToolTipPosition.BOTTOM_LEFT))

        self.dictBtn=QToolButton()
        self.dictBtn.setStyleSheet("""
        QToolButton{background-color: rgba(255,255,255,0); border-radius: 3px;}
        QToolButton:hover{background-color: rgba(255,255,255,0.15); border-radius: 3px;}
        QToolButton:pressed{ background-color: rgba(255,255,255,0.05) ; border-radius: 3px;}
        """)
        self.dictBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.dictBtn.setIcon(QIcon('resources/book.png'))
        self.dictBtn.clicked.connect(self.openDict)
        self.dictBtn.setFixedSize(28,28)
        self.dictBtn.installEventFilter(self)
        self.dictBtn.setToolTip("Personal Dictionary")
        self.dictBtn.installEventFilter(ToolTipFilter(self.dictBtn, 300, ToolTipPosition.BOTTOM_LEFT))

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
        self.closeBtn.installEventFilter(self)
        self.closeBtn.setToolTip("Close")
        self.closeBtn.installEventFilter(ToolTipFilter(self.closeBtn, 300, ToolTipPosition.BOTTOM_LEFT))

        spacer=QLabel()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)
        spacer.setStyleSheet("background-color: rgba(255,255,255,0); border-radius: 3px;")
        self.titleBtnLayout=QGridLayout()
        self.titleBtnLayout.setContentsMargins(0,0,0,0)
        self.titleBtnLayout.setSpacing(0)
        self.titleBtnLayout.addItem(QSpacerItem(5,5),0,0)
        self.titleBtnLayout.addWidget(self.dictBtn, 0,1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.titleBtnLayout.addWidget(spacer, 0,2)
        self.titleBtnLayout.addWidget(self.helpBtn, 0,3, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.titleBtnLayout.addItem(QSpacerItem(3,1),0,4)
        self.titleBtnLayout.addWidget(self.closeBtn, 0,5, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.titleBtnLayout.addItem(QSpacerItem(5,5),0,6)

        self.titleBtnLayoutFrame=QFrame()
        self.titleBtnLayoutFrame.setContentsMargins(0,0,0,0)
        self.titleBtnLayoutFrame.installEventFilter(self)
        self.titleBtnLayoutFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.titleBtnLayoutFrame.setStyleSheet(frameStyleSheet[0])
        self.titleBtnLayoutFrame.setLayout(self.titleBtnLayout)
        self.titleBtnLayoutFrame.setFixedHeight(36)

        self.outputLabel=TextEdit()
        self.outputLabel.document().setPlainText("Waiting for input...")
        self.outputLabel.setReadOnly(True)
        self.outputLabel.setStyleSheet("border-radius: 5px; background-color: rgba(255,255,255,0.2); font: 11pt 'Segoe UI'; color: white;")
        self.outputLabel.setViewportMargins(5,5,5,5)
        self.outputLabel.setFixedHeight(60)
        self.outputLabel.viewport().setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        self.inputBox=TextEdit()
        self.inputBox.installEventFilter(self)
        self.inputBox.setPlaceholderText("Type something to get started!")
        self.inputBox.setFixedHeight(ceil(self.textHeight*3))
        self.inputBox.setStyleSheet(inputBoxStyle)
        # print(self.inputBox.styleSheet())
        self.inputBox.verticalScrollBar().setStyleSheet("background-color: red;")
        # print(self.inputBox.verticalScrollBar().styleSheet())
        # print(self.inputBox.verticalScrollBar().invertedControls())

        self.sendPauseIcon=[FluentIcon.SEND.icon(),QIcon('resources/pause-button.png')]
        self.inputButton=ToolButton()
        self.inputButton.setIcon(self.sendPauseIcon[0])
        self.inputButton.setCheckable(True)
        self.inputButton.setChecked(False)
        self.inputButton.setFixedSize(40,ceil(self.textHeight*3-2))
        self.inputButton.setIconSize(QSize(20,20))
        self.inputButton.clicked.connect(self.sendInput)
        self.sendPauseSheet=[
        """
        QToolButton{background-color: rgba(116, 183, 46, 0.5); border-radius: 5px; border: 1px solid rgba(255, 255, 255, 0.08);}
        QToolButton:hover{background-color: rgba(116, 183, 46, 0.6); border-radius: 5px; border: 1px solid rgba(255, 255, 255, 0.08);}
        QToolButton:pressed{ background-color: rgba(116, 183, 46, 0.4) ; border-radius: 5px; border: 1px solid rgba(255, 255, 255, 0.08);}
        """
        ,
        """
        QToolButton{background-color: rgba(241, 74, 94,0.5); border-radius: 5px; border: 1px solid rgba(255, 255, 255, 0.08);}
        QToolButton:hover{background-color: rgba(241, 74, 94, 0.6); border-radius: 5px; border: 1px solid rgba(255, 255, 255, 0.08);}
        QToolButton:pressed{ background-color: rgba(241, 74, 94,0.4) ; border-radius: 5px; border: 1px solid rgba(255, 255, 255, 0.08);}
        """
        ]
        self.inputButton.setStyleSheet(self.sendPauseSheet[0])
        self.inputButton.setToolTip("Start TTS\n(shift+enter)")
        self.inputButton.installEventFilter(ToolTipFilter(self.inputButton, 300, ToolTipPosition.BOTTOM_LEFT))

        self.inputFrame=QFrame()
        self.inputFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.inputFrame.setStyleSheet("background-color: rgba(255,255,255,0.2); border-radius: 5px;")
        self.inputFrame.setLayout(QHBoxLayout())
        self.inputFrame.layout().addWidget(self.inputBox)
        self.inputFrame.layout().addWidget(self.inputButton)
        self.inputFrame.setFixedHeight(ceil(self.textHeight*4))

        self.initSettings()

        # self.mainLayout.addLayout(self.titleBtnLayout)
        self.mainLayout.addWidget(self.titleBtnLayoutFrame)
        self.mainLayout.addSpacerItem(QSpacerItem(1,5))
        self.mainLayout.addWidget(self.outputLabel)
        self.mainLayout.addSpacerItem(QSpacerItem(1,5))
        self.mainLayout.addWidget(self.inputFrame)
        self.mainLayout.addSpacerItem(QSpacerItem(1,5))
        self.mainLayout.addWidget(self.settingsSection)

        self.setLayout(self.mainLayout)

    def powerWarning(self):
        w = InfoBar.warning(
                title='WARNING',
                content=f"power saving mode is on, so the {' '*18}acrylic window effect is disabled",
                orient=Qt.Orientation.Vertical,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,
                parent=self
            )
        w.setCustomBackgroundColor('white', '#202020')
        w.setFont(QFont('Segoe UI', 10))

    def openDict(self):
        self.dictDialog=AcrylicDialog("title", self.personalDict)
        self.dictDialog.accepted.connect(lambda: print("accept"))
        self.dictDialog.show() # connect dict dialog close to re-applying window stays on top to the mainwindow

    def help(self):
        w = InfoBar.new(
            icon=FluentIcon.HELP,
            title='help',
            content=f"ctrl+space to focus window{' '*21}shift+enter to send text{' '*26}drag titlebar to move window",
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,
            parent=self
        )
        w.setCustomBackgroundColor('white', '#202020') #text, bg

    def eventFilter(self, obj, event): #overrides default enter with shift+enter
        try:
            if obj is self.inputBox and event.type() == QEvent.Type.KeyPress:
                if is_pressed("return") and is_pressed("shift"):
                    self.inputBox.insertPlainText("\n")
                    #self.inputBox.verticalScrollBar()
                    return True
                elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                    if self.inputBox.document().toPlainText():
                        print(self.inputBox.document().toPlainText())
                        self.inputButton.setChecked(not self.inputButton.isChecked())
                        self.sendInput()
                    else: print('must have text')
                    return True
            elif obj in (self.inputFrame, self.outputLabel, self.titleBtnLayoutFrame):
                if obj is self.titleBtnLayoutFrame:
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
            elif obj in (self.helpBtn, self.closeBtn, self.dictBtn):
                if event.type() == QEvent.Type.Enter:
                        self.titleBtnLayoutFrame.setStyleSheet(frameStyleSheet[0])
                if event.type() == QEvent.Type.Leave:
                        self.titleBtnLayoutFrame.setStyleSheet(frameStyleSheet[1])
            return super().eventFilter(obj, event)
        except: return super().eventFilter(obj, event)

    def sendInput(self):
        if self.inputBox.document().toPlainText() or not self.inputButton.isChecked():
            if self.inputButton.isChecked():
                text=self.inputBox.document().toPlainText()
                self.rawtext=text.split(' ')
                self.inputBox.document().setPlainText('')
                self.inputBox.setPlaceholderText("Please wait for TTS to finish speaking, or pause.")
                self.outputLabel.setText(text)

                self.objThread = QThread(parent=self)
                self.obj = TTSThread(text, self.rate)
                self.obj.moveToThread(self.objThread)
                self.obj.finished.connect(self.startMediaPlayer) #change to recieve segments data
                self.objThread.started.connect(self.obj.doThing)
                # self.objThread.finished.connect(self.startMediaPlayer)
                self.objThread.start()

                print("starting tts process")
                # for segment in segments:
                #     for word in segment.words:
                #         print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))

            else:
                self.outputLabel.setText("Waiting for input...")
                self.inputBox.setPlaceholderText("Type something to get started!")
            self.inputButton.setIcon(self.sendPauseIcon[1 if self.inputButton.isChecked() else 0])
            self.inputButton.setStyleSheet(self.sendPauseSheet[1 if self.inputButton.isChecked() else 0])
            self.inputButton.setToolTip("Pause" if self.inputButton.isChecked() else "Start TTS")
            self.inputBox.setDisabled(self.inputBox.isEnabled())
        else:
            self.inputButton.setChecked(False)
            self.outputLabel.setText("Must input text to start.")

    def startMediaPlayer(self, segments):
        self.objThread.quit()
        print("starting mediaplayer and text update threads")

        self.objThread = QThread(parent=self)
        self.obj = playerThread(self.volume) #add device later
        self.obj.moveToThread(self.objThread)
        self.obj.finished.connect(self.objThread.quit)
        self.objThread.started.connect(self.obj.run)

        self.objThread2 = QThread(parent=self)
        self.obj2 = transcribeThread(segments, self.rawtext)
        self.obj2.moveToThread(self.objThread)
        self.obj2.finished.connect(self.objThread.quit)
        self.obj2.next_word.connect(self.updateTTSLabel)
        self.objThread2.started.connect(self.obj2.run)

        self.objThread.start()
        self.objThread2.start()

    def updateTTSLabel(self, wordIndex, rawtext):
        s=str()
        for x in range(len(rawtext)):
            if x==wordIndex:
                s+=f"<font color=\"red\">{rawtext[x]}</font> "
            else:
                s+=rawtext[x]+" "
        self.outputLabel.setText(s)

    def initSettings(self):
        self.primaryOutputSelectLayout=QVBoxLayout()
        self.primaryOutputLabel=QLabel("Primary Output:<font color = #ff0000> *</font>")
        self.primaryOutputLabel.setStyleSheet("background-color: rgba(255,255,255,0); font: 14px 'Segoe UI'; color: white;")
        self.primaryOutputDeviceCombo=selectDeviceComboBox('output', QSize(200,30))
        self.primaryOutputDeviceCombo.setStyleSheet(self.primaryOutputDeviceCombo.styleSheet().replace("font: 14px","font: 14px"))
        self.primaryOutputDeviceCombo.setCurrentIndex(self.primaryOutputDeviceCombo.findText(self.outputDevice1))
        #this ensures that when a new device is added, indexes won't be messed up
        self.primaryOutputDeviceCombo.currentTextChanged.connect(lambda device: self.selectedDeviceChange('out1', device))
        self.primaryOutputSelectLayout.addWidget(self.primaryOutputLabel)
        self.primaryOutputSelectLayout.addWidget(self.primaryOutputDeviceCombo)
        self.primaryOutputFrame=QFrame()
        self.primaryOutputFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.primaryOutputFrame.setStyleSheet("background-color: rgba(0,0,0,0.3); border-radius: 5px;")
        self.primaryOutputFrame.setLayout(self.primaryOutputSelectLayout)

        self.secondaryOutputSelectLayout=QVBoxLayout()
        self.secondaryOutputLabel=QLabel("Secondary Output:")
        self.secondaryOutputLabel.setStyleSheet("background-color: rgba(255,255,255,0); font: 14px 'Segoe UI'; color: white;")
        self.secondaryOutputDeviceCombo=selectDeviceComboBox('output', QSize(200,30))
        self.secondaryOutputDeviceCombo.setStyleSheet(self.primaryOutputDeviceCombo.styleSheet().replace("font: 14px","font: 14px"))
        self.secondaryOutputDeviceCombo.setCurrentIndex(self.secondaryOutputDeviceCombo.findText(self.outputDevice2))
        self.secondaryOutputDeviceCombo.currentTextChanged.connect(lambda device: self.selectedDeviceChange('out2', device))
        self.secondaryOutputSelectLayout.addWidget(self.secondaryOutputLabel)
        self.secondaryOutputSelectLayout.addWidget(self.secondaryOutputDeviceCombo)
        self.secondaryOutputFrame=QFrame()
        self.secondaryOutputFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.secondaryOutputFrame.setStyleSheet("background-color: rgba(0,0,0,0.3); border-radius: 5px;")
        self.secondaryOutputFrame.setLayout(self.secondaryOutputSelectLayout)

        sliderStyle = {
            "groove.height": 3,
            "sub-page.color": QColor(163, 131, 180),
            "add-page.color": QColor(255, 255, 255, 64),
            "handle.color": QColor(255, 255, 255),
            "handle.ring-width": 4,
            "handle.hollow-radius": 3,
            "handle.margin": 1
        }
        self.rateLayout=QVBoxLayout()
        self.rateLabel=QLabel(f"Rate: {self.rate}")
        self.rateLabel.setStyleSheet("background-color: rgba(255,255,255,0); font: 14px 'Segoe UI'; color: white;")
        self.rateSlider=TipSlider()
        self.rateSlider.setStyleSheet("background-color: rgba(255,255,255,0)")
        self.rateSlider.setStyle(HollowHandleStyle(sliderStyle))
        self.rateSlider.setOrientation(Qt.Orientation.Horizontal)
        self.rateSlider.setRange(0,200)
        self.rateSlider.setFixedSize(200,17)
        self.rateSlider.setSliderPosition(self.rate)
        self.rateSlider.valueChanged.connect(self.rateChanged)
        self.rateLayout.addWidget(self.rateLabel)
        self.rateLayout.addWidget(self.rateSlider, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.rateFrame=QFrame()
        self.rateFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.rateFrame.setStyleSheet("background-color: rgba(0,0,0,0.3); border-radius: 5px;")
        self.rateFrame.setLayout(self.rateLayout)

        self.volumeLayout=QVBoxLayout()
        self.volumeLabel=QLabel(f"Volume: {self.volume}")
        self.volumeLabel.setStyleSheet("background-color: rgba(255,255,255,0); font: 14px 'Segoe UI'; color: white;")
        self.volumeSlider=QSlider()
        self.volumeSlider.setStyleSheet("background-color: rgba(255,255,255,0)")
        self.volumeSlider.setStyle(HollowHandleStyle(sliderStyle))
        self.volumeSlider.setOrientation(Qt.Orientation.Horizontal)
        self.volumeSlider.setRange(0,100)
        self.volumeSlider.setFixedSize(200,17)
        self.volumeSlider.setSliderPosition(self.volume)
        self.volumeSlider.valueChanged.connect(self.volumeChanged)
        self.volumeLayout.addWidget(self.volumeLabel)
        self.volumeLayout.addWidget(self.volumeSlider, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.volumeFrame=QFrame()
        self.volumeFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.volumeFrame.setStyleSheet("background-color: rgba(0,0,0,0.3); border-radius: 5px;")
        self.volumeFrame.setLayout(self.volumeLayout)

        self.settingsSection=CollapsibleSection("Settings", sectionHeight=220, sectionAnimSpeed=150, windowAnimSpeed=150, parent=self) #height, anim speed, height, animspeed
        #self.settingsSection.toggleButton.setStyleSheet("background-color: rgba(255, 255, 255, 0); border 0px; color: dark-grey; font: 14px 'Segoe UI';")
        self.settingsSectionLayout=QGridLayout()
        self.settingsSectionLayout.addWidget(self.rateFrame,0,0)
        self.settingsSectionLayout.addWidget(self.volumeFrame,0,1)
        self.settingsSectionLayout.addWidget(self.primaryOutputFrame,1,0)
        self.settingsSectionLayout.addWidget(self.secondaryOutputFrame,1,1)
        self.settingsSection.setContent(self.settingsSectionLayout)

    def rateChanged(self, value):
        self.rate=value
        self.rateLabel.setText(f"Rate: {self.rate}")

    def volumeChanged(self, value):
        self.volume=value
        self.volumeLabel.setText(f"Volume: {self.volume}")

    def selectedDeviceChange(self, sender, value):
        if sender=="out1":
            self.outputDevice1=value
        elif sender=="out2":
            self.outputDevice2=value

    def readSettings(self):
        self.settings=QSettings("org name", "TTS")
        #self.settings.clear()
        self.settings.beginGroup('MainWindow')
        if self.settings.contains('firstRun'):
            self.firstRun=False
        else:
            self.firstRun=True

        if self.settings.contains('position'):
            self.move(self.settings.value("position"))
        else:
            self.move(200,200)

        if self.settings.contains('textHeight'):
            self.textHeight=self.settings.value('textHeight')
        else:
            testLabel=QLabel("test")
            testFont=testLabel.font()
            testFont.setPointSize(12)
            testLabel.setFont(testFont)
            self.textHeight=testLabel.fontMetrics().boundingRect(testLabel.text()).height()

        if self.settings.contains('outputDevice1'):
            self.outputDevice1=self.settings.value('outputDevice1')
        else:
            self.outputDevice1="None"

        if self.settings.contains('outputDevice2'):
            self.outputDevice2=self.settings.value('outputDevice2')
        else:
            self.outputDevice2="None"

        if self.settings.contains('rate'):
            self.rate=self.settings.value('rate')
        else:
            self.rate=100

        if self.settings.contains('volume'):
            self.volume=self.settings.value('volume')
        else:
            self.volume=100

        self.personalDict=[]

        print(self.settings.value('personalDictionary'))

        if self.settings.contains('personalDictionary'):
            for i in self.settings.value('personalDictionary'):
                loadRow=dict()
                loadRow['ReplaceText']=LineEdit()
                loadRow['ReplaceText'].setFixedWidth(150)
                loadRow['ReplaceText'].setText(i['ReplaceText'])
                # loadRow['ReplaceText'].setText(str(self.settings.value('personalDictionary').index(i)))

                loadRow["WithText"]=LineEdit()
                loadRow['WithText'].setFixedWidth(150)
                loadRow['WithText'].setText(i['WithText'])
                # loadRow['WithText'].setText(str(self.settings.value('personalDictionary').index(i)))

                loadRow['DeleteButton']=QToolButton()
                loadRow['DeleteButton'].setIcon(FluentIcon.CLOSE.icon(Theme.DARK))
                loadRow['DeleteButton'].setIconSize(QSize(15,15))
                loadRow['DeleteButton'].setStyleSheet("background: transparent;")

                self.personalDict.append(loadRow)

        loadRow=dict()
        loadRow['ReplaceText']=LineEdit()
        loadRow['ReplaceText'].setFixedWidth(150)

        loadRow["WithText"]=LineEdit()
        loadRow['WithText'].setFixedWidth(150)

        loadRow['DeleteButton']=QToolButton()
        loadRow['DeleteButton'].setIcon(FluentIcon.CLOSE.icon(Theme.DARK))
        loadRow['DeleteButton'].setIconSize(QSize(15,15))
        loadRow['DeleteButton'].setStyleSheet("background: transparent;")

        self.personalDict.append(loadRow)

        self.settings.endGroup()

    def writeSettings(self):
        self.settings.beginGroup('MainWindow')
        self.settings.setValue('position', QPoint(self.x(),self.y()))
        self.settings.setValue('textHeight', self.textHeight)
        self.settings.setValue('outputDevice1', self.outputDevice1)
        self.settings.setValue('outputDevice2', self.outputDevice2)
        self.settings.setValue('rate', self.rate)
        self.settings.setValue('volume', self.volume)
        self.settings.setValue('firstRun', True)
        #THIS NEEDS TO BE CHANGED

        saveDict=list()
        for i in self.personalDict:
            if i['ReplaceText'].text() and i['WithText'].text():
                saveDict.append({'ReplaceText':i['ReplaceText'].text(),'WithText':i['WithText'].text()})
        print(saveDict)
        self.settings.setValue('personalDictionary', saveDict)
        self.settings.endGroup()

    def chooseClose(self):
        self.update()
        self.close()

    def closeEvent(self, event):
        try: self.dictDialog.reject()
        except: pass
        self.writeSettings()

class TTSThread(QObject):
    finished=pyqtSignal(object)
    def __init__(self, text, rate):
        super().__init__()
        self.text=text
        self.rate=rate

    def doThing(self):
        print("initiating engine")
        self.engine = pyttsx3.init('sapi5')

        print("modifying properties")
        self.engine.setProperty('rate', self.rate)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('volume',1)

        print("writing tts file")
        self.engine.save_to_file(self.text , r'temp\test2.wav') #CHANGE THIS LATER
        self.engine.runAndWait()

        print("transcribing")
        self.model = WhisperModel("tiny", device="cpu", compute_type="auto", num_workers=4)
        segments, info = self.model.transcribe(r"temp\test2.wav", beam_size=2, word_timestamps=True, language='en')

        print("finished tts")
        self.finished.emit(list(segments))
        #need to send back segments

class playerThread(QObject):
    playing=pyqtSignal()
    finished=pyqtSignal()

    def __init__(self, volume):
        super().__init__()
        self.volume=volume

    def run(self):
        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self.mediaPlayerUpdate)
        self.audio_output = QAudioOutput(QMediaDevices.audioOutputs()[0])
        self.player.setAudioOutput(self.audio_output)
        filename = r"temp\test2.wav"
        self.player.setSource(QUrl.fromLocalFile(filename))
        self.audio_output.setVolume(self.volume)
        self.playing.emit()
        self.player.play()

    def mediaPlayerUpdate(self, status):
        print("status updated:", status)

class transcribeThread(QObject):
    next_word=pyqtSignal(object, object)
    finished=pyqtSignal()
    def __init__(self, segments, rawtext):
        super().__init__()
        self.segments=segments
        self.rawtext=rawtext

    def run(self):
        sentence=[]
        for segment in self.segments:
            for word in segment.words:
                sentence.append(word.word)

        for i in range(len(sentence)):
            self.next_word.emit(i, self.rawtext)
            loop = QEventLoop()
            QTimer.singleShot(int((word.end-word.start)*1000), loop.quit)
            loop.exec()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

