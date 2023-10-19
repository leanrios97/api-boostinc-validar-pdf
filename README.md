# api-boostinc-validar-pdf
Repositorio de la api para validar documentos pdf

en el archivo /auth/.env tenemos el token de validacion para poder usar la api. 

para poder ejecutar la api, instalar anaconda. en la seccion de environments importar el archivo requerement para instalar todas las dependencias. 
al finalizar validar que este el entorno levanta para recien acceder a ejecutar el codigo. 


# Correr api

1. por consola ejecutar el siguiente comando: 
	
	uvicorn main:app --reload
	
en el archivo main estan los endpoint 

si accedes a la url donde corre la api y le agregas /docs tener un tipo swagger para iteractuar con los endpoint. 

Saludos !