import pypyodbc
from PySide6.QtCore import QThread, Signal
from main import *


class UpdateThread2(QThread):
    dataUpdated = Signal(list)

    def run(self):
        try:
            connString = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:thekitchenproject.database.windows.net,1433;Database=thekitchenproject;Uid=wwytk2mu;Pwd=Z4me5cwh*;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
            conn = odbc.connect(connString)
            mycursor = conn.cursor()
            sql = """
                    SELECT [noOrden]
                        ,[orden]
                        ,[mesa]
                        ,[total]
                    FROM [dbo].[pedidos] 
                    WHERE [estado] = 'Listo'
                    """
            mycursor.execute(sql)
            data = mycursor.fetchall()
            print(data)

            self.dataUpdated.emit(data)
        except odbc.Error as e:
            print(e)
        finally:
            mycursor.close()
            conn.close
