def verify_auth_token(token):
    from auth.leerEnv import cargarTokenEnv
    from fastapi import  HTTPException


    """Verifica el token de autenticación."""

    secret_key = cargarTokenEnv()

    # Verificar el token de autenticación
    if token == secret_key:
        return True
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")