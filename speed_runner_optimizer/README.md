# Speed Runner Optimizer

## Run baseline

python main.py --mode baseline --input bulk_data --output output

## Run optimized

python main.py --mode optimized --input bulk_data --output output

## Why multiprocessing?

Multiprocessing was chosen because file processing is CPU-bound and multiprocessing utilizes multiple CPU cores, giving better performance than threading.