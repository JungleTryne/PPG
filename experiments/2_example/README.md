Разрешение 640x426
Время работы: 3.692 секунд
Скорость работы: ~0.074 мегапиксель / сек

```
time python3 main.py --bayer_path experiments/2_example/RGB_CFA.bmp --output_path experiments/2_example/Result.bmp
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 426/426 [00:01<00:00, 373.76it/s]
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 426/426 [00:01<00:00, 215.90it/s]
python3 main.py --bayer_path experiments/2_example/RGB_CFA.bmp --output_path   3.64s user 0.04s system 99% cpu 3.692 total
```

MSE: 88.14021053403756, PSNR: 28.67906277325488 db

```
python3 metrics.py --original_path experiments/2_example/Original.bmp --recovered_path experiments/2_example/Result.bmp
```
