from typing import List

from fastapi import Depends
from fastapi.params import Body, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.internal.auth.models import User
from app.internal.auth.services import UserService
from app.internal.core.db import get_session
from app.internal.core.dependencies import get_jwt_bearer
from app.internal.runs.models import (
    Metric,
    Run,
    RunBaseWithMetricsAndId,
    RunBaseWithMetricsAndIdDocs,
    RunCreate,
    RunCreateDocs,
    MetricBase, MetricOut,
)
from app.pkg.auth.auth_bearer import JWTBearer

runs_router = APIRouter(
    prefix="",
    tags=["runs"],
    responses={404: {"description": "Not found"}},
)


@runs_router.get("/runs", response_model=List[RunBaseWithMetricsAndIdDocs])
async def get_runs(
    session: AsyncSession = Depends(get_session),
) -> List[RunBaseWithMetricsAndId]:
    result = await session.execute(select(Run).distinct(Run.commit_sha).options(selectinload(Run.metrics)))
    runs = result.scalars().all()

    return runs


@runs_router.post("/runs", dependencies=[Depends(JWTBearer(UserService()))], response_model=Run)
async def add_run(
    run_create: RunCreateDocs = Body(...),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_jwt_bearer, use_cache=False),
) -> Run:
    metrcs = [metric.dict() for metric in run_create.metrics]
    for metric in metrcs:
        metric['repo'] = run_create.repo

    metrics = [Metric(**metric) for metric in metrcs]
    run_create = run_create.dict()
    run_create.pop("metrics")
    run = Run(metrics=metrics, **run_create)

    session.add(run)
    await session.commit()
    await session.refresh(run)

    return run


@runs_router.get("/metrics/names", response_model=List[str])
async def get_metrics_names(
    session: AsyncSession = Depends(get_session),
) -> List[str]:
    result = await session.execute(select(Metric).distinct(Metric.name))
    runs = result.scalars().all()
    answer = []
    for run in runs:
        answer.append(run.name)

    return answer


@runs_router.get("/metrics/{name}", response_model=List[MetricOut])
async def get_metrics_by_name(
    session: AsyncSession = Depends(get_session),
    name: str = Path(...)
) -> List[MetricOut]:
    result = await session.execute(select(Metric).where(Metric.name == name).options(selectinload(Metric.run)))
    runs = result.scalars().all()

    return runs

