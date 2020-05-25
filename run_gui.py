# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 21:27:33 2020

@author: cuichen
"""

import sys
import datetime
import os


from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from pcc_tool import *

from pccMainwindow import *
# import chardet

# def get_encoding(fn):
#     with open(fn,'rb') as f:
#         code = chardet.detect(f.read(100)).get('encoding')
#     return code



class md(Ui_MainWindow):
    def __init__(self,MainWindow):
        super(md,self).__init__()
        self.openfilepath = ''

    def bt_5(self):
        # self.textBrowser_2.setText('import successful')
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)

        if dialog.exec_():
            filenames = dialog.selectedFiles()
            #print filenames 返回的是列表，如下
            #[u'D:/userdata/cuichen/anaconda2/MyDir/CmgPccTools/BJSAEGW104BNK.cfg']
            configfile = filenames[0]
            try:
                obj = PccTool(configfile)
                host = obj.get_hostname()
                today = datetime.datetime.now().strftime("%Y%m%d")
                file_path = "D:\\"
                if not os.path.isdir(file_path):
                    file_path = os.path.join("C:\\","result")
                    if not os.path.isdir(file_path):
                        os.mkdir(file_path)
                self.textBrowser_2.setText("import " + filenames[0] + " successfully")
                self.openfilepath = configfile
                self.file_path = file_path
                self.obj = obj
                self.host = host
                self.today = today
                # print(self.obj,self.host,self.today,self.openfilepath)

            except Exception as e:
                # print(str(e))
                self.openfilepath = ''
                self.textBrowser_2.setText('Please import correct file!')


    def bt_0(self):
        if self.openfilepath != '':
            #print(self.openfilepath)
            self.textBrowser_2.setText('The process is running, please be patient!')
            self.statusbar.showMessage('running...')
            
            #file_path = dialog.getExistingDirectory()
            #print(file_path)
            self.textBrowser_2.setText('running')
            #fr = open(self.openfilepath, 'rb')
            #with fr:
            #   data = fr.readlines()
            #    data = [str(line, encoding='utf-8') for line in data]
            
            f_out = self.file_path  + "\\" + self.host + "_PCC_" + self.today + '.csv'
            #print(fw)

            self.obj.output_all_config(f_out)
            self.textBrowser_2.setText(f_out  + ' has been generated!')
            self.statusbar.showMessage('done',3000)

        else:
            self.textBrowser_2.setText("Firstly, Please import the cMG config!")


    def bt_3(self):
        if self.openfilepath != '':
            self.textBrowser_2.setText('The process is running, please be patient!')
            self.statusbar.showMessage('running...')

            f_out = self.file_path + "\\" + self.host + "_FreeEntryId_" + self.today + '.csv'
            self.obj.output_free_entry(f_out)

            self.textBrowser_2.setText(f_out + ' has been generated!')
            self.statusbar.showMessage('done', 3000)

        else:
            self.textBrowser_2.setText("Firstly, Please import the cMG config!")


    def bt_2(self):
        if self.openfilepath != '':
            self.textBrowser_2.setText('The process is running, please be patient!')
            self.statusbar.showMessage('running...')
            # 返回数据
            # prb, pr, pru, cru, sru, srul, chg, app_grp, app, entry
            counters = self.obj.get_mg_counter()
            prb = counters[0]
            pr = counters[1]
            pru = counters[2]
            cru = counters[3]
            sru = counters[4]
            srul = counters[5]
            chg = counters[6]
            app_grp = counters[7]
            app = counters[8]
            entry = counters[9]

            PRB = "policy-rule-base数量 :   " + str(prb) + "\n"
            PR = "policy-rule数量 :   " + str(pr) + "\n"
            PRU = "policy-rule-unit数量 :   " + str(pru) + "\n"
            CRU = "charging-rule-unit数量 :   " + str(cru) + "\n"
            SRU = "stat-rule-unit数量 :   " + str(sru) + "\n"
            SRUL = "sru-list数量(UPF) :   " + str(srul) + "\n"
            ENTRY = "entry数量 :   " + str(entry) + "\n"
            APP = "application数量 :   " + str(app) + "\n"
            CHG = "charging-group数量 :   " + str(chg) + "\n"
            APP_GRP = "app-group数量 :   " + str(app_grp) + "\n"
            self.textBrowser_2.setText(PRB + PR + PRU + CRU + SRU + SRUL + ENTRY + APP + CHG + APP_GRP)
            self.statusbar.showMessage('done', 3000)
        else:
            self.textBrowser_2.setText("Firstly, Please import the cMG config!")


    def bt_4(self):
        if self.openfilepath != '':
            self.textBrowser_2.setText('The process is running, please be patient!')
            self.statusbar.showMessage('running...')

            invalid_chg = self.obj.get_invalid_chg()
            invalid_app = self.obj.get_invalid_app()
            if not invalid_chg and not invalid_app:
                txt = "%s没有垃圾数据!"%self.host
            if invalid_chg:
                txt1 = "如下charing-group为多余数据,请核查!\n" + '\n'.join(invalid_chg)
            if invalid_app:
                txt2 = "如下application为多余数据,请核查!\n" + '\n'.join(invalid_app)
            if invalid_chg and not invalid_app:
                txt = txt1
            if not invalid_chg and invalid_app:
                txt = txt2
            if invalid_chg and invalid_app:
                txt = txt1 + "\n\n" + txt2

            self.textBrowser_2.setText(txt)
            self.statusbar.showMessage('done', 3000)

        else:
            self.textBrowser_2.setText("Firstly, Please import the cMG config!")


    def bt_6(self):
        if self.openfilepath != '':
            self.textBrowser_2.setText('The process is running, please be patient!')
            self.statusbar.showMessage('running...')

            res = self.obj.check_duplicate_cache()
            ##联通项目未配置dns-ip-cache
            if res:
                txt = ''
                for k,v in res.items():
                    if not v:
                        txt = txt + "%s没有重复项\n\n" %k
                    else:
                        txt = txt + "%s包含重复项,重复项如下：\n\n" %k
                        for rr in v:
                            txt = txt + str(rr[0]) + ' ' + str(rr[1]) + '次\n'
            else:
                txt = "%s没有配置dns-ip-cache" %self.host
            self.textBrowser_2.setText(txt)
            self.statusbar.showMessage('done', 3000)

        else:
            self.textBrowser_2.setText("Firstly, Please import the cMG config!")



if __name__ == '__main__':

    # 实例化了一个应用程序对象
    app = QApplication(sys.argv)
    # 设置程序图标
#    app.setWindowIcon(QIcon('nokia.ico'))
    # 创建主窗口
    mianWindow = QMainWindow()
    # 设置按钮功能
    ui = md(mianWindow)

    # build the widget tree on the parent widget(将对话框依附于主窗体)
    ui.setupUi(mianWindow)

    ui.pushButton_5.clicked.connect(ui.bt_5)
    ui.pushButton.clicked.connect(ui.bt_0)
    ui.pushButton_3.clicked.connect(ui.bt_3)
    ui.pushButton_2.clicked.connect(ui.bt_2)
    ui.pushButton_4.clicked.connect(ui.bt_4)
    ui.pushButton_6.clicked.connect(ui.bt_6)
    mianWindow.show()
    sys.exit(app.exec_())
