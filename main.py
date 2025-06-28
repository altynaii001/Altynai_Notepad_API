from fastapi import FastAPI
from pydantic import BaseModel
from tasks.email_tasks import mock_email

app = FastAPI()

class EmailRequest(BaseModel):
    email:str

@app.post("/trigger-tasks")
def trigger_task(request: EmailRequest):
    mock_email.delay(request.email)
    return {"message": "Task started"}