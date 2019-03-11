#!/bin/env python
#-*- coding: utf-8 -*-

from ucsmsdk.ucshandle import UcsHandle
from time import sleep

def create():
    from ucsmsdk.mometa.vnic.VnicSanConnPolicy import VnicSanConnPolicy
    from ucsmsdk.mometa.vnic.VnicFc import VnicFc
    from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf
    from ucsmsdk.mometa.vnic.VnicFcNode import VnicFcNode
  
    mo = VnicSanConnPolicy(parent_mo_or_dn="org-root", policy_owner="local",
                           name="TestSANConPolicy", descr="TestSANConPolicy")
    mo_1 = VnicFc(parent_mo_or_dn=mo, addr="derived", name="TestWWPNForSAN",
                  admin_host_port="ANY", admin_vcon="any", stats_policy_name="default",
                  admin_cdn_name="", switch_id="A", pin_to_group_name="",
                  pers_bind="disabled", pers_bind_clear="no", qos_policy_name="",
                  adaptor_profile_name="", ident_pool_name="test001", order="1",
                  nw_templ_name="", max_data_field_size="2048")
    mo_1_1 = VnicFcIf(parent_mo_or_dn=mo_1, name="default")
    mo_2 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="WWNtestPool",
                      addr="pool-derived")
    handle.add_mo(mo)
    handle.commit()

    
def modify_FcNode():
    from ucsmsdk.mometa.vnic.VnicSanConnPolicy import VnicSanConnPolicy
    from ucsmsdk.mometa.vnic.VnicFcNode import VnicFcNode

    mo = VnicSanConnPolicy(parent_mo_or_dn="org-root", policy_owner="local",
                           name="TestSANConPolicy", descr="Test SAN Connectivity Policy")
    mo_1 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="test", addr="pool-derived")
    handle.add_mo(mo, True)
    handle.commit()


def modify_Fc():
    from ucsmsdk.mometa.vnic.VnicSanConnPolicy import VnicSanConnPolicy
    from ucsmsdk.mometa.vnic.VnicFc import VnicFc

    mo = VnicSanConnPolicy(parent_mo_or_dn="org-root", policy_owner="local",
                           name="TestSANConPolicy",
                           descr="Test SAN Connectivity Policy Change Test")
    mo_1 = VnicFc(parent_mo_or_dn=mo, addr="derived", name="TestvHBA001",
                  admin_host_port="ANY", admin_vcon="any", stats_policy_name="default",
                  admin_cdn_name="", switch_id="A", pin_to_group_name="",
                  pers_bind="disabled", pers_bind_clear="no", qos_policy_name="",
                  adaptor_profile_name="", ident_pool_name="WWPNTEST001", order="1",
                  nw_templ_name="", max_data_field_size="2048")
    handle.add_mo(mo, True)
    handle.commit()

def modify_Group_StorageInit():
    from ucsmsdk.mometa.storage.StorageIniGroup import StorageIniGroup
    from ucsmsdk.mometa.vnic.VnicFcGroupDef import VnicFcGroupDef
    from ucsmsdk.mometa.storage.StorageInitiator import StorageInitiator

    mo = StorageIniGroup(parent_mo_or_dn="org-root/san-conn-pol-TestSANConPolicy",
                         name="Test01InitiatorG", descr="Test01InitiatorGroup Test",
                         group_policy_name="", policy_name="", policy_owner="local",
                         rmt_disk_cfg_name="")
    mo_1 = VnicFcGroupDef(parent_mo_or_dn=mo, storage_conn_policy_name="",
                          policy_owner="local", name="", descr="",
                          stats_policy_name="default")
    mo_2 = StorageInitiator(parent_mo_or_dn=mo, policy_owner="local",
                            name="TestWWPNForSAN", descr="")
    handle.add_mo(mo)
    handle.commit()

def remove():
    obj = handle.query_dn("org-root/san-conn-pol-TestSANConPolicy")
    handle.remove_mo(obj)
    handle.commit()

if __name__ == "__main__":
    global handle
    handle = UcsHandle("192.168.56.250", "ucspe", "ucspe")
    handle.login()

    print "****************************"
    print "1. Creation : Fc,Fclf,FcNoe" 
    print "****************************"
    create()
    sleep(60)

    print "*****************************"
    print "2. Modification : VnicFcNode"
    print "*****************************"
    modify_FcNode()
    sleep(60)

    print "*************************"
    print "3. Modification : VnicFc"
    print "*************************"
    modify_Fc()
    sleep(60)
 
    print "***************************************************"
    print "4. Modification : VnicFcGroupsDef,StorageInitiator"
    print "***************************************************"
    modify_Group_StorageInit()
    sleep(60)

    print "**************************"
    print "5. Removal : SANConPolicy"
    print "**************************"
    remove()
    handle.logout()
