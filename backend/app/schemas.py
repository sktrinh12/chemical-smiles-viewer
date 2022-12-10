from typing import Optional, Dict, List

from pydantic import BaseModel, Field


class SMILESchema(BaseModel):
    regno: Optional[str] = Field(...)


class VKSchema(BaseModel):
    project_name: Optional[str] = Field(...)
    peyn_comment: Optional[int] = Field(...)
    smiles: Optional[str] = Field(...)
    qsar_model: Optional[float] = Field(...)
    model: Optional[str] = Field(...)
    kinnate_alias: Optional[str] = Field(...)
    transform: Optional[str] = Field(...)
    closest_names: Optional[str] = Field(...)
    cloest_smiles: Optional[str] = Field(...)
    tanimoto: Optional[float] = Field(...)
    best_similarity: Optional[float] = Field(...)
    no_prod_sim: Optional[int] = Field(...)
    project: Optional[str] = Field(...)
