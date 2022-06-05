from typing import List

from fastapi import Depends
from fastapi.params import Body
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
)
from app.pkg.auth.auth_bearer import JWTBearer

runs_router = APIRouter(
    prefix="/runs",
    tags=["runs"],
    responses={404: {"description": "Not found"}},
)


@runs_router.get("", dependencies=[Depends(JWTBearer(UserService()))], response_model=List[RunBaseWithMetricsAndIdDocs])
async def get_runs(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_jwt_bearer, use_cache=False),
) -> List[RunBaseWithMetricsAndId]:
    result = await session.execute(select(Run).options(selectinload(Run.metrics)))
    runs = result.scalars().all()

    return runs


@runs_router.post("", dependencies=[Depends(JWTBearer(UserService()))], response_model=Run)
async def add_run(
    run_create: RunCreateDocs = Body(...),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_jwt_bearer, use_cache=False),
) -> Run:
    metrics = [Metric(**metric.dict()) for metric in run_create.metrics]
    run_create = run_create.dict()
    run_create.pop("metrics")
    run = Run(metrics=metrics, **run_create)

    session.add(run)
    await session.commit()
    await session.refresh(run)

    return run
