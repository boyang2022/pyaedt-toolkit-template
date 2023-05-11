# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'toolkit.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QLocale
from PySide6.QtCore import QMetaObject
from PySide6.QtCore import QObject
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import QSize
from PySide6.QtCore import QTime
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor
from PySide6.QtGui import QConicalGradient
from PySide6.QtGui import QCursor
from PySide6.QtGui import QFont
from PySide6.QtGui import QFontDatabase
from PySide6.QtGui import QGradient
from PySide6.QtGui import QIcon
from PySide6.QtGui import QImage
from PySide6.QtGui import QKeySequence
from PySide6.QtGui import QLinearGradient
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPalette
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QRadialGradient
from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QMenuBar
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtWidgets import QProgressBar
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QSpacerItem
from PySide6.QtWidgets import QSplitter
from PySide6.QtWidgets import QStatusBar
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1047, 1130)
        self.action_export_model = QAction(MainWindow)
        self.action_export_model.setObjectName("action_export_model")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_menu = QWidget(self.centralwidget)
        self.main_menu.setObjectName("main_menu")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.main_menu.sizePolicy().hasHeightForWidth())
        self.main_menu.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.main_menu)
        self.gridLayout.setObjectName("gridLayout")
        self.connect_aedtapp = QPushButton(self.main_menu)
        self.connect_aedtapp.setObjectName("connect_aedtapp")
        self.connect_aedtapp.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.connect_aedtapp, 3, 0, 1, 1)

        self.release_button = QPushButton(self.main_menu)
        self.release_button.setObjectName("release_button")
        self.release_button.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.release_button, 3, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 1, 1, 1)

        self.release_and_exit_button = QPushButton(self.main_menu)
        self.release_and_exit_button.setObjectName("release_and_exit_button")
        self.release_and_exit_button.setMinimumSize(QSize(0, 40))

        self.gridLayout.addWidget(self.release_and_exit_button, 3, 3, 1, 1)

        self.design_tab = QTabWidget(self.main_menu)
        self.design_tab.setObjectName("design_tab")
        sizePolicy1.setHeightForWidth(self.design_tab.sizePolicy().hasHeightForWidth())
        self.design_tab.setSizePolicy(sizePolicy1)
        self.design_tab.setTabShape(QTabWidget.Triangular)
        self.settings = QWidget()
        self.settings.setObjectName("settings")
        self.horizontalLayout_25 = QHBoxLayout(self.settings)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")

        self.verticalLayout_4.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")

        self.verticalLayout_4.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_13 = QLabel(self.settings)
        self.label_13.setObjectName("label_13")

        self.horizontalLayout_24.addWidget(self.label_13)

        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_30)

        self.numcores = QLineEdit(self.settings)
        self.numcores.setObjectName("numcores")

        self.horizontalLayout_24.addWidget(self.numcores)

        self.verticalLayout_4.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_4 = QLabel(self.settings)
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_26.addWidget(self.label_4)

        self.non_graphical_combo = QComboBox(self.settings)
        self.non_graphical_combo.addItem("")
        self.non_graphical_combo.addItem("")
        self.non_graphical_combo.setObjectName("non_graphical_combo")

        self.horizontalLayout_26.addWidget(self.non_graphical_combo)

        self.verticalLayout_4.addLayout(self.horizontalLayout_26)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self.settings)
        self.label.setObjectName("label")

        self.horizontalLayout.addWidget(self.label)

        self.aedt_version_combo = QComboBox(self.settings)
        self.aedt_version_combo.setObjectName("aedt_version_combo")

        self.horizontalLayout.addWidget(self.aedt_version_combo)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QLabel(self.settings)
        self.label_5.setObjectName("label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.process_id_combo = QComboBox(self.settings)
        self.process_id_combo.addItem("")
        self.process_id_combo.setObjectName("process_id_combo")

        self.horizontalLayout_3.addWidget(self.process_id_combo)

        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QLabel(self.settings)
        self.label_6.setObjectName("label_6")

        self.horizontalLayout_4.addWidget(self.label_6)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.project_name = QLineEdit(self.settings)
        self.project_name.setObjectName("project_name")

        self.horizontalLayout_4.addWidget(self.project_name)

        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.browse_project = QPushButton(self.settings)
        self.browse_project.setObjectName("browse_project")

        self.horizontalLayout_5.addWidget(self.browse_project)

        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_8)

        self.horizontalLayout_25.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_29 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_29)

        self.design_tab.addTab(self.settings, "")
        self.design = QWidget()
        self.design.setObjectName("design")
        self.verticalLayout_2 = QVBoxLayout(self.design)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.design_settings = QFrame(self.design)
        self.design_settings.setObjectName("design_settings")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.design_settings.sizePolicy().hasHeightForWidth())
        self.design_settings.setSizePolicy(sizePolicy2)
        self.design_settings.setFrameShape(QFrame.StyledPanel)
        self.design_settings.setFrameShadow(QFrame.Raised)
        self.design_settings.setLineWidth(12)
        self.layout_settings = QGridLayout(self.design_settings)
        self.layout_settings.setObjectName("layout_settings")
        self.geometry_selection = QHBoxLayout()
        self.geometry_selection.setObjectName("geometry_selection")
        self.label_2 = QLabel(self.design_settings)
        self.label_2.setObjectName("label_2")
        font = QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)

        self.geometry_selection.addWidget(self.label_2)

        self.geometry_combo = QComboBox(self.design_settings)
        self.geometry_combo.addItem("")
        self.geometry_combo.addItem("")
        self.geometry_combo.setObjectName("geometry_combo")
        self.geometry_combo.setFont(font)

        self.geometry_selection.addWidget(self.geometry_combo)

        self.layout_settings.addLayout(self.geometry_selection, 4, 0, 1, 1)

        self.label_16 = QLabel(self.design_settings)
        self.label_16.setObjectName("label_16")
        font1 = QFont()
        font1.setPointSize(14)
        self.label_16.setFont(font1)
        self.label_16.setAlignment(Qt.AlignCenter)

        self.layout_settings.addWidget(self.label_16, 0, 0, 1, 1)

        self.create_geometry = QHBoxLayout()
        self.create_geometry.setObjectName("create_geometry")
        self.create_geometry_buttom = QPushButton(self.design_settings)
        self.create_geometry_buttom.setObjectName("create_geometry_buttom")
        self.create_geometry_buttom.setMinimumSize(QSize(0, 50))
        self.create_geometry_buttom.setFont(font)

        self.create_geometry.addWidget(self.create_geometry_buttom)

        self.layout_settings.addLayout(self.create_geometry, 6, 0, 1, 1)

        self.label_17 = QLabel(self.design_settings)
        self.label_17.setObjectName("label_17")
        self.label_17.setFont(font1)
        self.label_17.setAlignment(Qt.AlignCenter)

        self.layout_settings.addWidget(self.label_17, 3, 0, 1, 1)

        self.dimension_multiplier = QGridLayout()
        self.dimension_multiplier.setObjectName("dimension_multiplier")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QLabel(self.design_settings)
        self.label_7.setObjectName("label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_7)

        self.multiplier = QLineEdit(self.design_settings)
        self.multiplier.setObjectName("multiplier")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.multiplier.sizePolicy().hasHeightForWidth())
        self.multiplier.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.multiplier)

        self.dimension_multiplier.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.layout_settings.addLayout(self.dimension_multiplier, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout_settings.addItem(self.verticalSpacer, 5, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout_settings.addItem(self.verticalSpacer_4, 2, 0, 1, 1)

        self.horizontalLayout_20.addWidget(self.design_settings)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_27)

        self.splitter_2 = QSplitter(self.design)
        self.splitter_2.setObjectName("splitter_2")
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(Qt.Vertical)
        self.picture = QLabel(self.splitter_2)
        self.picture.setObjectName("picture")
        self.splitter_2.addWidget(self.picture)

        self.horizontalLayout_20.addWidget(self.splitter_2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_20)

        self.design_tab.addTab(self.design, "")

        self.gridLayout.addWidget(self.design_tab, 0, 0, 1, 5)

        self.verticalLayout.addWidget(self.main_menu)

        self.log_text = QPlainTextEdit(self.centralwidget)
        self.log_text.setObjectName("log_text")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.log_text.sizePolicy().hasHeightForWidth())
        self.log_text.setSizePolicy(sizePolicy4)

        self.verticalLayout.addWidget(self.log_text)

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setValue(0)

        self.verticalLayout.addWidget(self.progress_bar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.top_menu_bar = QMenuBar(MainWindow)
        self.top_menu_bar.setObjectName("top_menu_bar")
        self.top_menu_bar.setGeometry(QRect(0, 0, 1047, 28))
        self.top_menu_bar.setFont(font)
        self.top_menu = QMenu(self.top_menu_bar)
        self.top_menu.setObjectName("top_menu")
        self.top_menu.setFont(font)
        MainWindow.setMenuBar(self.top_menu_bar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.top_menu_bar.addAction(self.top_menu.menuAction())
        self.top_menu.addAction(self.action_export_model)

        self.retranslateUi(MainWindow)

        self.design_tab.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.action_export_model.setText(
            QCoreApplication.translate("MainWindow", "Export 3D Plot", None)
        )
        self.connect_aedtapp.setText(
            QCoreApplication.translate("MainWindow", "  Launch AEDT  ", None)
        )
        self.release_button.setText(
            QCoreApplication.translate("MainWindow", " Close Toolkit ", None)
        )
        self.release_and_exit_button.setText(
            QCoreApplication.translate("MainWindow", " Close Desktop and Toolkit ", None)
        )
        self.label_13.setText(QCoreApplication.translate("MainWindow", "Number of Cores", None))
        self.numcores.setText(QCoreApplication.translate("MainWindow", "4", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", "Non Graphical", None))
        self.non_graphical_combo.setItemText(
            0, QCoreApplication.translate("MainWindow", "False", None)
        )
        self.non_graphical_combo.setItemText(
            1, QCoreApplication.translate("MainWindow", "True", None)
        )

        self.label.setText(QCoreApplication.translate("MainWindow", "AEDT Version", None))
        self.label_5.setText(
            QCoreApplication.translate("MainWindow", "Available AEDT Sessions", None)
        )
        self.process_id_combo.setItemText(
            0, QCoreApplication.translate("MainWindow", "Create New Session", None)
        )

        self.label_6.setText(QCoreApplication.translate("MainWindow", "Project Name", None))
        self.browse_project.setText(
            QCoreApplication.translate("MainWindow", "Select aedt project", None)
        )
        self.design_tab.setTabText(
            self.design_tab.indexOf(self.settings),
            QCoreApplication.translate("MainWindow", " Settings ", None),
        )
        self.label_2.setText(QCoreApplication.translate("MainWindow", "Select", None))
        self.geometry_combo.setItemText(0, QCoreApplication.translate("MainWindow", "Box", None))
        self.geometry_combo.setItemText(1, QCoreApplication.translate("MainWindow", "Sphere", None))

        self.label_16.setText(
            QCoreApplication.translate("MainWindow", "Dimension multiplier", None)
        )
        self.create_geometry_buttom.setText(
            QCoreApplication.translate("MainWindow", "Create geometry", None)
        )
        self.label_17.setText(QCoreApplication.translate("MainWindow", "Geometry selection", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", "Value", None))
        self.multiplier.setText(QCoreApplication.translate("MainWindow", "1", None))
        self.picture.setText("")
        self.design_tab.setTabText(
            self.design_tab.indexOf(self.design),
            QCoreApplication.translate("MainWindow", " Design ", None),
        )
        self.top_menu.setTitle(QCoreApplication.translate("MainWindow", "File", None))

    # retranslateUi
