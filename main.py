from fastapi import FastAPI, Depends, HTTPException
from auth.authValidarToken import verify_auth_token
from preprosesamiento.funcionesValidacion import validacion



app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Api Funcionado!!"}

@app.post("/auth")
def authentication(authorized: bool = Depends(verify_auth_token)):
    if authorized == True:
        raise HTTPException(status_code=200, detail="Authorized")
    
@app.post("/validarPDF")
def validarPDF(pdfBase64, token):

    if verify_auth_token(token) == True:
        #path, state = 
        #print(path, state)
        return validacion(pdfBase64)