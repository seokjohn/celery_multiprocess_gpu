import os
from app.celery_app import celery_app, PID_GPU_NUM


@celery_app.task(
    name="run_task",
    queue="task"
)
def run_task():
    import torch

    device = PID_GPU_NUM.get(os.getpid(), "cuda")

    vector_obj = torch.tensor([1, 2, 3, 4, 5], device=torch.device(device))

    result = vector_obj + vector_obj

    print(f"[*] task gpu:{device} result:{result}")
