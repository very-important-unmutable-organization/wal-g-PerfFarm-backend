from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship
from app.internal.models.metric import Metric, MetricBase


class RunBase(SQLModel):
    os: str
    commit_sha: str
    commit_time: datetime
    client_version: str
    client_environment: str


class RunBaseWithMetrics(RunBase):
    metrics: List["MetricBase"]


class RunBaseWithMetricsAndId(RunBase):
    id: int
    metrics: List["MetricBase"]


class Run(RunBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    metrics: List["Metric"] = Relationship(back_populates="run")


class RunCreate(RunBaseWithMetrics):
    pass


