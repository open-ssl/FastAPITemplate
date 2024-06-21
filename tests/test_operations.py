import http

from httpx import AsyncClient


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post(
        "/operations",
        json={
            "id": 1,
            "quantity": "25.5",
            "figi": "figi_CODE",
            "instrument_type": "bonds",
            "date": "2024-07-09T00:00:00",
            "type": "Bonds payment",
        },
    )

    assert (
        response.status_code == http.HTTPStatus.OK
    ), "Incorrect status code on add_specific_operations"


async def test_get_specific_operations(ac: AsyncClient):
    response_success = await ac.get(
        "/operations", params={"operation_type": "Bonds payment"}
    )

    response_failed = await ac.get(
        "/operations", params={"operation_type": "Action payment"}
    )

    assert (
        response_success.status_code == http.HTTPStatus.OK
    ), "Incorrect status for existed operation on get_specific_operation"
    assert (
        response_failed.status_code == http.HTTPStatus.OK
    ), "Incorrect status for not-existed operation on get_specific_operation"

    try:
        success_data = response_success.json()
        failed_data = response_failed.json()
        assert success_data.get("status") == "Success"
        assert failed_data.get("status") == "Success"

        assert (
            len(success_data.get("data")) == 1
        ), "Incorrect data count for existed operation on get_specific_operation"
        assert (
            len(failed_data.get("data")) == 0
        ), "Incorrect data count for not-existed operation on get_specific_operation"
    except Exception:
        assert False, "Error during get_specific operation"
