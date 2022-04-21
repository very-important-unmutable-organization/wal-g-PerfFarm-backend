from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from sqlalchemy.orm import selectinload
from app.internal.models.metric import Metric
from app.internal.models.runs import Run, RunCreate, RunBaseWithMetricsAndId
from app.internal.core.db import get_session

app = FastAPI()


@app.get("/runs", response_model=List[RunBaseWithMetricsAndId])
async def get_runs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Run).options(selectinload(Run.metrics)))
    runs = result.scalars().all()

    return runs


@app.post("/runs", response_model=Run)
async def add_run(run_create: RunCreate, session: AsyncSession = Depends(get_session)):
    metrics = [Metric(**metric.dict()) for metric in run_create.metrics]
    run_create = run_create.dict()
    run_create.pop('metrics')
    run = Run(
        metrics=metrics,
        **run_create
    )

    session.add(run)
    await session.commit()
    await session.refresh(run)

    return run
