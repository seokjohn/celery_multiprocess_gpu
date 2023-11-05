# Celery multiprocess gpu Ex
Example of running multiple GPUs concurrently and in parallel in celery

### sole

```bash
CUDA_VISIBLE_DEVICES=0 celery -A app.task worker --loglevel info -P processes -c 1
```

### multiprocess

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 celery -A app.task worker --loglevel info -P processes -c 4
```

## test run
```bash
python run.py
```
