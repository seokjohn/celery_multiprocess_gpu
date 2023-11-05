# Celery multiprocess gpu Ex
<p align="center"><img src="https://github.com/seokjohn/celery_multiprocess_gpu/assets/57163202/58640acd-e8ea-4edf-b250-3ad4f0235c4f"></p>

Example of running multiple GPUs concurrently and in parallel in celery.
For more details, click the [link](https://medium.com/@sujohn478/celery-%ED%95%9C-%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%EC%97%90%EC%84%9C-gpu-%EC%97%AC%EB%9F%AC%EA%B0%9C-%ED%95%A0%EB%8B%B9-%EB%B0%8F-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0-0eb6e1a0a1e8).


### solo

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
