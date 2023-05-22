import mysql.connector
import pypyodbc as odbc


def conectar():
    connString = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:thekitchenproject.database.windows.net,1433;Database=thekitchenproject;Uid=wwytk2mu;Pwd=Z4me5cwh*;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    conexion1 = odbc.connect(connString)
    sql = """
                    SELECT [noOrden]
                        ,[orden]
                        ,[mesa]
                        ,[fecha]
                        ,[hora]
                    FROM [dbo].[pedidos] 
                    WHERE [estado] = 'Preparando'
                    """
    cursor = conexion1.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        print(row)


conectar()
