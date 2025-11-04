from fastapi import FastAPI,HTTPException
import uvicorn
from pydantic import BaseModel,EmailStr,Field

app=FastAPI()

@app.get("/add")
def add(a:int,b:int):
    return {"result":a+b}

class Model(BaseModel):
    a:int
    b:int

class CalModel(BaseModel):
    x:int
    y:int
    ops:str
class UserRegis(BaseModel):
    user_name:str
    email_id:EmailStr
    password:str=Field(...,min_length=8)

@app.post("/subtract")
def subtract(model:Model):
    return {"result":model.a-model.b}

@app.post("/calculator")
def calculator(model:CalModel):
    try:
        if model.ops=="add":
            result=model.x+model.y
        elif model.ops=="subtract":
            result=model.x-model.y
        elif model.ops=="multiply":
            result= model.x*model.y
        elif model.ops=="divide":
            if model.y==0:
                return{"error":"Division by zero not allowed"}
            else:
                result=model.x/model.y
        else:
            return {"error":"please provide valid operation"}
        return {"result":result}
    except Exception as e:
        return {"error":str(e)}

list1=[]

@app.post('/UserReg')
def UserRegistration(model:UserRegis):
    for name in list1:
        if name["user_name"] == model.user_name:
            raise HTTPException(status_code=400, detail="Username already taken")
        if name["email_id"]==model.email_id:
            raise HTTPException(status_code=401,detail="Email id already exists")
    
    if "password" in model.password.lower():
        return {"Password":"Password is too weak"}
    dic={"user_name":model.user_name,
         "email_id":model.email_id}
    list1.append(dic)
    return {"Message":"login Success","email":model.email_id}

@app.get('/users')
def GetUsers():
    return {"Users ": list1}



class User(BaseModel):
    name:str
    age:int

## Put method
user_db={
    1:{"name":"Santhosh","age":25},
    2:{"name":"nagendra","age":26},
    3:{"name":"jampa","age":25}
}

## Put will update the enter record based on id 
##patch will update partial record 
@app.put("/update/{user_id}")
def update(user_id:int,user:User):
    if user_id in user_db:
        user_db[user_id]=user.model_dump()
        print(user_db)
        return {"message":f"User updated successfully {user_db[user_id]}"}
    else:
        return {"message":"No user found"}

@app.delete("/delete/{user_id}")
def delete(user_id:int):
    if user_id in user_db:
        del user_db[user_id]
        return {"message":"User Deleted Success",
                "user_id":f"{user_id}"}
    else:
        return {"message":"User not available"}
    
# if __name__=="__main__":
#     uvicorn.run(app,port=5000)

    
