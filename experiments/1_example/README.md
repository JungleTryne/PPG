Разрешение 4176х2073
Время работы: 114.07 секунд
Скорость работы: ~0.04 мегапиксель / сек

```
time python3 main.py --bayer_path experiments/1_example/RGB_CFA.bmp --output_path experiments/1_example/Result.bmp
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2073/2073 [00:36<00:00, 56.93it/s]
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2073/2073 [01:03<00:00, 32.54it/s]
python3 main.py --bayer_path experiments/1_example/RGB_CFA.bmp --output_path   114.07s user 0.92s system 99% cpu 1:55.12 total
```

MSE: 82.57761358406663, PSNR: 28.962180328529232 db

```
python3 metrics.py --original_path experiments/1_example/Original.bmp --recovered_path experiments/1_example/Result.bmp
```