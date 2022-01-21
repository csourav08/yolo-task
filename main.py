from fastapi import FastAPI, Body, Request, Depends,HTTPException
# from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json

app = FastAPI()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/ping")
def home():
    return "Pong"

# Login App
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    with open("userdb.json", "r") as json_file:
        json_data = json.load(json_file)
    if json_data:
    #     check if the user name is present

        password = json_data.get(form_data.username)
        if not password:
            print("Wrong username or password.. re-enter")
            raise HTTPException(status_code=403, detail="Incorrect username or password")
    # to check if the username in the db and the password matches
    return {"access_token": form_data.username ,"token_type":"bearer" }

@app.get("/spend/history")
def spend_history(token: str = Depends(oauth_scheme)):
    print(token)
# spend history logic
#     print("SPEND HISTORY")
    with open("spendhist.json", "r") as spend_hist:
        spend_hist_data = json.load(spend_hist)
        if not spend_hist_data.get(token):
            raise HTTPException(status_code=400, detail ="Username not found")


        return {
            "username": token,
            "spend_hist": spend_hist_data[token]
        }


@app.get("/creditcard/history")
def credit_history(token: str = Depends(oauth_scheme)):
    print(token)
    print(token)
    # spend history logic
    print("SPEND HISTORY")
    with open("credithist.json", "r") as credit_hist:
        credit_hist_data = json.load(credit_hist)
        if not credit_hist_data.get(token):
            raise HTTPException(status_code=400, detail="Username not found")

        return {
            "username": token,
            "credit_hist": credit_hist_data[token]
        }

    @app.post("/transfer_money")
    def transfer_money(token: str = Depends(oauth_scheme), destination_user : str= Body(...),amount_to_transfer: float = Body(...) ):
       print(token)
       print(destination_user)
       print(amount_to_transfer)
       # userbalance_data = None

       with open("userbalance.json", "r") as userbalance_file:
           userbalance_data = json.load(userbalance_file)
           #current user balance
           curr_user_bal = userbalance_data.get(token)['curr_balance']
           print(f"current user balance is {curr_user_bal}")
           #destination user balance
           dest_user = userbalance_data.get(destination_user)
           if not dest_user:
               raise HTTPException(status_code=400, detail="Destination user is not in the DB cannot transfer money")
           dest_user_bal = dest_user['curr_balance']
           print(f"Destnation user Balance = {dest_user_bal}")
           if curr_user_bal - amount_to_transfer < 0:
               raise HTTPException(status_code=400,detail="Amount you're trying to transfer is greated than account balance")
           userbalance_data[token]['curr_balance'] -= amount_to_transfer
           print(userbalance_data)
           userbalance_data[destination_user]['curr_balance'] += amount_to_transfer
           with open ("userbalance.json", "w") as userbal_write:
               json.dump(userbalance_data, userbal_write)
               return {
                   "username": token,
                   "message": f"Money {amount_to_transfer} successfully transferred"
               }
           # getter method
           @app.get("/userbalance")
           def get_userbalance(token: str = Depends(oauth_scheme)):
               with open("userbalance.json", "r") as userfile:
                   userbalance = json.load(userfile)
                   if not userbalance.get(token):
                       raise HTTPException(status_code=400,
                                           detail="username not present in db")
                   return {
                       "username": token,
                       "current_balance": userbalance.get(token)['curr_balance']
                   }




























