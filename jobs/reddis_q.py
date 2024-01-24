from pydantic import BaseModel
from redis import Redis
import requests
from rq import Queue
from jobs.job import test
from celery import Celery
import time

MODEL_URL="http://127.0.0.1:8001/model"
API_URL = "http://127.0.0.1:8000/show_res"

#r_connection = Redis(host="localhost", port=6379)
celery_conection = Celery('test_q', broker='redis://localhost:6379') 
job_queue = Queue("test_q", connection = celery_conection)

#class JobData(BaseModel):
    #num:int

@celery_conection.task    
def make_queue(data):
    #Запрос на predict отправляем модели
    response = requests.post(MODEL_URL, json = data)
    if response.status_code == 200:
        res = response.json()["prediction"][0]
    else:
        res = None
    #Запрос с результатом отправляем на бэк    
    requests.post(API_URL, json = res)   
    
    return res
