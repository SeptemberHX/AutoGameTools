# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_StatusEditWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StatusEditWidget(object):
    def setupUi(self, StatusEditWidget):
        StatusEditWidget.setObjectName("StatusEditWidget")
        StatusEditWidget.resize(496, 675)
        StatusEditWidget.setMaximumSize(QtCore.QSize(500, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(StatusEditWidget)
        self.verticalLayout.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(StatusEditWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.name_lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.name_lineEdit.setMinimumSize(QtCore.QSize(250, 0))
        self.name_lineEdit.setMaximumSize(QtCore.QSize(250, 16777215))
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.horizontalLayout.addWidget(self.name_lineEdit)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.type_comboBox = QtWidgets.QComboBox(self.widget_3)
        self.type_comboBox.setMinimumSize(QtCore.QSize(250, 0))
        self.type_comboBox.setMaximumSize(QtCore.QSize(250, 16777215))
        self.type_comboBox.setObjectName("type_comboBox")
        self.horizontalLayout_2.addWidget(self.type_comboBox)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.verticalLayout_7.addWidget(self.widget)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setContentsMargins(9, 3, -1, 3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_4 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_4.setMinimumSize(QtCore.QSize(180, 0))
        self.widget_4.setMaximumSize(QtCore.QSize(180, 16777215))
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_13 = QtWidgets.QWidget(self.widget_4)
        self.widget_13.setObjectName("widget_13")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.widget_13)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_3 = QtWidgets.QLabel(self.widget_13)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_12.addWidget(self.label_3)
        self.condition_name = QtWidgets.QLineEdit(self.widget_13)
        self.condition_name.setObjectName("condition_name")
        self.horizontalLayout_12.addWidget(self.condition_name)
        self.verticalLayout_3.addWidget(self.widget_13)
        self.widget_5 = QtWidgets.QWidget(self.widget_4)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.widget_5)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.contain_comboBox = QtWidgets.QComboBox(self.widget_5)
        self.contain_comboBox.setObjectName("contain_comboBox")
        self.contain_comboBox.addItem("")
        self.contain_comboBox.addItem("")
        self.horizontalLayout_4.addWidget(self.contain_comboBox)
        self.verticalLayout_3.addWidget(self.widget_5)
        self.widget_6 = QtWidgets.QWidget(self.widget_4)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.screenshot_button = QtWidgets.QPushButton(self.widget_6)
        self.screenshot_button.setObjectName("screenshot_button")
        self.horizontalLayout_5.addWidget(self.screenshot_button)
        self.verticalLayout_3.addWidget(self.widget_6)
        self.horizontalLayout_3.addWidget(self.widget_4)
        self.preview_label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview_label.sizePolicy().hasHeightForWidth())
        self.preview_label.setSizePolicy(sizePolicy)
        self.preview_label.setMinimumSize(QtCore.QSize(250, 0))
        self.preview_label.setMaximumSize(QtCore.QSize(250, 16777215))
        self.preview_label.setFrameShape(QtWidgets.QFrame.Box)
        self.preview_label.setScaledContents(False)
        self.preview_label.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_label.setObjectName("preview_label")
        self.horizontalLayout_3.addWidget(self.preview_label)
        self.verticalLayout_6.addWidget(self.groupBox_2)
        self.optional_groupbox_1 = QtWidgets.QGroupBox(self.groupBox_4)
        self.optional_groupbox_1.setFlat(True)
        self.optional_groupbox_1.setCheckable(True)
        self.optional_groupbox_1.setChecked(False)
        self.optional_groupbox_1.setObjectName("optional_groupbox_1")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.optional_groupbox_1)
        self.horizontalLayout_6.setContentsMargins(-1, 3, -1, 3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.widget_7 = QtWidgets.QWidget(self.optional_groupbox_1)
        self.widget_7.setMinimumSize(QtCore.QSize(180, 0))
        self.widget_7.setMaximumSize(QtCore.QSize(180, 16777215))
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_4.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_14 = QtWidgets.QWidget(self.widget_7)
        self.widget_14.setObjectName("widget_14")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.widget_14)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_6 = QtWidgets.QLabel(self.widget_14)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_13.addWidget(self.label_6)
        self.condition_name_1 = QtWidgets.QLineEdit(self.widget_14)
        self.condition_name_1.setObjectName("condition_name_1")
        self.horizontalLayout_13.addWidget(self.condition_name_1)
        self.verticalLayout_4.addWidget(self.widget_14)
        self.widget_8 = QtWidgets.QWidget(self.widget_7)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.widget_8)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.contain_comboBox_1 = QtWidgets.QComboBox(self.widget_8)
        self.contain_comboBox_1.setObjectName("contain_comboBox_1")
        self.contain_comboBox_1.addItem("")
        self.contain_comboBox_1.addItem("")
        self.horizontalLayout_7.addWidget(self.contain_comboBox_1)
        self.verticalLayout_4.addWidget(self.widget_8)
        self.widget_9 = QtWidgets.QWidget(self.widget_7)
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_9)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.screenshot_button_1 = QtWidgets.QPushButton(self.widget_9)
        self.screenshot_button_1.setObjectName("screenshot_button_1")
        self.horizontalLayout_8.addWidget(self.screenshot_button_1)
        self.verticalLayout_4.addWidget(self.widget_9)
        self.horizontalLayout_6.addWidget(self.widget_7)
        self.preview_label_1 = QtWidgets.QLabel(self.optional_groupbox_1)
        self.preview_label_1.setMinimumSize(QtCore.QSize(250, 0))
        self.preview_label_1.setMaximumSize(QtCore.QSize(250, 16777215))
        self.preview_label_1.setFrameShape(QtWidgets.QFrame.Box)
        self.preview_label_1.setScaledContents(False)
        self.preview_label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_label_1.setObjectName("preview_label_1")
        self.horizontalLayout_6.addWidget(self.preview_label_1)
        self.verticalLayout_6.addWidget(self.optional_groupbox_1)
        self.optional_groupbox_2 = QtWidgets.QGroupBox(self.groupBox_4)
        self.optional_groupbox_2.setFlat(True)
        self.optional_groupbox_2.setCheckable(True)
        self.optional_groupbox_2.setChecked(False)
        self.optional_groupbox_2.setObjectName("optional_groupbox_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.optional_groupbox_2)
        self.horizontalLayout_9.setContentsMargins(-1, 3, -1, 3)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.widget_10 = QtWidgets.QWidget(self.optional_groupbox_2)
        self.widget_10.setMinimumSize(QtCore.QSize(180, 0))
        self.widget_10.setMaximumSize(QtCore.QSize(180, 16777215))
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_5.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_15 = QtWidgets.QWidget(self.widget_10)
        self.widget_15.setObjectName("widget_15")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.widget_15)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_8 = QtWidgets.QLabel(self.widget_15)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_14.addWidget(self.label_8)
        self.condition_name_2 = QtWidgets.QLineEdit(self.widget_15)
        self.condition_name_2.setText("")
        self.condition_name_2.setObjectName("condition_name_2")
        self.horizontalLayout_14.addWidget(self.condition_name_2)
        self.verticalLayout_5.addWidget(self.widget_15)
        self.widget_11 = QtWidgets.QWidget(self.widget_10)
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_7 = QtWidgets.QLabel(self.widget_11)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_10.addWidget(self.label_7)
        self.contain_comboBox_2 = QtWidgets.QComboBox(self.widget_11)
        self.contain_comboBox_2.setObjectName("contain_comboBox_2")
        self.contain_comboBox_2.addItem("")
        self.contain_comboBox_2.addItem("")
        self.horizontalLayout_10.addWidget(self.contain_comboBox_2)
        self.verticalLayout_5.addWidget(self.widget_11)
        self.widget_12 = QtWidgets.QWidget(self.widget_10)
        self.widget_12.setObjectName("widget_12")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.widget_12)
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.screenshot_button_2 = QtWidgets.QPushButton(self.widget_12)
        self.screenshot_button_2.setObjectName("screenshot_button_2")
        self.horizontalLayout_11.addWidget(self.screenshot_button_2)
        self.verticalLayout_5.addWidget(self.widget_12)
        self.horizontalLayout_9.addWidget(self.widget_10)
        self.preview_label_2 = QtWidgets.QLabel(self.optional_groupbox_2)
        self.preview_label_2.setMinimumSize(QtCore.QSize(250, 0))
        self.preview_label_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.preview_label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.preview_label_2.setScaledContents(False)
        self.preview_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_label_2.setObjectName("preview_label_2")
        self.horizontalLayout_9.addWidget(self.preview_label_2)
        self.verticalLayout_6.addWidget(self.optional_groupbox_2)
        self.verticalLayout_7.addWidget(self.groupBox_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem1)
        self.button_group = QtWidgets.QDialogButtonBox(self.groupBox)
        self.button_group.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.button_group.setObjectName("button_group")
        self.verticalLayout_7.addWidget(self.button_group)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(StatusEditWidget)
        QtCore.QMetaObject.connectSlotsByName(StatusEditWidget)

    def retranslateUi(self, StatusEditWidget):
        _translate = QtCore.QCoreApplication.translate
        StatusEditWidget.setWindowTitle(_translate("StatusEditWidget", "Form"))
        self.groupBox.setTitle(_translate("StatusEditWidget", "State Editor"))
        self.label.setText(_translate("StatusEditWidget", "Name:"))
        self.label_2.setText(_translate("StatusEditWidget", "Type:"))
        self.groupBox_4.setTitle(_translate("StatusEditWidget", "Condition(s) for judging current game status"))
        self.groupBox_2.setTitle(_translate("StatusEditWidget", "Condition"))
        self.label_3.setText(_translate("StatusEditWidget", "Name:"))
        self.condition_name.setPlaceholderText(_translate("StatusEditWidget", "Optional"))
        self.label_4.setText(_translate("StatusEditWidget", "Contains:"))
        self.contain_comboBox.setItemText(0, _translate("StatusEditWidget", "Yes"))
        self.contain_comboBox.setItemText(1, _translate("StatusEditWidget", "No"))
        self.screenshot_button.setText(_translate("StatusEditWidget", "Take Screenshot"))
        self.preview_label.setText(_translate("StatusEditWidget", "No Screenshot"))
        self.optional_groupbox_1.setTitle(_translate("StatusEditWidget", "Optional Condition 1"))
        self.label_6.setText(_translate("StatusEditWidget", "Name:"))
        self.condition_name_1.setPlaceholderText(_translate("StatusEditWidget", "Optional"))
        self.label_5.setText(_translate("StatusEditWidget", "Contains:"))
        self.contain_comboBox_1.setItemText(0, _translate("StatusEditWidget", "Yes"))
        self.contain_comboBox_1.setItemText(1, _translate("StatusEditWidget", "No"))
        self.screenshot_button_1.setText(_translate("StatusEditWidget", "Take Screenshot"))
        self.preview_label_1.setText(_translate("StatusEditWidget", "No Screenshot"))
        self.optional_groupbox_2.setTitle(_translate("StatusEditWidget", "Optional Condition 2"))
        self.label_8.setText(_translate("StatusEditWidget", "Name:"))
        self.condition_name_2.setPlaceholderText(_translate("StatusEditWidget", "Optional"))
        self.label_7.setText(_translate("StatusEditWidget", "Contains:"))
        self.contain_comboBox_2.setItemText(0, _translate("StatusEditWidget", "Yes"))
        self.contain_comboBox_2.setItemText(1, _translate("StatusEditWidget", "No"))
        self.screenshot_button_2.setText(_translate("StatusEditWidget", "Take Screenshot"))
        self.preview_label_2.setText(_translate("StatusEditWidget", "No Screenshot"))
