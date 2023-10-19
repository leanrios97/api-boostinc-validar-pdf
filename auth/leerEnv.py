def cargarTokenEnv():
    # Importamos los módulos necesarios para manejar las variables de entorno y configuración.
    import os

    try:
        with open("auth/.env") as f:
            
            for line in f:
                key, value = line.strip().split("=")
                os.environ[key] = value

        SECRET_KEY = os.environ["SECRET_KEY"]
        print("Se guardo y envio el secret_key.")
        return SECRET_KEY
    
    except Exception as e:
        # Atrapar error
        print("Ocurrio un error al encontrar el archivo .env ", e)
