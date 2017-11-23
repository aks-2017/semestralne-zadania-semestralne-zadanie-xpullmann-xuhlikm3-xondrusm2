import string
import requests
import json
from APP_GUI.gui import *
from AclRule import Acl as AclClass
from PyQt4 import QtCore, QtGui
from Forwarder import *

#myAcl = AclClass("192.168.2.1", "permit")
#myAcl.printState()
#print WebDev Branch test 2
ui = None
fwList = []
selectedFw = None


print ("udene klobasy")


def addNewRuleToAcl():
    # add New Rule to ACL from GUI text fields
    global ui
    print "Add new rule to acl"
    action = str(ui.guiCbAction.currentText())
    id = len(selectedFw.acl)+1
    srcMac = ui.guiLeSrcMac.text()
    dstMac = ui.guiLeDstMac.text()
    srcIp = ui.guiLeSrcIp.text()
    dstIp = ui.guiLeDstIp.text()
    srcPrefix = ui.guiLeSrcPrefix.text()
    dstPrefix =  ui.guiLeDstPrefix.text()
    l4Protocol = str(ui.guiCbL4Protocol.currentText())
    interface = str(ui.guiCbInterface.currentText())
    direction = str(ui.guiCbDirection.currentText())
    srcPortNumber = ui.guiLeSrcPortNumber.text()
    dstPortNumber = ui.guiLeDstPortNumber.text()

    selectedFw.addRuleToAcl(
        AclClass(action, id, srcMac, dstMac, srcIp, dstIp, srcPrefix, dstPrefix, l4Protocol,
                 interface, direction, srcPortNumber, dstPortNumber))
    loadSelectedForwarderToGuiTblFirewallRules()

def loadForwarders(list):
    global selectedFw

    # GET FOR NUMBER OF FORWARDERS
    r = requests.get('http://localhost:8080/stats/switches')
    result = r.content.translate(None, '[] ')

    # LAST ENTRY TAB #0 FOR IMPLICIT PERMIT
    mec = {"type": "GOTO_TABLE", "table_id": 1, }


    mn_position = 0
    for x in result.split(','):
        print x
        list.append(Forwarder(mn_position, "Forwarder s"+x))
        mn_position+1

        data = {"dpid": x, "table_id": "0", "priority": "0", "actions": [mec]}
        r2 = requests.post('http://localhost:8080/stats/flowentry/add', data=json.dumps(data))
        r2.status_code

    if mn_position == 0:
        list.append(Forwarder(mn_position, "No Forwarder connected"))

    if selectedFw is None:
        selectedFw = list[0]

def testFunctionForFW():
    selectedFw.addRuleToAcl( AclClass("permit", 1, "aa:aa:aa:bb:bb:bb", "cc:cc:cc:dd:dd:dd", "192.168.5.2", "192.168.3.5", 20, 25, "UDP","s0/0/0", "IN",123,456))
    selectedFw.addRuleToAcl(
        AclClass("deny", 2, "aa:aa:aa:bb:bb:bb", "cc:cc:cc:dd:dd:dd", "192.168.5.2", "192.168.3.5", 20, 25, "TCP",
                 "s0/0/0", "IN",321,654))
    selectedFw.printAclRules()


def loadSelectedForwarder(forwarderName):
    global fwList, selectedFw
    print "Searching Forwarder in fwList: "+forwarderName+" to GUI"
    for i in fwList:
        if i.name == forwarderName:
            print "I found forwarder: "+i.name+"i will load it to Table"
            selectedFw = i
    loadSelectedForwarderToGuiTblFirewallRules()

def loadSelectedForwarderToGuiTblFirewallRules():
    global selectedFw, ui
    ui.guiTblFirewallRules.setRowCount(0)
    index = 0
    ui.guiTblFirewallRules.setRowCount(len(selectedFw.acl))
    for i in selectedFw.acl:
        print "I will ad this rule"
        ui.guiTblFirewallRules.setItem(index,0, QtGui.QTableWidgetItem(str(i.id)))
        ui.guiTblFirewallRules.setItem(index, 1, QtGui.QTableWidgetItem(i.action))
        ui.guiTblFirewallRules.setItem(index, 2, QtGui.QTableWidgetItem(i.srcMac))
        ui.guiTblFirewallRules.setItem(index, 3, QtGui.QTableWidgetItem(i.dstMac))
        ui.guiTblFirewallRules.setItem(index, 4, QtGui.QTableWidgetItem(i.srcIp+"/"+str(i.srcPrefix)))
        ui.guiTblFirewallRules.setItem(index, 5, QtGui.QTableWidgetItem(i.dstIp+"/"+str(i.dstPrefix)))
        ui.guiTblFirewallRules.setItem(index, 6, QtGui.QTableWidgetItem(i.l4Protocol+" ("+str(i.srcPortNumber)+"/"+str(i.dstPortNumber)+")"))
        ui.guiTblFirewallRules.setItem(index, 7, QtGui.QTableWidgetItem(i.interface))
        ui.guiTblFirewallRules.setItem(index, 8, QtGui.QTableWidgetItem(i.direction))
        index += 1
    header = ui.guiTblFirewallRules.horizontalHeader()
    for x in range(0, 9):
        header.setResizeMode(x, QtGui.QHeaderView.ResizeToContents)

