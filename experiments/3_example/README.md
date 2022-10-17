Разрешение 1920x1080
Время работы: 32.71 секунд
Скорость работы: ~0.063 мегапиксель / сек

```
time python3 main.py --bayer_path experiments/3_example/RGB_CFA.bmp --output_path experiments/3_example/Result.bmp
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1280/1280 [00:10<00:00, 122.63it/s]
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1280/1280 [00:17<00:00, 71.82it/s]
python3 main.py --bayer_path experiments/3_example/RGB_CFA.bmp --output_path   32.34s user 0.23s system 99% cpu 32.710 total
```

MSE: 88.41927652994792, PSNR: 28.665334037965494 db

```
python3 metrics.py --original_path experiments/3_example/Original.bmp --recovered_path experiments/3_example/Result.bmp
```