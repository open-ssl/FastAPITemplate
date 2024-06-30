import http

import pytest
from sqlalchemy import insert, select

from .auth.models import Role
from conftest import client
from tests.conftest import async_session_maker


async def test_create_new_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        filtered_query = select(Role).where(Role.id == 1)
        query_result = await session.execute(query)
        filtered_query_result = await session.execute(filtered_query)

        exp_result = [(1, "admin", None)]

        query_values = [item[0].as_tuple() for item in query_result.all()]
        filtered_query_values = [
            item[0].as_tuple() for item in filtered_query_result.all()
        ]

        assert query_values == exp_result, "No any roles in database"
        assert (
            filtered_query_values == exp_result
        ), "No role with identifier 1 in database"


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "username": "test_user",
            "email": "test_user@test_user.test_user",
            "password": "test_user1",
            "role_id": 0,
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )

    assert (
        response.status_code == http.HTTPStatus.CREATED
    ), "Incorrect status code on register_new_user"
    try:
        body = response.json()
        assert body.get("role_id") == 1, "Incorrect 'role_id' on register_new_user"
        assert body.get("is_active"), "Incorrect 'is_active' state on register_new_user"
    except:
        assert False, "No test register response body"
