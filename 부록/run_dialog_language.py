#!/bin/env python
#-*- coding: utf-8 -*-
    
from PyQt4.QtGui import *
import sys
from resource import get_message
 
# ui XML을 변환한 모듈 import
import vkvm_dialog

# vkvm_dialog 모듈 안의 Ui_Dialog 클래스로부터 파생
class XDialog(QDialog, vkvm_dialog.Ui_Dialog):
    
    def __init__(self):        
        QDialog.__init__(self)
        # setupUi() 메서드는 화면에 다이얼로그를 보여줌
        self.setupUi(self)
        self.set_resource()
        
    def set_resource(self):
        self.setWindowTitle(get_message("title"))
        self.tabWidget.setTabText(0, get_message("rack_tab_title"))
        self.tabWidget.setTabText(1, get_message("blade_tab_title"))
        self.connInfoBox.setTitle(get_message("conn_info"))
        self.ipLabel.setText(get_message("ip"))
        self.idLabel.setText(get_message("id"))
        self.pwLabel.setText(get_message("pw"))
        self.portLabel.setText(get_message("port"))
        self.addButton.setText(get_message("add"))
        self.removeButton.setText(get_message("delete"))
        self.connButton.setText(get_message("vkvm_conn"))
        self.bladeBox.setTitle(get_message("selected_blade"))
        self.statusBox.setTitle(get_message("status"))
        self.statusList.item(0).setText(get_message("status"))
        self.statusList.item(1).setText(get_message("status_ready"))
        self.statusList.item(2).setText(get_message("status_attached"))
        self.statusList.item(3).setText(get_message("status_etc"))
        self.statusList.item(3).setText(get_message("status_empty"))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = XDialog()
    dlg.show()
    app.exec_()
