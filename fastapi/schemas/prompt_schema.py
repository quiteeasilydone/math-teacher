from pydantic import BaseModel, Field
from typing import List

class OCR(BaseModel):
    LATEX: str = Field(description="LATEX syntax extracted from images")
    
class condition(BaseModel):
    conditions: List[str] = Field(description="Conditions extracted from LATEX syntax")
    target: List[str] = Field(description="Target extracted from LATEX syntax")
    
class solution_steps(BaseModel):
    solution_steps: List[str] = Field(description="Solution process extracted from conditions and goals")
    
class wolfram_code(BaseModel):
    wolfram_code: str = Field(description="wolfram code from solution steps")

class commentary(BaseModel):
    commentary: str = Field(description="commentary from math problem")