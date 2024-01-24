from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    username:str
    password:str
    wallet:float
    age:Optional[int] = None
    
class UserPwd(User):
    password:str
    
    
class UserIn(User):
    id:int
    
    class Config:
        orm_mode = True
      
class UserHsh(UserIn):
    hashed_pwd:str
    
class TokenData(BaseModel):
    username:Optional[str] = None

class Token(BaseModel):
    access_token:str
    token_type:str
    
class Model(BaseModel):
    id:int
    name:str
    cost:float

class Models(BaseModel):
    models: list[Model]
    
class Prediction(BaseModel):
    id:int
    model_id:int
    data:str
    result:int
    
class Predictions(BaseModel):
    predictions: list[Prediction]
    
class InputsIn(BaseModel):
    id:int
        
    class Config:
            orm_mode = True
            
class InputsDB(BaseModel):
    N_Days: int
    Drug:int
    Age: int
    Sex: int 
    Ascites: int
    Hepatomegaly:int
    Spiders:int
    Edema:int
    Bilirubin: float
    Cholesterol: float
    Albumin: float
    Copper: float
    Alk_Phos: float
    SGOT: float
    Triglycerides: float
    Platelets: float
    Prothrombin:float
    Stage: int
    