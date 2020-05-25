# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # 设置主窗口
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(896, 632)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        # QSize(int width, int height);
        MainWindow.setMinimumSize(QtCore.QSize(896, 632))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        # 创建主窗口的子窗口
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        # 设置文本区域
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(977, 128))
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 160))
        self.textBrowser.setMouseTracking(True)
        self.textBrowser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "color: rgb(170, 10, 39);")
        self.textBrowser.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.textBrowser.setFrameShadow(QtWidgets.QFrame.Raised)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setMidLineWidth(0)
        self.textBrowser.setTabStopWidth(80)
        self.textBrowser.setOpenExternalLinks(False)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        # 创建 frame
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        # self.frame_2.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_2.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(20)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_3 = QtWidgets.QFrame(self.frame_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setStyleSheet("font: 25 9pt \"Microsoft JhengHei UI Light\";\n"
                                 "")
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        # 创建pushButton_5 "Import"
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_5.setStyleSheet(
            "QPushButton{background-color:rgba(225,225,225);border-style:inset;border-width:1px;border-radius:14px;border-color:rgba(255,0,0);font:87 9pt \"Arial Black\";color:rgba(0,0,0);padding:6px;}\n"
            "QPushButton:hover{background-color:rgba(204,204,204);border-color:rgba(225,225,255);color:rgba(255,255,255);}\n"
            "QPushButton:pressed{background-color:rgba(255,255,255,200);border-color:rgba(255,255,255,30);border-style:inset;color:rgba(0,0,0,100);}")
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.line_2 = QtWidgets.QFrame(self.frame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.verticalLayout.addWidget(self.frame_2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        # 创建 pushButton_2 "Configuration Statistic"
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setStyleSheet(
            "QPushButton{background-color:rgba(225,225,225);border-style:inset;border-width:1px;border-radius:14px;border-color:rgba(0,0,0);font:87 9pt \"Arial Black\";color:rgba(0,0,0);padding:6px;}\n"
            "QPushButton:hover{background-color:rgba(204,204,204);border-color:rgba(225,225,255);color:rgba(255,255,255);}\n"
            "QPushButton:pressed{background-color:rgba(255,255,255,200);border-color:rgba(255,255,255,30);border-style:inset;color:rgba(0,0,0,100);}\n"
            "")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 0, 1, 1)
        # 创建 pushButton_6 "Dns-ip-cache Duplicate Check"
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setStyleSheet(
            "QPushButton{background-color:rgba(225,225,225);border-style:inset;border-width:1px;border-radius:14px;border-color:rgba(0,0,0);font:87 9pt \"Arial Black\";color:rgba(0,0,0);padding:6px;}\n"
            "QPushButton:hover{background-color:rgba(204,204,204);border-color:rgba(225,225,255);color:rgba(255,255,255);}\n"
            "QPushButton:pressed{background-color:rgba(255,255,255,200);border-color:rgba(255,255,255,30);border-style:inset;color:rgba(0,0,0,100);}\n"
            "")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 4, 0, 1, 1)
        # 创建pushButton_4 "Grammar Check"
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setStyleSheet(
            "QPushButton{background-color:rgba(225,225,225);border-style:inset;border-width:1px;border-radius:14px;border-color:rgba(0,0,0);font:87 9pt \"Arial Black\";color:rgba(0,0,0);padding:6px;}\n"
            "QPushButton:hover{background-color:rgba(204,204,204);border-color:rgba(225,225,255);color:rgba(255,255,255);}\n"
            "QPushButton:pressed{background-color:rgba(255,255,255,200);border-color:rgba(255,255,255,30);border-style:inset;color:rgba(0,0,0,100);}\n"
            "")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 3, 0, 1, 1)
        # 创建pushButton "Generate Configuration"
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(180, 0))
        self.pushButton.setStyleSheet(
            "QPushButton{background-color:rgba(225,225,225);border-style:inset;border-width:1px;border-radius:14px;border-color:rgba(0,0,0);font:87 9pt \"Arial Black\";color:rgba(0,0,0);padding:6px;}\n"
            "QPushButton:hover{background-color:rgba(204,204,204);border-color:rgba(225,225,255);color:rgba(255,255,255);}\n"
            "QPushButton:pressed{background-color:rgba(255,255,255,200);border-color:rgba(255,255,255,30);border-style:inset;color:rgba(0,0,0,100);}\n"
            "")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        # 网格
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setStyleSheet("font: 25 9pt \"Microsoft JhengHei UI Light\";")
        self.textBrowser_2.setObjectName("textBrowser_2")
        # self.gridLayout.addWidget(self.textBrowser_2, 0, 1, 4, 1)
        self.gridLayout.addWidget(self.textBrowser_2, 0, 1, 5, 1)
        # 创建pushButton_3 "Free Entry ID"
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setStyleSheet(
            "QPushButton{background-color:rgba(225,225,225);border-style:inset;border-width:1px;border-radius:14px;border-color:rgba(0,0,0);font:87 9pt \"Arial Black\";color:rgba(0,0,0);padding:6px;}\n"
            "QPushButton:hover{background-color:rgba(204,204,204);border-color:rgba(225,225,255);color:rgba(255,255,255);}\n"
            "QPushButton:pressed{background-color:rgba(255,255,255,200);border-color:rgba(255,255,255,30);border-style:inset;color:rgba(0,0,0,100);}\n"
            "")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 0, 1, 1)
        #创建pushButton_7 "Http Anti Fraud Configuration"
        # self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton_7.setStyleSheet(
        #     "QPushButton{background-color:rgba(225,225,225);border-style:inset;border-width:1px;border-radius:14px;border-color:rgba(0,0,0);font:87 9pt \"Arial Black\";color:rgba(0,0,0);padding:6px;}\n"
        #     "QPushButton:hover{background-color:rgba(204,204,204);border-color:rgba(225,225,255);color:rgba(255,255,255);}\n"
        #     "QPushButton:pressed{background-color:rgba(255,255,255,200);border-color:rgba(255,255,255,30);border-style:inset;color:rgba(0,0,0,100);}\n"
        #     "")
        # self.pushButton_7.setObjectName("pushButton_7")
        # self.gridLayout.addWidget(self.pushButton_7,5,0,1,1)
        #
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setStyleSheet("color:rgba(0,0,0,80);")
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3, 0, QtCore.Qt.AlignRight)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 896, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "5GC_PCC_tools_v1.0"))
        # MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">   _____  __  __   _____          ___   </span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">  / ____||  \\/  | / ____|        / _ \\</span>    ____   ____ ____   _____ ___   ___  _     ____  </p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\"> | |     | \\  / || |  __   __ _ | (_) |</span>  |  _ \\ / ___/ ___| |_   _/ _ \\ / _ \\| |   / ___| </p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\"> | |     | |\\/| || | |_ | / _` | &gt; _ &lt; </span>  | |_) | |  | |       | || | | | | | | |   \\___ \\ </p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\"> | |____ | |  | || |__| || (_| || (_) |</span>  |  __/| |___ |___    | || |_| | |_| | |___ ___) |</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">  \\_____||_|  |_| \\_____| \\__,_| \\___/  </span> |_|    \\____\\____|   |_| \\___/ \\___/|_____|____/ </p></body></html>"))
        self.label.setText(_translate("MainWindow", "        Please import the SMF or UPF configuration"))
        self.pushButton_5.setText(_translate("MainWindow", "Import"))
        self.pushButton.setText(_translate("MainWindow", "Generate Configuration"))
        self.pushButton_2.setText(_translate("MainWindow", "Configuration statistics"))
        self.pushButton_3.setText(_translate("MainWindow", "Free Entry ID"))
        self.pushButton_4.setText(_translate("MainWindow", "Grammar Check"))
        self.pushButton_6.setText(_translate("MainWindow", "Dns-ip-cache Duplicate Check"))
        # self.pushButton_7.setText(_translate("MainWindow","Http Anti Fraud Configuration"))
        self.label_3.setText(_translate("MainWindow",
                                        "                                                         Report bug to cuicui.c.chen@nokia-sbell.com"))
