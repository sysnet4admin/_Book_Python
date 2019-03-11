#!/bin/env python
#-*- coding: utf-8 -*-
    
from PyQt4.QtGui import *
import sys
 
# ui XML을 변환한 모듈 import
import vkvm_dialog

# vkvm_dialog 모듈 안의 Ui_Dialog 클래스로부터 파생
class XDialog(QDialog, vkvm_dialog.Ui_Dialog):
    
    def __init__(self):        
        QDialog.__init__(self)
        # setupUi() 메서드는 화면에 다이얼로그 보여줌
        self.setupUi(self)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = XDialog()
    dlg.show()
    app.exec_()
