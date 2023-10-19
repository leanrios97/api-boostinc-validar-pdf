import pymssql
from conexionDB.datos_conexion import datosConexion

def dev_cursor():
    '''
    Función para realizar la conexión a la base de datos bddo.
    '''
    # Recibe las credenciales del .env para luego ser asignadas al string de conexión.
    servidor, bd, user, password = datosConexion()
    print("Paso 1.2: Se pudieron obtener los datos para la cadena de conexión")

    try:
        # Configura la cadena de conexión
        conn = pymssql.connect(server=servidor, user=user, password=password, database=bd)
        

        print("Conexión exitosa!")
        # OK! Conexión exitosa
        return conn

    except Exception as e:
        # Atrapar error
        print("Ocurrió un error al conectar a SQL Server: ", e)

