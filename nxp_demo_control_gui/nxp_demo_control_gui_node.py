#!/usr/bin/env python3
import rclpy
import time
import os
from rclpy.node import Node
from std_msgs.msg import Bool
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class NXPDemoControlGUI(Node, QWidget):
    def __init__(self):
        super().__init__("nxp_demo_control_gui")
        QWidget.__init__(self)

        self.extraPath = os.path.realpath(os.path.relpath(os.path.join(os.path.realpath(__file__).replace("nxp_demo_control_gui_node.py",""),"../extras")))


        self.SystemReadyPub  = self.create_publisher(Bool, '/SystemReady', 10)
        self.UsePWMOutputPub  = self.create_publisher(Bool, '/UsePWMOutput', 10)

        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowTitle("NXP DEMO CONTROL")
        self.setWindowIcon(QIcon(os.path.join(self.extraPath,'NXPDemoControl.png')))

        self.SystemReadyCheckbox = QCheckBox("System is Ready  ")
        self.SystemReadyCheckbox.setChecked(False)
        self.SystemReadyCheckbox.toggled.connect(self.onSystemReadyClicked)
        layout.addWidget(self.SystemReadyCheckbox, 0, 1)


        self.UsePWMOutputCheckbox = QCheckBox("Use PWM Output  ")
        self.UsePWMOutputCheckbox.setChecked(False)
        self.UsePWMOutputCheckbox.toggled.connect(self.onUsePWMOutputClicked)
        layout.addWidget(self.UsePWMOutputCheckbox, 0, 0)

    def onSystemReadyClicked(self):
        msgSysReady = Bool()
        if self.SystemReadyCheckbox.isChecked():
            msgSysReady.data = True
            self.SystemReadyPub.publish(msgSysReady)
        if not self.SystemReadyCheckbox.isChecked():
            msgSysReady.data = False
            self.SystemReadyPub.publish(msgSysReady)

    def onUsePWMOutputClicked(self):
        msgUsePWM = Bool()
        if self.UsePWMOutputCheckbox.isChecked():
            msgUsePWM.data = True
            self.UsePWMOutputPub.publish(msgUsePWM)
        if not self.UsePWMOutputCheckbox.isChecked():
            msgUsePWM.data = False
            self.UsePWMOutputPub.publish(msgUsePWM)


def main(args=None):
    rclpy.init(args=args)
    app = QApplication(["NXP DEMO CONTROL"])
    
    GoPNG = os.path.realpath(os.path.relpath(os.path.join(os.path.join(os.path.realpath(__file__).replace("nxp_demo_control_gui_node.py",""),"../extras"),"Go.png")))
    StopPNG = os.path.realpath(os.path.relpath(os.path.join(os.path.join(os.path.realpath(__file__).replace("nxp_demo_control_gui_node.py",""),"../extras"),"Stop.png")))
    style = '''
    QWidget {{
        background-color: #8baed9;
    }}
    QCheckBox {{
        background-color: white;
        color: black;
        min-width:  165px;
        max-width:  165px;
        min-height: 40px;
        max-height: 40px;
        border-radius: 10px;
        border-width: 3px;
        border-color: #627a98;
        border-style: outset;
    }}
    QCheckBox:unchecked {{
        background-color: #e8b410;
    }}
    QCheckBox:checked {{
        background-color: #c9d121;
    }}
    QCheckBox::indicator {{
        width: 30px;
        height: 30px;
        left: 5px
    }}
    QCheckBox::indicator:unchecked {{ 
        image: url({:s});
    }}
    QCheckBox::indicator:unchecked:hover {{
        image: url({:s});
    }}
    QCheckBox::indicator:unchecked:pressed {{
        image: url({:s});
    }}
    QCheckBox::indicator:checked {{
        image: url({:s});
    }}
    QCheckBox::indicator:checked:hover {{
        image: url({:s});
    }}
    QCheckBox::indicator:checked:pressed {{
        image: url({:s});
    }}'''.format(StopPNG, StopPNG, StopPNG, GoPNG, GoPNG, GoPNG)

    app.setStyleSheet(style)
    NXPDCG=NXPDemoControlGUI()
    NXPDCG.show()
    while(app.exec_()):
        rclpy.spin(NXPDCG)
    NXPDCG.get_logger().info("Shutting down")
    NXPDCG.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
