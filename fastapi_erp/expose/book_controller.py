from fastapi import APIRouter
from fastapi import Depends
from fastapi_erp.cbv import cbv
from fastapi_erp.business.book_service import BookService
from fastapi_erp.model.api.book import BookSchema, Response

router = APIRouter(prefix="/book")

# Cabe mencionar que vamos a usar constantemente dos parametros 
# "request" el cual es la entrada y será acorde con el esquema "mostrar en SWAGGER"
# y "db" que es de tipo Sesion y de la cual depende de la conexión de nuestr db

# haremos uso de las funciones que creamos en el archivo de crud.py

# Creamos la ruta con la que crearemos 
@cbv(router)
class ItemController:
    
    book_service: BookService = Depends(BookService.instance)

    @router.post("")
    async def create(self, request: BookSchema):
        self.book_service.create(book=request)
        print(request)
        return Response(status="Ok",
                        code="200",
                        message="Book created successfully",result=request).dict(exclude_none=True)
        # retornamos la respuesta con el schema de response


    @router.get("/{skip}/{limit}")
    async def list(self, skip: int = 0, limit: int = 100):
        books = self.book_service.list(skip, limit)
        return Response(status="Ok", code="200", message="Success fetch all data", result= books)


    @router.patch("")
    async def update(self, request: BookSchema):
        try:
            book = self.book_service.update(book_id=request.id,
                                    title=request.title, description=request.description)
            return Response(status="Ok", code="200", message="Success update data", result= book)
        except Exception as e:
            return Response(
                status="bad",
                code="304",
                message="the updated gone wrong"
            )
        # colocamos una excepción por si ocurre un error en la escritura en la db

    @router.delete("")
    async def delete(self, request: BookSchema):
        try:
            self.book_service.remove(book_id=request.id)
            return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)
        except Exception as e:
            return Response(
                status="bad",
                code="",
                message="the deleted gone wrong"
            )