#!/bin/env python
#-*- coding: utf-8 -*-
    
from PyQt4.QtGui import *
from PyQt4 import *
import sys
import re
from vkvm_launch_dialog_cfg import *
from ssh_check_type import *
from resource import get_message
import threading
import time
import subprocess
 
# ui XML을 변환한 모듈 import
import vKVMLauncherDialogUI

blade_list = {}
connect_status = {}
green_icon = None
grey_icon = None
red_icon = None
orange_icon = None
blank_icon = None
# MyDiag 모듈 안의 Ui_MyDialog 클래스로부터 파생
class XDialog(QDialog, vKVMLauncherDialogUI.Ui_Dialog):
    
    def __init__(self):
        global green_icon, grey_icon, red_icon, orange_icon, blank_icon
        QDialog.__init__(self)
        # setupUi() 메서드는 화면에 다이얼로그 보여줌
        self.setupUi(self)
        self.set_resource()
        self.addButton.clicked.connect(self.add)
        self.removeButton.clicked.connect(self.remove)
        self.connButton.clicked.connect(self.connect_clicked)
        self.listWidget.itemSelectionChanged.connect(self.rack_select_changed)
        self.listWidget.itemDoubleClicked.connect(self.vkvm_connect_rack)
        self.treeWidget.itemSelectionChanged.connect(self.blade_select_changed)
        self.treeWidget.itemDoubleClicked.connect(self.vkvm_connect_blade)
        green_icon = QIcon("./green.png")
        grey_icon = QIcon("./grey.png")
        red_icon = QIcon("./red.png")
        orange_icon = QIcon("./orange.png")
        blank_icon = QIcon("./blank.png")        
        reload_cfg()
        self.refresh_rack_list()
        self.refresh_blade_tree()
        
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
        
    def selected_rack_tab(self) :
        if self.tabWidget.currentIndex() == 0 :
            return True
        return False
        
    def refresh_rack_list(self) :
        self.listWidget.clear()
        for conf_ip in get_ip_list():
            (conf_id, conf_pw, conf_type) = get_conf_info(conf_ip)
            if conf_type != "rack" :
                continue
            item = QListWidgetItem(conf_ip)
            if connect_status.get(conf_ip) != None and connect_status[conf_ip]:
                item.setIcon(green_icon)
            else :
                item.setIcon(grey_icon)
            self.listWidget.addItem(item)       
        item = QListWidgetItem(get_message("new_input"))
        item.setIcon(blank_icon)
        self.listWidget.addItem(item)
        
    def refresh_blade_tree(self) :
        self.treeWidget.clear()
        for conf_ip in get_ip_list():
            (conf_id, conf_pw, conf_type) = get_conf_info(conf_ip)
            if conf_type == "blade" :
                item = QTreeWidgetItem(self.treeWidget)  
                item.setText(0, conf_ip)
                self.append_chassis(item, conf_ip)
        item = QTreeWidgetItem(self.treeWidget)
        item.setText(0, get_message("new_input"))
        
    def refresh_current_tab(self) :
        reload_cfg()
        if self.selected_rack_tab():
            self.refresh_rack_list()
        else :
            self.refresh_blade_tree()  
                
    def get_conn_info_input(self): 
        cimc_ip = str(self.serverEdit.text())
        c_user = str(self.userEdit.text())
        c_password = str(self.passwordEdit.text())
        return (cimc_ip, c_user, c_password)

    def set_conn_info_input(self, cimc_ip, c_user, c_password): 
        self.serverEdit.setText(cimc_ip)
        self.userEdit.setText(c_user)
        self.passwordEdit.setText(c_password) 

    def get_port_num (self) :
        port_num = 22
        try :
            port_num = int(self.portEdit.text())
        except :
            port_num = 22
        return port_num
        
    def add(self):
        (cimc_ip, c_user, c_password) = self.get_conn_info_input()
        if cimc_ip == "" or c_user == "" or c_password == "":
            return False
        c_type = "rack"
        if not self.selected_rack_tab():
            c_type = "blade"             
        (exist_ip, exist_conf) = is_exist_conf(cimc_ip, c_user, c_password)
        # 수정
        if exist_conf :
            return False    # 변경사항이 없는 경우 특별한 동작없이 중단
        if exist_ip :
            (conf_id, conf_pw, conf_type) = get_conf_info(cimc_ip)
            if conf_type != c_type :    # 타입이 다른 매니저로 등록되어 있는 경우
                return False

        # 접속 테스트
        if not connect(cimc_ip, self.get_port_num(), c_user, c_password) :
            pop_msg(get_message("conn_fail"))
            (conf_id, conf_pw, conf_type) = get_conf_info(cimc_ip)
            if not exist_ip :
                return False    #추가에서 접속 실패의 경우
            self.userEdit.setText(conf_id)
            self.passwordEdit.setText(conf_id)            
            connect_status[cimc_ip] = False
            self.refresh_current_tab()
            return False
        # 추가
        if not exist_ip : 
            if c_type=="blade" : 
                (system_type, cmd_result) = check_type()
                if system_type != "UCSM_FI" :
                    pop_msg(get_message("no_ucs_man"))
                    return False
            set_cfg(cimc_ip, c_user, c_password, c_type)
        connect_status[cimc_ip] = True
        self.refresh_current_tab()
        return True
    
    def vkvm_connect_rack(self) :
        (cimc_ip, c_user, c_password) = self.get_conn_info_input()
        if  cimc_ip == "" :
            return
        if connect_status.get(cimc_ip) == None or connect_status[cimc_ip] == False :
            if not check_active(cimc_ip) :
                pop_msg(get_message("conn_fail"))
                connect_status[cimc_ip] = False    
                self.refresh_current_tab()
                return
        connect_status[cimc_ip] = True
        self.refresh_rack_list()
        self.refresh_current_tab()
        t = vKVM_launcher_Thread()
        t.cimc_ip = cimc_ip
        t.c_user = c_user
        t.c_password = c_password
        t.start()
        
    def vkvm_connect_blade(self) :
        (cimc_ip, c_user, c_password) = self.get_conn_info_input()
        if len(self.treeWidget.selectedItems()) == 0:
            return
        selected_item = self.treeWidget.selectedItems()[0]
        if selected_item.parent() == None :
            return
        chassis_info = str(selected_item.text(0))  
        t = vKVM_launcher_Thread()
        t.cimc_ip = cimc_ip
        t.c_user = c_user
        t.c_password = c_password
        t.chassis = chassis_info.split("/")[0]
        t.blade = chassis_info.split("/")[1]
        t.start()
            
    def connect_clicked(self):
        (cimc_ip, c_user, c_password) = self.get_conn_info_input()
        (exist_ip, exist_conf) = is_exist_conf(cimc_ip, c_user, c_password)
        if not exist_conf :
            if not self.add() :
                return
        if self.selected_rack_tab():
            self.vkvm_connect_rack()
        else :
            self.vkvm_connect_blade()
        
    def remove(self):
        remove_ip = ""
        if self.selected_rack_tab():
            selected_items = self.listWidget.selectedItems()
            if not selected_items:
                return
            remove_ip = str(selected_items[0].text())
        else :
            selected_items = self.treeWidget.selectedItems()
            if not selected_items:
                return      
            remove_ip = str(selected_items[0].text(0))  
        remove_cfg(remove_ip)
        self.refresh_current_tab()
        
    def rack_select_changed(self):
        if len(self.listWidget.selectedItems()) == 0 :
            return
        selected_item = self.listWidget.selectedItems()[0]
        cimc_ip = selected_item.text()
        if cimc_ip == get_message("new_input"): 
            self.set_conn_info_input("", "", "")
        else :
            (conf_id, conf_pw, conf_type) = get_conf_info(str(cimc_ip))
            self.set_conn_info_input(str(cimc_ip), conf_id, conf_pw)
            
    def get_chassis_list(self, cimc_ip, c_user, c_password) :
        global blade_list
        if connect(cimc_ip, self.get_port_num(), c_user, c_password) :
            ret = exec_cmd("show server status")
            close()
        rows = re.findall("[0-9]/[0-9] .*.", ret)
        chassis_list = {}
        for row in rows :
            columns = row.split("  ")
            i = len(columns) - 1
            while i >= 0 :
                if columns[i] == "" :
                    columns.pop(i)
                else :
                    columns[i] = columns[i].strip()
                i = i - 1
            server = columns[0]
            solt_status = ""
            availability = ""
            overall_status = ""
            discovery = ""
            if len(columns) > 1 : solt_status = columns[1]
            if len(columns) > 2 : availability = columns[2]
            if len(columns) > 3 : overall_status = columns[3]
            if len(columns) > 4 : discovery = columns[len(columns) - 1]
            chassis_list[server] = (
                solt_status, availability, overall_status, discovery)
        blade_list[cimc_ip] = chassis_list
        
    def set_chassis_detail(self, slot, avail, overall, discovery): 
        self.slotEdit.setText(slot)
        self.availEdit.setText(avail)
        self.overallEdit.setText(overall)
        self.discoveryEdit.setText(discovery)
        
    def blade_select_changed (self) :
        if len(self.treeWidget.selectedItems()) == 0 :
            return
        selected_item = self.treeWidget.selectedItems()[0]
        cimc_ip = ""
        if selected_item.parent() == None :
            if selected_item.text(0) == get_message("new_input"): 
                self.set_conn_info_input("", "", "")
                return
            else :
                cimc_ip = str(selected_item.text(0))
        else :
            cimc_ip = str(selected_item.parent().text(0))
        (conf_id, conf_pw, conf_type) = get_conf_info(cimc_ip)
        
        if selected_item.parent() == None :
            selected_item.takeChildren()
            # 선택한 샤시 정보 조회
            if blade_list.get(cimc_ip) == None :
                self.get_chassis_list(cimc_ip, conf_id, conf_pw)
            self.append_chassis(selected_item, cimc_ip) 
            self.removeButton.setDisabled(False)
            self.connButton.setDisabled(True)
        else :
            chassis_info = blade_list[cimc_ip][str(selected_item.text(0))]
            (solt_status, availability, overall_status, discovery) = chassis_info
            self.set_chassis_detail(
                solt_status, availability, overall_status, discovery)
            self.removeButton.setDisabled(True)
            self.connButton.setDisabled(False)
        self.set_conn_info_input(cimc_ip, conf_id, conf_pw)  

    def append_chassis(self, parent_item, cimc_ip) :
        if blade_list.get(cimc_ip) == None:
            return
        chassis_list = blade_list[cimc_ip]              
        server_list = chassis_list.keys()
        server_list.sort()            
        for server in server_list:                
            item = QTreeWidgetItem(parent_item)
            item.setText(0, server)
            (solt_status, availability, overall_status, discovery) = blade_list[cimc_ip][server]
            if availability.find("Unavailable") >= 0 and (
                overall_status.find("Associated") >= 0  or overall_status.find("OK")) :
                item.setIcon(0, green_icon)
            elif availability.find("Available") >= 0 and overall_status.find("UnAssociated") >= 0 :
                item.setIcon(0, orange_icon)
            elif availability != "" and overall_status != "" :
                item.setIcon(0, red_icon)
            else :
                item.setIcon(0, grey_icon)
        parent_item.setExpanded(True)
        self.set_chassis_detail("", "", "", "")

def pop_msg(msg):
    QtGui.QMessageBox.about(None, "Info", msg)

def check_active(hostname):
    response = subprocess.call("ping -n 1 " + hostname, shell=True)
    if response == 0:
        return True
    return False
        
class vKVM_launcher_Thread(threading.Thread):
    cimc_ip = ""
    c_user = ""
    c_password = ""
    chassis = ""
    blade = ""
    def run(self) :
        if self.chassis != "" and self.blade != "" :
            vKVM_launcher_blade(
                self.cimc_ip,self.c_user,self.c_password,self.chassis,self.blade)
        else :
            vKVM_launcher(self.cimc_ip,self.c_user,self.c_password)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = XDialog()
    dlg.show()
    app.exec_()
