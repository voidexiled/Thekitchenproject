import sys
import os
import platform
import mysql.connector
from mysql.connector.plugins import caching_sha2_password

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
# FIX Problem for High DPI and Scale above 100%
os.environ["QT_FONT_DPI"] = "96"

# SET GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None


class MainWindow(QMainWindow):
    tableTimer = QTimer()
    currentPage = "Home"
    conn = None
    mode = "School"

    def onSelectRow(self):
        if widgets.tableWidget.currentRow() >= 0:
            dlg = QDialog(self)
            dlg.setMinimumSize(QSize(350, 170))
            dlg.setWindowTitle(
                f'Orden {widgets.tableWidget.item(widgets.tableWidget.currentRow(), 0).text()} // Mesa {widgets.tableWidget.item(widgets.tableWidget.currentRow(), 2).text()}')
            dlg.setStyleSheet(u"QDialog{background-color: rgb(40, 44, 52);border: 1px solid rgb(44, 49, 58);text-color: rgb(221, 221, 221);font: 10pt \"Segoe UI\";}  \n"
                              "QPushButton{\n"

                              "verical-align: bottom; horizontal-align: center; margin-bottom: 10px; background-color: rgba(15, 15, 15, 0.9); border: 1px solid rgb(255, 121, 198); border-radius: 8px;padding: 3px 3px 3px 3px; color: rgb(255, 121, 198); font: 10pt \"Segoe UI\"\n"
                              "}\n"
                              "QPushButton:hover{\n"
                              "transition-delay:1s;\n"
                              "background-color: rgba(50, 50, 50, 0.7); border: 1px solid rgb(255, 121, 198); color: rgb(255, 121, 198)\n"
                              "}\n"
                              "QPushButton:pressed{\n"
                              "transition-delay:0.3s;\n"
                              "background-color: rgba(80, 80, 80, 0.5); border: 1px solid rgb(255, 121, 198); color: rgb(255, 121, 198)\n"
                              "}\n"
                              "QLabel{\n"
                              "text-color: white;\n"
                              "}\n"
                              )
            ordenes = widgets.tableWidget.item(
                widgets.tableWidget.currentRow(), 1).text().split("\n")
            print(ordenes)
            font = QFont()
            font.setPointSize(10)
            font.setFamily("Segoe UI")
            container = QGridLayout(dlg)
            container.setHorizontalSpacing(10)
            container.setVerticalSpacing(10)
            container.setContentsMargins(10, -1, 10, -1)
            # Align all items inside of container to the center

            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setText(widgets.tableWidget.item(
                widgets.tableWidget.currentRow(), 1).text())
            label.setStyleSheet("color: #FFFFFF")
            # put the label at 0, 0, 0, 0 in the container grid layout
            container.addWidget(label, 0, 0, alignment=Qt.AlignTop)
            # create a button with material design style with "Listo" as Text
            button = QPushButton("Listo")
            button.setMinimumSize(QSize(80, 30))
            button.setMaximumSize(QSize(80, 30))
            button.setFont(font)
            # Align the button at bottom of the label

            # button.setStyleSheet()
            button.clicked.connect(lambda: self.switchOrderState(dlg, button))

            container.addWidget(button, 2, 0, alignment=Qt.AlignCenter)
            dlg.exec_()
            print(widgets.tableWidget.currentRow())

    def switchOrderState(self, parent, btn):

        if widgets.tableWidget.currentRow() >= 0:
            self.conn = self.dbConnect()
            mycursor = self.conn.cursor()
            mycursor.execute(
                f"UPDATE pedidos SET estado = 'Listo' WHERE noOrden = {widgets.tableWidget.item(widgets.tableWidget.currentRow(), 0).text()}")
            self.conn.commit()
            self.conn.close()
            self.tableTimer.stop()
            self.fillTable(None)
            parent.close()
        if widgets.tableWidget.currentRow() < 0:
            dlg = QDialog(parent)
            dlg.setMinimumSize(QSize(250, 140))
            dlg.setWindowTitle("Error")
            font = QFont()
            font.setPointSize(10)
            font.setFamily("Segoe UI")
            label = QLabel(dlg)
            label.setFont(font)
            label.setText("No hay un pedido seleccionado.")
            label.move(50, 50)
            label.setAlignment(Qt.AlignCenter)

    def dbConnect(self):
        try:
            if self.mode == "Home":
                self.conn = mysql.connector.connect(
                    host='localhost', password='EURO20partners.', user='root', database="thekitchenproject")
                mysql.connector.plugins.caching_sha2_password.MySQLCachingSHA2PasswordAuthPlugin(
                    auth_data='', username='root', password='EURO20partners.', database='thekitchenproject')
            if self.mode == "School":
                self.conn = mysql.connector.connect(
                    host='localhost', password='Z4me5cwh*', user='root', database="thekitchenproject")
                mysql.connector.plugins.caching_sha2_password.MySQLCachingSHA2PasswordAuthPlugin(
                    auth_data='', username='root', password='Z4me5cwh*', database='thekitchenproject')
            if self.conn.is_connected():

                mycursor = self.conn.cursor()
            else:
                # widgets.plainTextEdit.setText(
                # str())
                print("Failed to connect")
            return self.conn
        except Exception as ex:
            print("////////")
            print(ex.args[0])
            print("////////")
            widgets.plainTextEdit.setPlainText(str(ex.args))

    def rememberSelected(self, data):
        sel = widgets.tableWidget.currentRow()
        self.selected = sel
        self.fillTable(data)

    def fillTable(self, data):
        print(self.currentPage)
        if (self.currentPage == "Cocina"):
            self.conn = self.dbConnect()
            mycursor = self.conn.cursor()
            mycursor.execute(
                "SELECT noOrden, orden, mesa, fecha, hora FROM pedidos where estado = 'Preparando'")
            data = mycursor.fetchall()
            print(data)
            columns = ["N° Orden", "Orden", "Mesa", "Fecha", "Hora"]
            widgets.tableWidget.setRowCount(1)
            for row in data:
                rowcount = widgets.tableWidget.rowCount()
                widgets.tableWidget.insertRow(rowcount)
                for col in columns:
                    currCol = columns.index(col)
                    item = QTableWidgetItem()
                    widgets.tableWidget.setItem(
                        data.index(row)+1, currCol, item)
                    item.setText(str(row[currCol]))

            if (widgets.tableWidget.rowCount() < 16):
                widgets.tableWidget.setRowCount(16)
            widgets.tableWidget.selectRow(self.selected)
            self.conn.close()
            if self.tableTimer.isActive():
                self.tableTimer.stop()
            if not self.tableTimer.isActive():
                self.tableTimer = QTimer()
                self.tableTimer.setInterval(3000)
                self.tableTimer.timeout.connect(
                    lambda: self.rememberSelected(data))
                self.tableTimer.start()

    def __init__(self):

        QMainWindow.__init__(self)
        self.selected = 0
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR |
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "The Kitchen Project"
        description = "The Kitchen Project"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(
            lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        widgets.tableWidget.doubleClicked.connect(self.onSelectRow)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(
            UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # BUTTONS CLICK

    # ///////////////////////////////////////////////////////////////

    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            self.currentPage = "Home"
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        # widgets.tableWidget.clicked.connect(lambda: self.rememberselected())

        if btnName == "btn_widgets":
            self.currentPage = "Cocina"
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            data = [
                ["1", "Orden1", "Mesa1", "04/03/2023", "00:08"],
                ["2", "Orden2", "Mesa2", "04/03/2023", "00:08"],
                ["3", "Orden3", "Mesa3", "04/03/2023", "00:08"],
                ["4", "Orden4", "Mesa4", "04/03/2023", "00:08"],
            ]
            columns = ["N° Orden", "Orden", "Mesa", "Fecha", "Hora"]
            font = QFont()
            font.setFamily(u"Segoe UI")
            font.setPointSize(12)
            font.setBold(True)
            font.setItalic(False)
            widgets.tableWidget.setRowCount(1)
            widgets.tableWidget.item(0, 0).setFont(font)
            widgets.tableWidget.item(0, 1).setFont(font)
            widgets.tableWidget.item(0, 2).setFont(font)
            widgets.tableWidget.item(0, 3).setFont(font)
            widgets.tableWidget.item(0, 4).setFont(font)
            # FILL TABLE DATA

            # ROWS
            for row in data:
                rowcount = widgets.tableWidget.rowCount()
                widgets.tableWidget.insertRow(rowcount)
                for col in columns:
                    currCol = columns.index(col)
                    item = QTableWidgetItem()
                    widgets.tableWidget.setItem(
                        data.index(row)+1, currCol, item)
                    item.setText(row[currCol])
            if not self.tableTimer.isActive():
                self.fillTable(data)

            if (widgets.tableWidget.rowCount() < 16):
                widgets.tableWidget.setRowCount(16)

        # SHOW NEW PAGE
        if btnName == "btn_new":
            self.currentPage = "Historial"
            widgets.stackedWidget.setCurrentWidget(
                widgets.new_page)  # SET PAGE
            # RESET ANOTHERS BUTTONS SELECTED
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(
                btn.styleSheet()))  # SELECT MENU

        if btnName == "btn_save":
            self.currentPage = "Save"
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////

    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    # DOUBLE CLICK PRINTS WIDGET NAME
    def mouseDoubleClickEvent(self, event):
        widget = self.childAt(event.pos())
        if widget is not None and widget.objectName():
            print('dblclick:', widget.objectName())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
