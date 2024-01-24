from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib 
import sklearn
import numpy as np
import uvicorn

model_logic = FastAPI()

GB_NAME = 'gb.joblib'
RF_NAME = 'rf.joblib'
LR_NAME = 'lr.joblib'



LINEAR_REG = joblib.load(LR_NAME)
GRAD_BOOST = joblib.load(GB_NAME)
RANDOM_FOREST = joblib.load(RF_NAME)

MODEL_NAMES={"gb":GRAD_BOOST,"rf":RANDOM_FOREST,"lr":LINEAR_REG}

class ModelData(BaseModel):
    user_id: int
    model_name:str
    N_Days: int
    Drug: int
    Age: int
    Sex: int
    Ascites: int
    Hepatomegaly: int
    Spiders: int
    Edema: int
    Bilirubin: float
    Cholesterol: float
    Albumin: float
    Copper: float
    Alk_Phos: float
    SGOT: float
    Triglycerides: float
    Platelets: float
    Prothrombin: float
    Stage: int
    
@model_logic.post('/predict')
def predict(data: ModelData):
    try:
        zeros = [0,1,0,1,0,1,1]
        l_data = zeros + [data.N_Days,
                          data.Drug,
                          data.Age,
                          data.Sex,
                          data.Ascites,
                          data.Hepatomegaly,
                          data.Spiders,
                          data.Edema,
                          data.Bilirubin,
                          data.Cholesterol,
                          data.Albumin,
                          data.Copper,
                          data.Alk_Phos,
                          data.SGOT,
                          data.Triglycerides,
                          data.Platelets,
                          data.Prothrombin,
                          data.Stage] 
        np_data = np.array(l_data)
        clear_data = np_data.reshape(1,-1)
        pred = MODEL_NAMES[data.model_name].predict(clear_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    return {
        "prediction": pred.tolist()
        }
        
#if __name__ == '__main__':
    #uvicorn.run(model_logic, host='127.0.0.1', port=8001)