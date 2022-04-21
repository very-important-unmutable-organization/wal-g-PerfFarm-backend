from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.internal.core.db import get_session
from app.internal.models.metric import Metric
from app.internal.models.runs import Run, RunBaseWithMetricsAndId, RunCreate

app = FastAPI()


@app.get("/runs", response_model=List[RunBaseWithMetricsAndId])
async def get_runs(session: AsyncSession = Depends(get_session)) -> List[RunBaseWithMetricsAndId]:
    result = await session.execute(select(Run).options(selectinload(Run.metrics)))
    runs = result.scalars().all()

    return runs


@app.post("/runs", response_model=Run)
async def add_run(run_create: RunCreate, session: AsyncSession = Depends(get_session)) -> Run:
    metrics = [Metric(**metric.dict()) for metric in run_create.metrics]
    run_create = run_create.dict()
    run_create.pop("metrics")
    run = Run(metrics=metrics, **run_create)

    session.add(run)
    await session.commit()
    await session.refresh(run)

    return run
