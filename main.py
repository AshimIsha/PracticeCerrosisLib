from fastapi import FastAPI
import uvicorn

from database import connection 
from routers.user_routers import user_router
from routers.predict_routers import predict_router

app = FastAPI()

app.include_router(router = user_router)
app.include_router(router = predict_router)
#connection.create_db()



#if __name__ == '__main__':
    #uvicorn.run(app, host='127.0.0.1', port=8000)