import sys
import os
import platform

import pypyodbc as odbc
from modules.tableThread import UpdateThread
from modules.table2Thread import UpdateThread2

import time
from datetime import datetime
from decimal import Decimal

from modules import *
from widgets import *

# FIX Problem for High DPI and Scale above 100%
os.environ["QT_FONT_DPI"] = "96"

widgets = None


class MainWindow(QMainWindow):
    currentPage = "Home"
    conn = None
    mode = "School"
    pedidoString = ""
    numPlato = 1
    pedidos = []
    pedidosShowTextEdit = None
    date_time_str = None
    total = 0.0

    def closeQDialog(self):
        os.system(cmd)
        QtCore.QCoreApplication.instance().quit()

    def onSelectRow(self, table):
        if not table.currentRow() > 0:
            return

        dlg = QDialog(self)
        dlg.setMinimumSize(QSize(350, 170))
        dlg.setWindowTitle(
            f"Orden {table.item(table.currentRow(), 0).text()} // Mesa {table.item(table.currentRow(), 2).text()}"
        )
        dlg.setStyleSheet(
            'QDialog{background-color: rgb(40, 44, 52);border: 1px solid rgb(44, 49, 58);color: rgb(221, 221, 221);font: 10pt "Segoe UI";}  \n'
            "QPushButton {\n"
            "	border: 2px solid rgb(52, 59, 72);\n"
            "	border-radius: 5px;	\n"
            "	background-color: rgb(52, 59, 72);\n"
            "   color: rgb(255, 255, 255);\n"
            "   padding: 5px;\n"
            "   text-align: center;\n"
            "   font: 12pt 'Segoe UI';\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(57, 65, 80);\n"
            "	border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(35, 40, 49);\n"
            "	border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QLabel{\n"
            "color: white;\n"
            "}\n"
        )
        ordenes = table.item(table.currentRow(), 1).text().split("\n")
        font = QFont()
        font.setPointSize(10)
        font.setFamily("Segoe UI")
        container = QGridLayout(dlg)
        container.setHorizontalSpacing(10)
        container.setVerticalSpacing(10)
        container.setContentsMargins(10, -1, 10, -1)
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setText(table.item(table.currentRow(), 1).text())
        label.setStyleSheet("color: #FFFFFF")
        # put the label at 0, 0, 0, 0 in the container grid layout
        container.addWidget(label, 0, 0, alignment=Qt.AlignTop)
        if self.currentPage == "Cocina":
            # Align all items inside of container to the center
            # create a button with material design style with "Listo" as Text
            button = QPushButton("Listo")
            button.setMinimumSize(QSize(80, 30))
            button.setMaximumSize(QSize(80, 30))
            button.setFont(font)
            button.clicked.connect(lambda: self.switchOrderState(dlg, table, "Listo"))

            container.addWidget(button, 2, 0, alignment=Qt.AlignCenter)
            dlg.exec()
        elif self.currentPage == "Pedidos":
            button = QPushButton("Pagado")
            button.setMinimumSize(QSize(80, 30))
            button.setMaximumSize(QSize(80, 30))
            button.setFont(font)
            button.clicked.connect(lambda: self.switchOrderState(dlg, table, "Pagado"))
            container.addWidget(button, 2, 0, alignment=Qt.AlignCenter)
            dlg.exec()

    def switchOrderState(self, parent, table, state):
        if table.currentRow() >= 0:
            self.conn = self.dbConnect()
            mycursor = self.conn.cursor()
            mycursor.execute(
                f"UPDATE pedidos SET estado = '{state}' WHERE noOrden = {table.item(table.currentRow(), 0).text()}"
            )
            self.conn.commit()
            self.conn.close()
        if table.currentRow() < 0:
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
        parent.close()

    def dbConnect(self):
        try:
            connString = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:thekitchenproject.database.windows.net,1433;Database=thekitchenproject;Uid=wwytk2mu;Pwd=Z4me5cwh*;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
            self.conn = odbc.connect(connString)

            if self.is_connection_active(self.conn):
                mycursor = self.conn.cursor()
            else:
                # widgets.plainTextEdit.setText(
                # str())
                print("Failed to connect")
                return
            return self.conn
        except odbc.Error as ex:
            print("////////")
            print(ex)
            widgets.creditsLabel.setText(err.msg)
            print("////////")

    def is_connection_active(self, connection):
        try:
            # Realiza una operación de prueba en la base de datos
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            return True
        except pyodbc.Error:
            return False

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
        widgets.home.setStyleSheet(
            "background-image: url('images/images/tkpp.png'); background-position: centered; background-repeat: no-repeat;"
        )
        widgets.topLogo.setStyleSheet(
            "background-image: url('images/images/tkp2.png'); background-position: centered; background-repeat: no-repeat;"
        )

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        widgets.tableWidget2.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        widgets.tableWidget.doubleClicked.connect(
            lambda: self.onSelectRow(widgets.tableWidget)
        )
        widgets.tableWidget2.doubleClicked.connect(
            lambda: self.onSelectRow(widgets.tableWidget2)
        )

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
            UIFunctions.selectMenu(widgets.btn_home.styleSheet())
        )
        self.updateThread = UpdateThread()
        widgets.pedidoLineEdit.clicked.connect(self.openPedidoWindow)
        widgets.enviarPedidoButton.clicked.connect(
            lambda: self.enviarPedidoToDB(widgets.mesaLineEdit, self.pedidoString)
        )

    # BUTTONS CLICK

    # ///////////////////////////////////////////////////////////////

    def buttonClick(self):
        """
        Esta función maneja los clics en los botones y cambia la página actual que se muestra en función
        del botón en el que se hizo clic.
        """
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)

        # SHOW HOME PAGE
        if btnName == "btn_home":
            self.currentPage = "Home"
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        # widgets.tableWidget.clicked.connect(lambda: self.rememberselected())

        if btnName == "btn_widgets":
            try:
                if self.timer:
                    if self.timer.isActive():
                        self.timer.stop()
                if self.timer2:
                    if self.timer2.isActive():
                        self.timer2.stop()
                if self.updateThread:
                    if self.updateThread.isRunning():
                        self.updateThread.terminate()
                        self.updateThread.wait()
                if self.updateThread2:
                    if self.updateThread2.isRunning():
                        self.updateThread2.terminate()
                        self.updateThread2.wait()
            except Exception as ex:
                print(ex)
            self.currentPage = "Cocina"
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            columns = ["N° Orden", "Orden", "Mesa", "Fecha", "Hora"]

            widgets.tableWidget.setRowCount(1)

            for i in range(len(columns)):
                widgets.tableWidget.item(0, i).setFont(font)

            widgets.tableWidget.verticalHeader().setStretchLastSection(False)
            widgets.tableWidget.horizontalHeader().setStretchLastSection(False)
            # Crear el objeto QThread para realizar la actualización en segundo plano
            self.updateThread = UpdateThread()
            self.updateThread.dataUpdated.connect(self.actualizar_tabla1_en_hilo)
            self.updateThread.start()

            # Crear un QTimer para actualizar la tabla periódicamente

            self.timer = QTimer()
            self.timer.timeout.connect(self.actualizar_tabla1)
            self.timer.start(
                1200
            )  # Actualizar cada 2 segundos (ajusta el intervalo según tus necesidades)

        # SHOW NEW PAGE
        if btnName == "btn_new":
            try:
                if self.timer:
                    if self.timer.isActive():
                        self.timer.stop()
                if self.timer2:
                    if self.timer2.isActive():
                        self.timer2.stop()
                if self.updateThread:
                    if self.updateThread.isRunning():
                        self.updateThread.terminate()
                        self.updateThread.wait()
                if self.updateThread2:
                    if self.updateThread2.isRunning():
                        self.updateThread2.terminate()
                        self.updateThread2.wait()
            except Exception as ex:
                print(ex)
            self.currentPage = "Pedidos"
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)  # SET PAGE
            # RESET ANOTHERS BUTTONS SELECTED
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU
            self.pedidosShowTextEdit = widgets.pedidosStringShow

            columns = ["N° Orden", "Orden", "Mesa", "Total"]

            widgets.tableWidget2.setRowCount(1)
            widgets.tableWidget2.item(0, 0).setText("N° Orden")
            for i in range(len(columns)):
                widgets.tableWidget.item(0, i).setFont(font)

            widgets.tableWidget2.verticalHeader().setStretchLastSection(False)
            widgets.tableWidget2.horizontalHeader().setStretchLastSection(False)
            # Crear el objeto QThread para realizar la actualización en segundo plano
            self.updateThread2 = UpdateThread2()
            self.updateThread2.dataUpdated.connect(self.actualizar_tabla2_en_hilo)
            self.updateThread2.start()
            # Crear un QTimer para actualizar la tabla periódicamente

            self.timer2 = QTimer()
            self.timer2.timeout.connect(self.actualizar_tabla2)
            self.timer2.start(1200)  # Actualizar cada 2 segundos

        if btnName == "btn_save":
            self.currentPage = "Save"
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////

    def actualizar_tabla1(self):
        # Iniciar la actualización en un hilo separado
        self.updateThread.start()

    def actualizar_tabla1_en_hilo(self, data):
        # Borrar los elementos existentes en la tabla
        # widgets.tableWidget.clearContents()
        if widgets.tableWidget.rowCount() != len(data) + 1:
            widgets.tableWidget.setRowCount(len(data) + 1)
        # Obtener los datos y actualizar la tabla
        for i, row_data in enumerate(data):
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                widgets.tableWidget.setItem(i + 1, j, item)

    def actualizar_tabla2(self):
        # Iniciar la actualización en un hilo separado
        self.updateThread2.start()

    def actualizar_tabla2_en_hilo(self, data):
        # Borrar los elementos existentes en la tabla
        # widgets.tableWidget.clearContents()

        # Obtener los datos y actualizar la tabla
        if widgets.tableWidget2.rowCount() != len(data) + 1:
            widgets.tableWidget2.setRowCount(len(data) + 1)
        for i, row_data in enumerate(data):
            for j, value in enumerate(row_data):
                try:
                    item = QTableWidgetItem(str(value))
                    widgets.tableWidget2.setItem(i + 1, j, item)
                except Exception as ex:
                    print(ex)

    def enviarPedidoToDB(self, mesaLE, pedidos):
        mesa = mesaLE.text()
        # current dateTime
        now = datetime.now()
        # convert to string
        fecha = now.strftime("%d/%m/%Y")
        # %H:%M:%S
        hora = now.strftime("%H:%M:%S")
        try:
            string = f"INSERT INTO pedidos (orden, mesa, fecha, hora, estado, total) VALUES ('{pedidos}', '{mesa}', '{fecha}', '{hora}', 'Preparando', '{self.total}')"
            self.conn = self.dbConnect()
            mycursor = self.conn.cursor()
            mycursor.execute(string)
            mycursor.commit()
        except odbc.Error as err:
            print(err.msg)
        finally:
            dlg = QDialog()
            dlg.setMinimumSize(QSize(230, 80))
            dlg.setWindowTitle("Pedido enviado")
            dlg.setStyleSheet(
                'QDialog{background-color: rgb(40, 44, 52);border: 1px solid rgb(44, 49, 58);color: rgb(221, 221, 221);font: 10pt "Segoe UI";}  \n'
            )
            font = QFont()
            font.setPointSize(10)
            font.setFamily("Segoe UI")
            label = QLabel(dlg)
            label.setFont(font)
            label.setText("El pedido ha sido enviado")
            label.move(50, 50)
            label.setStyleSheet("color: rgb(221,221,221);")
            label.setAlignment(Qt.AlignCenter)
            dlg.exec()
            dlg.show()
            mycursor.close()
            self.conn.close()

    def getMenu(self):
        self.conn = self.dbConnect()
        mycursor = self.conn.cursor()
        mycursor.execute("SELECT nombreComida, precioComida FROM menu")
        data = mycursor.fetchall()

        menu = {}
        for a, b in data:
            menu.setdefault(a, []).append(str(b))

        return menu

    def actualizarTotal(self, tw, tl):
        try:
            total = float(tl.text().split("$")[1])
            for i in range(tw.rowCount()):
                if i >= self.numPlato:
                    if (
                        not type(tw.item(i, 2)) == None
                        and not type(tw.item(i, 3)) == None
                    ):
                        total += float(tw.item(i, 3).text()) * float(
                            tw.item(i, 2).text()
                        )
            tl.setText(f"Total: ${str(round(total, 2))}")
        except ValueError:
            print(ValueError)

    def agregarPedido(self, cb, le, tw, tl):
        menu = self.getMenu()
        comida = cb.currentText()
        cantidad = le.text()
        if cantidad and comida:
            try:
                cantidad = int(cantidad)

                if cantidad > 0:
                    tw.insertRow(tw.rowCount())
                    tw.setItem(self.numPlato, 0, QTableWidgetItem(str(self.numPlato)))
                    tw.setItem(self.numPlato, 1, QTableWidgetItem(comida))
                    tw.setItem(self.numPlato, 2, QTableWidgetItem(str(cantidad)))
                    tw.setItem(
                        self.numPlato, 3, QTableWidgetItem(menu[comida.lower()][0])
                    )

                    self.pedidoString += f"{comida} x{cantidad}\n"
                    self.actualizarTotal(tw, tl)

                    self.numPlato += 1
            except ValueError:
                print(ValueError)

    def openPedidoWindow(self):
        self.pedidoString = ""
        self.pedidos = []
        self.numPlato = 1

        dlg = QDialog(self)
        dlg.setMinimumSize(QSize(1000, 600))
        # dlg.setWindowTitle(
        #    f"Orden {table.item(table.currentRow(), 0).text()} // Mesa {table.item(table.currentRow(), 2).text()}"
        # )
        dlg.setWindowTitle("Food Chooser")
        dlg.setStyleSheet(
            'QDialog{background-color: rgb(40, 44, 52);border: 1px solid rgb(44, 49, 58);color: rgb(221, 221, 221);font: 10pt "Segoe UI";}  \n'
            "QPushButton {\n"
            "	border: 2px solid rgb(52, 59, 72);\n"
            "	border-radius: 5px;	\n"
            "	background-color: rgb(52, 59, 72);\n"
            "   color: rgb(255, 255, 255);\n"
            "   padding: 5px;\n"
            "   text-align: center;\n"
            "   font: 12pt 'Segoe UI';\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(57, 65, 80);\n"
            "	border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(35, 40, 49);\n"
            "	border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QLabel{\n"
            "color: white;\n"
            "}\n"
            "QLineEdit {\n"
            "	background-color: rgb(33, 37, 43);\n"
            "	border-radius: 5px;\n"
            "	border: 2px solid rgb(33, 37, 43);\n"
            "	padding-left: 10px;\n"
            "	selection-color: rgb(255, 255, 255);\n"
            "	selection-background-color: rgb(255, 121, 198);\n"
            "   color: rgb(255, 255, 255);\n"
            "}\n"
            "QLineEdit:hover {\n"
            "	border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QLineEdit:focus {\n"
            "	border: 2px solid rgb(91, 101, 124);\n"
            "}\n"
            """
            QComboBox {
                background-color: #212121;
                color: #fff;
                padding: 8px 16px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
                
                font-family: 'Segoe UI';
            }
            
            QComboBox::drop-down {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: none;
                
                subcontrol-origin: padding;
                subcontrol-position: top right;
                margin-top: 8px;
                margin-right: 5px;
            }
            
            QComboBox::down-arrow {
                border: none;
                width: 10px;
                height: 10px;
                image: url(images/icons/cil-arrow-bottom.png);  /* Ruta de la imagen de la flecha hacia abajo */
            }
            
            QComboBox::down-arrow:on {
                transform: rotate(180deg);
            }
            
            QComboBox QAbstractItemView {
                border: none;
                background-color: #212121;
                color: #fff;
            }
            """
            "QTableWidget {	\n"
            "	background-color: transparent;\n"
            "	padding: 10px;\n"
            "	border-radius: 5px;\n"
            "	gridline-color: rgb(44, 49, 58);\n"
            "	border-bottom: 1px solid rgb(44, 49, 60);\n"
            "   color: rgb(255, 255, 255);\n"
            "}\n"
            "QTableWidget::item{\n"
            "	border-color: rgb(44, 49, 60);\n"
            "	padding-left: 5px;\n"
            "	padding-right: 5px;\n"
            "	gridline-color: rgb(44, 49, 60);\n"
            "}\n"
            "QTableWidget::item:selected{\n"
            "	background-color: rgb(189, 147, 249);\n"
            "}\n"
            "QHeaderView::section{\n"
            "	background-color: rgb(33, 37, 43);\n"
            "	max-width: 30px;\n"
            "	border: 1px solid rgb(44, 49, 58);\n"
            "	border-style: none;\n"
            "    border-bottom: 1px solid rgb(44, 49, 60);\n"
            "    border-right: 1px solid rgb(44, 49, 60);\n"
            "}\n"
            "QTableWidget::horizontalHeader {	\n"
            "	background-color: rgb(33, 37, 43);\n"
            "}\n"
            "QHeaderView::section:horizontal\n"
            "{\n"
            "    border: 1px solid rgb(33, 37, 43);\n"
            "	background-co"
            "lor: rgb(33, 37, 43);\n"
            "	padding: 3px;\n"
            "	border-top-left-radius: 7px;\n"
            "    border-top-right-radius: 7px;\n"
            "}\n"
            "QHeaderView::section:vertical\n"
            "{\n"
            "    border: 1px solid rgb(44, 49, 60);\n"
            "}\n"
            "QScrollBar:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    height: 8px;\n"
            "    margin: 0px 21px 0 21px;\n"
            "	border-radius: 0px;\n"
            "}\n"
            "QScrollBar::handle:horizontal {\n"
            "    background: rgb(189, 147, 249);\n"
            "    min-width: 25px;\n"
            "	border-radius: 4px\n"
            "}\n"
            "QScrollBar::add-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "	border-top-right-radius: 4px;\n"
            "    border-bottom-right-radius: 4px;\n"
            "    subcontrol-position: right;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            ""
            "QScrollBar::sub-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "	border-top-left-radius: 4px;\n"
            "    border-bottom-left-radius: 4px;\n"
            "    subcontrol-position: left;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            "QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
            "{\n"
            "     background: none;\n"
            "}\n"
            "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
            "{\n"
            "     background: none;\n"
            "}\n"
            " QScrollBar:vertical {\n"
            "	border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    width: 8px;\n"
            "    margin: 21px 0 21px 0;\n"
            "	border-radius: 0px;\n"
            " }\n"
            " QScrollBar::handle:vertical {	\n"
            "	background: rgb(189, 147, 249);\n"
            "    min-height: 25px;\n"
            "	border-radius: 4px\n"
            " }\n"
            " QScrollBar::add-line:vertical {\n"
            "     border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "     height: 20px;\n"
            "	border-bottom-left-radius: 4px;\n"
            "    border-bottom-right-radius: 4px;\n"
            "     subcontrol-position: bottom;\n"
            "     su"
            "bcontrol-origin: margin;\n"
            " }\n"
            " QScrollBar::sub-line:vertical {\n"
            "	border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "     height: 20px;\n"
            "	border-top-left-radius: 4px;\n"
            "    border-top-right-radius: 4px;\n"
            "     subcontrol-position: top;\n"
            "     subcontrol-origin: margin;\n"
            " }\n"
            " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
            "     background: none;\n"
            " }\n"
            "\n"
            " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "     background: none;\n"
            " }\n"
        )

        font = QFont()
        font.setPointSize(10)
        font.setFamily("Segoe UI")
        container = QGridLayout(dlg)

        container.setHorizontalSpacing(0)
        container.setVerticalSpacing(25)
        # container.setRowStretch(5, 1)
        # Align all items inside of container to the center

        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setText("Comida")
        label.setStyleSheet("color: #FFFFFF")
        # put the label at 0, 0, 0, 0 in the container grid layout
        container.addWidget(label, 0, 0, 1, 1, alignment=Qt.AlignHCenter)
        # create a button with material design style with "Listo" as Text

        menu = self.getMenu()
        comidaComboBox = QComboBox()
        comidaComboBox.setPlaceholderText("Selecciona una opción")
        for key in menu:
            comidaComboBox.addItem(key.title())

        container.addWidget(comidaComboBox, 0, 1, 1, 2, alignment=Qt.AlignHCenter)

        # label
        cantidadLabel = QLabel()
        cantidadLabel.setAlignment(Qt.AlignCenter)
        cantidadLabel.setText("Cantidad")
        cantidadLabel.setStyleSheet("color: #FFFFFF")
        container.addWidget(cantidadLabel, 1, 0, 1, 1, alignment=Qt.AlignHCenter)

        cantidadLineEdit = QLineEdit()
        cantidadLineEdit.setPlaceholderText("Cantidad")
        cantidadLineEdit.setValidator(QIntValidator().setRange(1, 100))

        container.addWidget(cantidadLineEdit, 1, 1, 1, 2, alignment=Qt.AlignHCenter)

        agregarPushButton = QPushButton()
        agregarPushButton.setMinimumSize(QSize(160, 55))
        agregarPushButton.setFont(font)
        agregarPushButton.setText("Agregar")

        container.addWidget(agregarPushButton, 2, 0, 1, 3, alignment=Qt.AlignHCenter)
        total = 0.00
        totalLabel = QLabel()
        totalLabel.setAlignment(Qt.AlignCenter)
        totalLabel.setText(f"Total: ${total:.2f}")
        totalLabel.setStyleSheet("color: #FFFFFF")
        totalLabel.setFont(font)
        container.addWidget(totalLabel, 4, 0, 1, 3, alignment=Qt.AlignLeft)
        # numPlato = 1
        pedidosTable = QTableWidget()
        pedidosTable.setColumnCount(4)

        pedidosTable.setObjectName("tablePedidosWidget")
        sizePolicyPedidos = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicyPedidos.setHorizontalStretch(0)
        sizePolicyPedidos.setVerticalStretch(0)
        sizePolicyPedidos.setHeightForWidth(
            pedidosTable.sizePolicy().hasHeightForWidth()
        )
        pedidosTable.setSizePolicy(sizePolicyPedidos)
        palette = QPalette()
        brush = QBrush(QColor(221, 221, 221, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush)
        # endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush)
        # endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        brush4 = QBrush(QColor(0, 0, 0, 255))
        brush4.setStyle(Qt.NoBrush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush)
        # endif
        pedidosTable.setPalette(palette)
        pedidosTable.setFrameShape(QFrame.NoFrame)
        pedidosTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        pedidosTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        pedidosTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        pedidosTable.setSelectionMode(QAbstractItemView.SingleSelection)
        pedidosTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        pedidosTable.setShowGrid(True)
        pedidosTable.setGridStyle(Qt.SolidLine)
        pedidosTable.setSortingEnabled(False)
        pedidosTable.horizontalHeader().setVisible(False)
        pedidosTable.horizontalHeader().setCascadingSectionResizes(True)
        pedidosTable.horizontalHeader().setDefaultSectionSize(200)
        pedidosTable.horizontalHeader().setStretchLastSection(True)
        pedidosTable.verticalHeader().setVisible(False)
        pedidosTable.verticalHeader().setCascadingSectionResizes(False)
        pedidosTable.verticalHeader().setHighlightSections(False)
        pedidosTable.verticalHeader().setStretchLastSection(False)
        pedidosTable.setMinimumHeight(300)

        pedidosTable.setRowCount(1)

        columns = ["#", "Plato", "Cantidad", "Precio"]
        font2 = QFont()
        font2.setFamily("Segoe UI")
        font2.setPointSize(12)
        font2.setBold(True)
        font2.setItalic(False)
        for col in columns:
            item = QTableWidgetItem(col)
            item.setFont(font2)
            item.setBackground(QColor(0, 0, 0))
            pedidosTable.setItem(0, columns.index(col), item)
        pedidosTable.row

        container.addWidget(pedidosTable, 0, 3, 4, 4, alignment=Qt.AlignCenter)

        terminarPushButton = QPushButton()
        terminarPushButton.setMinimumSize(QSize(160, 55))
        terminarPushButton.setMaximumSize(QSize(160, 55))
        terminarPushButton.setFont(font)
        terminarPushButton.setText("Terminar")
        pedidos = []
        terminarPushButton.clicked.connect(
            lambda: self.terminarPedido(dlg, self.pedidoString, totalLabel)
        )
        container.addWidget(terminarPushButton, 4, 3, 1, 4, alignment=Qt.AlignCenter)
        invisibleInput = QLineEdit()
        invisibleInput.setVisible(False)
        invisibleInput.setMinimumWidth(300)
        container.addWidget(invisibleInput, 5, 0, 6, 1, alignment=Qt.AlignCenter)

        """
            button = QPushButton("Listo")
            button.setMinimumSize(QSize(80, 30))
            button.setMaximumSize(QSize(80, 30))
            button.setFont(font)
            button.clicked.connect(lambda: self.switchOrderState(dlg, table))

            container.addWidget(button, 2, 0, alignment=Qt.AlignCenter)
        """
        agregarPushButton.clicked.connect(
            lambda: self.agregarPedido(
                comidaComboBox, cantidadLineEdit, pedidosTable, totalLabel
            )
        )
        dlg.exec()

    def terminarPedido(self, parent, pS, tL):
        self.pedidos.append(pS)
        self.pedidos.append(float(tL.text().split("$")[1]))
        print("*** PEDIDO TERMINADO ***")
        print(self.pedidos)
        self.pedidosShowTextEdit.setPlainText(pS)
        # current dateTime
        now = datetime.now()
        # convert to string
        self.date_time_str = now.strftime("%D/%m/%Y %H:%M:%S")
        print("DateTime String:", self.date_time_str)
        self.total = float(tL.text().split("$")[1])
        parent.close()

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
            print("Mouse click: LEFT CLICK")
        if event.buttons() == Qt.RightButton:
            print("Mouse click: RIGHT CLICK")

    # DOUBLE CLICK PRINTS WIDGET NAME
    def mouseDoubleClickEvent(self, event):
        widget = self.childAt(event.pos())
        if widget is not None and widget.objectName():
            print("dblclick:", widget.objectName())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
