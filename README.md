# The kitchen project

# Requerimentos

Python 3.9 > <br>
Sql Server <br>
MySQL Workbench 8.0 > <br>

# Primeros pasos

Añade en MySQL Workbench el schema indicado en las configuraciones del proyecto. <br>
<code>
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

</code>
