from http.client import HTTPException
from urllib.request import Request

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from h11 import Response
from matplotlib import pyplot as plt
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from pydantic.fields import ModelField
from typing import Type, io
import inspect
from fastapi import Form
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import matplotlib.pyplot as plt
import io
import json


# def as_form(cls: Type[BaseModel]):
#     new_parameters = []

#     for field_name, model_field in cls.__fields__.items():
#         model_field: ModelField  # type: ignore

#         new_parameters.append(
#              inspect.Parameter(
#                  model_field.alias,
#                  inspect.Parameter.POSITIONAL_ONLY,
#                  default=Form(...) if model_field.required else Form(model_field.default),
#                  annotation=model_field.outer_type_,
#              )
#          )

#     async def as_form_func(**data):
#         return cls(**data)

#     sig = inspect.signature(as_form_func)
#     sig = sig.replace(parameters=new_parameters)
#     as_form_func.__signature__ = sig  # type: ignore
#     setattr(cls, 'as_form', as_form_func)
#     return cls


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @as_form
class Employee(BaseModel):
    employeeId : int
    firstName : str
    firstName : str
    lastName : str
    employeePhone: str
    employeeEmail : str

class Insight(BaseModel):
    Name: str
    Insight: str

employee_data = [
    {
        "employeeId": 1,
        "firstName": "Richard",
        "lastName": "Hendricks",
        "employeePhone": "(158) 389-2794",
        "employeeEmail": "richard@piedpiper.com",
    },
    {
        "employeeId": 2,
        "firstName": "Jared",
        "lastName": "Dunn",
        "employeePhone": "(518) 390-2749",
        "employeeEmail": "jared@piedpiper.com",
    },
    {
        "employeeId": 3,
        "firstName": "Erlich",
        "lastName": "Bachman",
        "employeePhone": "(815) 391-2974",
        "employeeEmail": "erlich.bachman@piedpiper.com",
    },
]

employee_data = [Employee(**item) for item in employee_data]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/employees")
async def list_employees():
    return ORJSONResponse(jsonable_encoder(employee_data))

@app.post("/add_employee")
async def add_employee(employee: Employee):
    employee_data.append(employee)

    return ORJSONResponse({
        "status": 200, "id":employee.employeeId
    })


insights = [
        {
            "Insight": "Insight text 1", "Name": "Insight1"
        },
        {
            "Insight": "Insight text 2", "Name": "Insight2"
        }
    ]

@app.get("/list_insight")
async def list_insights():
    return ORJSONResponse(insights)

@app.post("/add_insight")
async def add_insight(insight: Insight):
    insights.append(insight.__dict__)
    return 200

@app.post('/generate_pie_chart')
async def generate_pie_chart():
    try:
        # Hardcoded JSON data (you can replace this with your desired data)
        data = {
            "Category 1": 30,
            "Category 2": 50,
            "Category 3": 20,
        }

        labels = list(data.keys())
        values = list(data.values())

        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')

        # Save the pie chart to a BytesIO buffer
        image_buffer = io.BytesIO()
        plt.savefig(image_buffer, format='png')
        image_buffer.seek(0)

        # Return the image as a raw byte string
        return Response(content=image_buffer.read(), media_type="image/png")
    except Exception as e:
        return Response(content=str(e), status_code=500, media_type="text/plain")
