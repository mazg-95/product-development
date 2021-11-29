from typing import Optional
from fastapi import FastAPI, Query
from enum import Enum
from pydantic import BaseModel
from random import randint
from functools import reduce
from typing import List


app = FastAPI()

class Operation(str, Enum):
    sum = 'Sum'
    substract = "Substract"
    div = "Division"
    mult = "Multiplication"

@app.get("/sum")
def sum_of_operands(operands: List[int] = Query([])):
    return compute(Operation.sum, operands)

@app.get("/substract")
def substract(operands: List[int] = Query([])):
    return compute(Operation.substract, operands)

@app.get("/div")
def div(operands: List[int] = Query([])):
    return compute(Operation.div, operands)

@app.get("/mult")
def mult(operands: List[int] = Query([])):
    return compute(Operation.mult, operands)

@app.get("/compute/{operation}")
def operate(operation: Operation, operands: List[int] = Query([])):
    return compute(operation, operands)

def compute(operation: Operation, operands: List[int]):
    if operation == Operation.sum:
        return sum(operands)
    elif operation == Operation.substract:
        return reduce(lambda a,b: a - b, operands)
    elif operation == Operation.div:
        return reduce(lambda a,b: a/b, operands)
    return reduce(lambda a,b: a*b, operands)