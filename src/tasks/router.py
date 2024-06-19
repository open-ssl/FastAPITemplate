from fastapi import APIRouter, BackgroundTasks, Depends

from src.auth.base_config import current_user
from src.base_schemas import BaseResponse
from src.tasks.tasks import send_email_report_dashboard, send_email_report_dashboard_with_celery

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/dashboard", response_model=BaseResponse)
def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
    # ~ 1400 ms - Client is waiting for
    send_email_report_dashboard(user.username)
    # native fast api way to execute background task
    # ~ 500 ms - Task is processing with event loop or another thread
    background_tasks.add_task(send_email_report_dashboard, user.username)
    # celery style way to execute background task
    # ~ 600 ms Task is processing in the own celery process. Best way!
    send_email_report_dashboard_with_celery.delay(user.username)
    return {
        "status": 200,
        "data": " A letter has sent",
        "details": "",
    }
