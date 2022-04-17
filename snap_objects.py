# Maya tool which allows users to easily and quickly place objects in/around another object
# with a set radius and many other customizable parameters.

# Instructions: to run, navigate to execute_tool.py and run the file

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *
from functools import partial
import maya.cmds as cmds
from maya import OpenMayaUI
from pathlib import Path
import math
from shiboken2 import wrapInstance
from random import randrange
import random

# keep track of transform settings created by user


class Transform():
    def __init__(self):
        self.snapee = None
        self.surface = None
        self.orientation = 0
        self.rotate = False

# show gui window


def showWindow():
    # get this files location so we can find the .ui file in the /ui/ folder alongside it
    UI_FILE = str(Path(__file__).parent.resolve() / "gui.ui")
    loader = QUiLoader()
    file = QFile(UI_FILE)
    file.open(QFile.ReadOnly)

    # Get Maya main window to parent gui window to it
    mayaMainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
    ui = loader.load(file, parentWidget=mayaMainWindow)
    file.close()

    ui.setParent(mayaMainWindow)
    ui.setWindowFlags(Qt.Window)
    ui.setWindowTitle('Snap to Surface Tool')
    ui.setObjectName('Snap_To_Surface')
    ui.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

    t = Transform()  # transform attribute

    # function for surface object button

    def select_surface_plane():
        # get selected object(s)
        selected = cmds.ls(sl=True, long=True) or []
        if not(len(selected) == 1):
            print("Please set surface to be exactly 1 selected plane.")
        else:
            print('objectType selected[0]')
        
        isPlane = False
        #check if the surface is a plane
        for node in cmds.listHistory(selected[0]):
            if cmds.nodeType(node) == "polyDisc" or cmds.nodeType(node) == "nurbsPlane":
                print(cmds.nodeType(node))
                isPlane = True
                t.surface=selected[0]  # transform of the selected object
                break
        
        if isPlane:
            # Change location of locator to be at center object's pivot position
            x=cmds.getAttr(t.surface + ".translateX")
            y=cmds.getAttr(t.surface + ".translateY")
            z=cmds.getAttr(t.surface + ".translateZ")
            # change ui text
            ui.center_objs.setText(t.surface[1:])
        else:ui.warnings.setText(
                "<font color='red'>Warning:Please select a plane.</font>")

        

    # function for the the selecting objects to snap button
    def select_snapping_objects():
        # get selected object(s)
        selected=cmds.ls(sl=True, long=True) or []
        list_to_snap=[]
        for item in cmds.ls(selected):
            # chack the object to snap is not part of objects to snap
            if not(item == t.surface):
                list_to_snap.append(item)
        t.snapee=list_to_snap
        list_str=""
        for item in list_to_snap:
            list_str += str(item)
            if(list_to_snap.index(item) < (len(list_to_snap) - 1)):
                list_str += ", "
        # show current selected objects as a list of text on gui
        ui.outer_objs.setText(list_str)



    # snap to x side of object
    def set_X(x1):
        isChecked=ui.x_radio.isChecked()
        print(isChecked)
        if isChecked:
            t.orientation = 0
            print("x")

    # snap to y side of object
    def set_Y(y1):
        isChecked=ui.y_radio.isChecked()
        if isChecked:
            t.orientation = 1
            print("Y")

    # snap to y side of object
    def set_Z(z1):
        isChecked=ui.z_radio.isChecked()
        if isChecked:
            t.orientation = 2
            print("Z")

    # snap to y side of object
    def set_rotate_selected(r):
        isChecked = ui.rotate_checkbox.checkState()
        if isChecked:
            t.rotate = True
        else:
            t.rotate = False
        print(t.rotate)



    def snapToAlign(vertex, object):
        # cmds.select(vertex)
        x = vertex[0]
        y = vertex[1]
        z = vertex[2]

        print(x, y, z)
        cmds.select(object)

        if t.orientation is 2:
            cmds.move(z, z=True)
        elif t.orientation is 1:
            cmds.move(y, y=True)
        else:
            cmds.move(x, x=True)

    # apply button clicked
    def apply():
        # User error handling
        if t.surface == None:
            ui.warnings.setText(
                "<font color='red'>Warning: Please select a plane.</font>")
            return
        elif t.snapee == None:
            ui.warnings.setText(
                "<font color='red'>Warning: Please set at least 1 object to move.</font>")
            return        
        elif t.orientation == None:
            ui.warnings.setText(
                "<font color='red'>Warning: Please set orientation.</font>")
            return

        else:  # all proper fields have been set
            ui.warnings.setText("")
            pos = cmds.objectCenter(t.surface) 
            rotX = cmds.getAttr(t.surface + ".rx")
            rotY = cmds.getAttr(t.surface + ".ry")
            rotZ = cmds.getAttr(t.surface + ".rz")

            for obj in t.snapee:           

                snapToAlign(pos, obj)

                if t.rotate:
                    cmds.rotate(rotX, rotY, rotY, obj)

        
         # apply button clicked
    def applyAndClose():
        apply()
        close()
                





# Close dialog
    def close():
        ui.done(0)

    # connect buttons to functions
    ui.center_button.clicked.connect(partial(select_surface_plane))
    ui.outer_button.clicked.connect(partial(select_snapping_objects))
    ui.x_radio.toggled.connect(partial(set_X))
    ui.y_radio.toggled.connect(partial(set_Y))
    ui.z_radio.toggled.connect(partial(set_Z))
    ui.rotate_checkbox.stateChanged.connect(partial(set_rotate_selected))
    # ui.applyAndClose_button.clicked.connect(partial(applyAndClose))
    ui.apply_button.clicked.connect(partial(apply))
    ui.close_button.clicked.connect(partial(close))


    # show the QT ui
    ui.show()
    return ui

if __name__ == "__main__":
    window=showWindow()
