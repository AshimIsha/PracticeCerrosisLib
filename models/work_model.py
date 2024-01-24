import joblib 
import sklearn
import numpy as np

from schemes import user_schemes
from database import user_database
from database.connection import get_connection, commit
from jobs import reddis_q

MODEL_COST={"gb":3,"rf":2,"lr":1}

GB_NAME = 'models/gb.joblib'
RF_NAME = 'models/rf.joblib'
LR_NAME = 'models/lr.joblib'

MODEL_NAMES={"gb":GB_NAME,"rf":RF_NAME,"lr":LR_NAME}

LINEAR_REG = joblib.load(LR_NAME)
GRAD_BOOST = joblib.load(GB_NAME)
RANDOM_FOREST = joblib.load(RF_NAME)

input_data= {
        'N_Days': 3000,
        'Drug':1,
        'Age':23,
        'Sex': 1, 
        'Ascites': 1,
        'Hepatomegaly':1,
        'Spiders':1,
        'Edema':1,
        'Bilirubin 0-30 [mg/dl]': 22,
        'Cholesterol 0-400 [mg/dl]': 300,
        'Albumin 0-10 [gm/dl]': 4,
        'Copper 0-600 [ug/day]': 333,
        'Alk_Phos 100-10000 [U/liter]': 5000,
        'SGOT 0-600 [U/ml]': 500,
        'Triglycerides 0-600 [mg/dl]': 441,
        'Platelets 0-1000 [ml/1000]': 600,
        'Prothrombin  0-20 [s]':13,
        'Stage 1 2 3 4': 2
   }

#zeros = [0,1,0,1,0,1,1]
#l_data = zeros + list(input_data.values()) 
#np_data = np.array(l_data)

#clear_data = np_data.reshape(1,-1)
#clear_data = np.nan_to_num(clear_data)
#grad_pred = GRAD_BOOST.predict(clear_data)

def get_result(id, session = get_connection()):
    return session.query(user_database.Predict).filter_by(user_id=id).all()

def add_result(id, model_name, N_Days,Drug,Age,Sex, Ascites,Hepatomegaly,\
                Spiders,Edema,Bilirubin,Cholesterol,Albumin,Copper,Alk_Phos,\
                SGOT,Triglycerides,Platelets,Prothrombin,Stage,\
                result, session=get_connection()):
    new_predict = user_database.Predict(
        user_id=id,
        model_name=model_name,
        N_Days = N_Days,
        Drug = Drug,
        Age = Age,
        Sex = Sex,
        Ascites = Ascites,
        Hepatomegaly = Hepatomegaly,
        Spiders = Spiders,
        Edema = Edema,
        Bilirubin = Bilirubin,
        Cholesterol = Cholesterol,
        Albumin = Albumin,
        Copper = Copper,
        Alk_Phos = Alk_Phos,
        SGOT = SGOT,
        Triglycerides = Triglycerides,
        Platelets = Platelets,
        Prothrombin = Prothrombin,
        Stage = Stage,
        result = result )
    
    session.add(new_predict)
    commit(session)
    return new_predict

def job_predict(N_Days,Drug,Age,Sex, Ascites,Hepatomegaly,\
                Spiders,Edema,Bilirubin,Cholesterol,Albumin,Copper,Alk_Phos,\
                SGOT,Triglycerides,Platelets,Prothrombin,Stage):
    
    data_to_model = [N_Days,Drug,Age,Sex, Ascites,Hepatomegaly,\
                Spiders,Edema,Bilirubin,Cholesterol,Albumin,Copper,Alk_Phos,\
                SGOT,Triglycerides,Platelets,Prothrombin,Stage]
    
    reddis_q.make_queue(data_to_model)
    
    return
