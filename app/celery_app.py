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
    load_count = 0
    max_load_count = 6

    while True:
        gpu_num = len(os.environ.get("CUDA_VISIBLE_DEVICES").split(","))
        inspector = celery_app.control.inspect()
        inspector.active()
        inspector.registered()
        inspector_stats = inspector.stats()

        if inspector_stats:
            inspect: dict = inspector_stats.get(str(WORKER_NAME))
            concurrency_pid_list = inspect['pool']['processes']
            assert gpu_num >= len(concurrency_pid_list)

            for gpu, pid in zip(range(gpu_num), concurrency_pid_list):
                PID_GPU_NUM[pid] = f"cuda:{gpu}"

            break
        else:
            if load_count >= max_load_count:
                raise Exception("Inspector Set Error")
            load_count += 1
