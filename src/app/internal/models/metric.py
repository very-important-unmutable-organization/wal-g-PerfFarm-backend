from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class MetricBase(SQLModel):
    name: str  # TODO enum
    value: float


class Metric(MetricBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: Optional[int] = Field(default=None, foreign_key="run.id")
    run: Optional["Run"] = Relationship(back_populates="metrics")
