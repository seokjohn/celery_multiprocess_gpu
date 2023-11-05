import os
from celery import Celery
from celery.signals import worker_process_init, worker_init


celery_app = Celery('app', broker='redis://localhost:6379/0')


WORKER_NAME: str = None
PID_GPU_NUM: dict = {}


@worker_init.connect
def configure_workers(sender=None, **kwargs):
    global WORKER_NAME
    WORKER_NAME = sender


@worker_process_init.connect
def set_gpu_for_concurrency(**kwargs):
    print("[*] Init set gpu for concurrency")
    gpu_num = len(os.environ.get("CUDA_VISIBLE_DEVICES").split(","))
    celery_app.control.inspect().active()
    celery_app.control.inspect().stats()
    inspect: dict = celery_app.control.inspect([str(WORKER_NAME)]).stats()
    if not PID_GPU_NUM:
        if inspect:
            concurrency_pid_list = list(inspect.values())[0]['pool']['processes']
            assert gpu_num >= len(concurrency_pid_list)

            global PID_GPU_NUM
            for gpu, pid in zip(range(gpu_num), concurrency_pid_list):
                PID_GPU_NUM[pid] = f"cuda:{gpu}"

        else:
            print("[*] Not found Celery Inspect")
