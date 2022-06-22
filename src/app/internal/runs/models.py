from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


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


class MetricBase(SQLModel):
    name: str  # TODO enum
    value: float
    repo: Optional[str]


class MetricOut(SQLModel):
    name: str  # TODO enum
    value: float
    repo: Optional[str]
    run: Run

class Metric(MetricBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: Optional[int] = Field(default=None, foreign_key="run.id")
    run: Optional["Run"] = Relationship(back_populates="metrics")


class RunCreateDocs(BaseModel):
    os: str
    commit_sha: str
    commit_time: datetime
    client_version: str
    client_environment: str
    repo: str
    metrics: List["MetricBase"]


class RunBaseWithMetricsAndIdDocs(BaseModel):
    id: int
    os: str
    commit_sha: str
    commit_time: datetime
    client_version: str
    client_environment: str
    metrics: List["MetricBase"]
