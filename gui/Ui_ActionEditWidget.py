# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_ActionEditWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ActionEditWidget(object):
    def setupUi(self, ActionEditWidget):
        ActionEditWidget.setObjectName("ActionEditWidget")
        ActionEditWidget.resize(475, 487)
        self.verticalLayout = QtWidgets.QVBoxLayout(ActionEditWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(ActionEditWidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.name_lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.horizontalLayout.addWidget(self.name_lineEdit)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(ActionEditWidget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.successor_comboBox = QtWidgets.QComboBox(self.widget_3)
        self.successor_comboBox.setObjectName("successor_comboBox")
        self.horizontalLayout_2.addWidget(self.successor_comboBox)
        self.verticalLayout.addWidget(self.widget_3)
        self.groupBox = QtWidgets.QGroupBox(ActionEditWidget)
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_4 = QtWidgets.QWidget(self.groupBox)
        self.widget_4.setMaximumSize(QtCore.QSize(250, 16777215))
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.widget_4)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 9, 0, 9)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.area_condition = QtWidgets.QLineEdit(self.widget)
        self.area_condition.setObjectName("area_condition")
        self.horizontalLayout_4.addWidget(self.area_condition)
        self.verticalLayout_2.addWidget(self.widget)
        self.screenshot_button = QtWidgets.QPushButton(self.widget_4)
        self.screenshot_button.setObjectName("screenshot_button")
        self.verticalLayout_2.addWidget(self.screenshot_button)
        self.horizontalLayout_3.addWidget(self.widget_4)
        self.preview_label = QtWidgets.QLabel(self.groupBox)
        self.preview_label.setFrameShape(QtWidgets.QFrame.Box)
        self.preview_label.setScaledContents(False)
        self.preview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_label.setObjectName("preview_label")
        self.horizontalLayout_3.addWidget(self.preview_label)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.button_group = QtWidgets.QDialogButtonBox(ActionEditWidget)
        self.button_group.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.button_group.setObjectName("button_group")
        self.verticalLayout.addWidget(self.button_group)

        self.retranslateUi(ActionEditWidget)
        QtCore.QMetaObject.connectSlotsByName(ActionEditWidget)

    def retranslateUi(self, ActionEditWidget):
        _translate = QtCore.QCoreApplication.translate
        ActionEditWidget.setWindowTitle(_translate("ActionEditWidget", "Form"))
        self.label.setText(_translate("ActionEditWidget", "Name:"))
        self.label_2.setText(_translate("ActionEditWidget", "Successor: "))
        self.groupBox.setTitle(_translate("ActionEditWidget", "Screenshot for the click area"))
        self.label_3.setText(_translate("ActionEditWidget", "Name:"))
        self.area_condition.setPlaceholderText(_translate("ActionEditWidget", "Optional"))
        self.screenshot_button.setText(_translate("ActionEditWidget", "Take Screenshot"))
        self.preview_label.setText(_translate("ActionEditWidget", "No Screenshot"))
