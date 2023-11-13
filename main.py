from fastapi import FastAPI, Depends, HTTPException
from auth.authValidarToken import verify_auth_token
from accionesPDF.funcionesValidacion import PDFValidator
from accionesPDF.summarization import SummarizePDF


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
        vl = PDFValidator()
        return vl.validate_pdf(pdfBase64)


@app.post("/summarizePDF")
def summarizePDF(pdfBase64, token):

    if verify_auth_token(token) == True:
        su = SummarizePDF(max_summary_length=500, min_summary_length=250)
        return su.translate_and_summarize(pdfBase64)