def actionPerformedGuiChbEnableFirewall():
    global ui
    if ui.guiChbEnableFirewall.isChecked():
        print "Firewall is activated"
    else:
        print "Firewall is deactivated"

def loadForwardersToGuiCbForwarder():
    global fwList
    global ui, selectedFw
    print "Loading Fw to Gui: "
    for i in fwList:
        print "Fw list: " + i.name
        ui.guiCbForwarder.addItem(i.name)

def actionPerformedGuiBtnDelete():
    global ui
    print "actionPerformedGuiBtnDelete"



    #POST FOR DELETION OF ENRTY
    #mec = {"type":"GOTO_TABLE", "table_id": 1}
    #data = {"dpid": "1", "table_id": "0", "priority": "22222", "actions": [mec]}
    #r2 = requests.post('http://localhost:8080/stats/flowentry/delete', data=json.dumps(data))
    #r2.status_code




def actionPerformedGuiBtnEdit():
    global ui
    print "actionPerformedGuiBtnEdit"


def loadUserData():
    ACL_match_data = {}

    if ui.guiLeSrcIp.text():
        ACL_match_data['nw_src'] = str(ui.guiLeSrcIp.text()) + '/' + str(ui.guiLeSrcPrefix.text())

    if ui.guiLeDstIp.text():
        ACL_match_data['nw_dst'] = str(ui.guiLeDstIp.text()) + "/" + str(ui.guiLeDstPrefix.text())

    if ui.guiLeSrcMac.text():
        ACL_match_data['dl_src'] = str(ui.guiLeSrcMac.text())

    if ui.guiLeDstMac.text():
        ACL_match_data['dl_dst'] = str(ui.guiLeDstMac.text())

    if ui.guiLeDstPortNumber.text():
        ACL_match_data['tp_dst'] = str(ui.guiLeDstPortNumber.text())

    if ui.guiLeSrcPortNumber.text():
        ACL_match_data['tp_src'] = str(ui.guiLeSrcPortNumber.text())

    if str(ui.guiCbL4Protocol.currentText()) == 'TCP':
        ACL_match_data['nw_proto'] = 6
    elif str(ui.guiCbL4Protocol.currentText()) == 'UDP':
        ACL_match_data['nw_proto'] = 17
    elif str(ui.guiCbL4Protocol.currentText()) == 'ICMP':
        ACL_match_data['nw_proto'] = 1

    return ACL_match_data


def actionPerformedGuiBtnCreate():
    global ui
    print "actionPerformedGuiBtnCreate"

    # POST FOR SPECIFIC ENTRY
    #DPID refers to (switchID + 1)

    interface = str(ui.guiCbInterface.currentText())
    direction = str(ui.guiCbDirection.currentText())

    ACL_result = {}
    if ui.guiCbAction.currentText() == 'Permit':
        ACL_result = {"type": "GOTO_TABLE", "table_id": 1}

    data = {"dpid": "2", "priority": "1", "table_id": "0", "match":
            dict(loadUserData(), **{'dl_type': '2048'}), "actions": [ACL_result]}

    r = requests.post('http://localhost:8080/stats/flowentry/add', data=json.dumps(data))
    r.status_code

    #addNewRuleToAcl()

def actionPerformedGuiCbForwarder():
    global ui
    print "Forwarder changed to: "+ui.guiCbForwarder.currentText()
    loadSelectedForwarder(ui.guiCbForwarder.currentText())

def actionPerformedGuiCbL4Protocol():
    global ui
    l4proto = ui.guiCbL4Protocol.currentText()
    print "L4 protocol changed to:"+l4proto
    if l4proto != "TCP" and l4proto != "UDP":
        print "Block Src/Dst port number lineEdit"
        ui.guiLeSrcPortNumber.setDisabled(True)
        ui.guiLeDstPortNumber.setDisabled(True)
    else:
        print "Unblock Src/Dst port number lineEdit"
        ui.guiLeSrcPortNumber.setDisabled(False)
        ui.guiLeDstPortNumber.setDisabled(False)

class GuiManager(Ui_MainWindow):

    def __init__(self):
        Ui_MainWindow.__init__(self)

    def start(self):
        # add action performed functions
        self.guiBtnDelete.clicked.connect(actionPerformedGuiBtnDelete)
        self.guiBtnCreate.clicked.connect(actionPerformedGuiBtnCreate)
        self.guiBtnEdit.clicked.connect(actionPerformedGuiBtnDelete)
        self.guiCbForwarder.currentIndexChanged.connect(actionPerformedGuiCbForwarder)
        self.guiChbEnableFirewall.stateChanged.connect(actionPerformedGuiChbEnableFirewall)
        self.guiCbL4Protocol.currentIndexChanged.connect(actionPerformedGuiCbL4Protocol)


if __name__ == "__main__":
    import sys
    print('Starting GUI')
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = GuiManager()
    ui.setupUi(MainWindow)
    ui.start()
    MainWindow.show()

    loadForwarders(fwList)
    loadForwardersToGuiCbForwarder()
    testFunctionForFW()
    loadSelectedForwarder(ui.guiCbForwarder.currentText())

    sys.exit(app.exec_())



