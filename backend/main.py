from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from backend.prediction_helper import predict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class InsuranceInput(BaseModel):
    age: int = Field(..., alias="Age")
    number_of_dependants: int = Field(..., alias="Number of Dependants")
    income_lakhs: float = Field(..., alias="Income in Lakhs")
    genetical_risk: int = Field(..., alias="Genetical Risk")
    insurance_plan: str = Field(..., alias="Insurance Plan")
    employment_status: str = Field(..., alias="Employment Status")
    gender: str = Field(..., alias="Gender")
    marital_status: str = Field(..., alias="Marital Status")
    bmi_category: str = Field(..., alias="BMI Category")
    smoking_status: str = Field(..., alias="Smoking Status")
    region: str = Field(..., alias="Region")
    medical_history: str = Field(..., alias="Medical History")


app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.post("/predict")
def get_prediction(data: InsuranceInput):
    input_dict = data.model_dump(by_alias=True)  

    prediction = predict(input_dict)

    return {
        "predicted_cost": prediction
    }