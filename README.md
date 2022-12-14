# Задание 1

Был реализован алгоритм [Patterned Pixel Grouping (PPG)](https://web.archive.org/web/20160923211135/https://sites.google.com/site/chklin/demosaic/) на языке Python3

Запуск:

```
pip3 install -r requirements.txt
python3 main.py --bayer_path [Path to CFA_RGB] --output_path result.bmp
```

CFA_RGB должен быть в формате BMP!

## Результаты

### Общие выводы

Результаты работы алгоритма, помимо мануального запуска, можно найти в папке experiments.
В результате само физическое разрешение изображения никак не меняется. 
При этом теряется цветовое качество и возникают артифакты. Они особо заметны на первом изображении в папке 1_example
в области серого шума, где довольно сложно восстановить серый цвет. 
Также небольшие артифакты наблюдаются в области интерференции картинки.
Общее качество картинки уменьшается. Это можно понять по тексту на коробке правее
Микки-Мауса. Оптическое разрешение падает. Это можно увидеть по тому, что
тонкие близкие друг к другу полосы начинают сливаться на уровне 16-17 для вертикальных и горизонтальных
образцов.

Было добавлено еще 2 картинки разрешения SD и FULL HD. Матрица Байера была восстановлена с помощью скрипта `from_bmp_to_bayer.py`,
в котором просто брался тот или иной цвет пикселя в соответствии с паттерном матрицы.

Оценка скорости алгоритмов проводилась с помощью утилиты time. Метрики получались с помощью `metrics.py`.
Для каждой программы доступен флаг `--help`. Более подробные данные можно посмотреть в README каждого примера
в папке experiments. Краткая сводка:

### Первый пример.

Разрешение 4176х2073
Время работы: 114.07 секунд
Скорость работы: ~0.04 мегапиксель / сек
MSE: 82.57761358406663, PSNR: 28.962180328529232 db

### Второй пример

Разрешение 640x426
Время работы: 3.692 секунд
Скорость работы: ~0.074 мегапиксель / сек
MSE: 88.14021053403756, PSNR: 28.67906277325488 db

### Третий пример

Разрешение 1920x1080
Время работы: 32.71 секунд
Скорость работы: ~0.063 мегапиксель / сек
MSE: 88.41927652994792, PSNR: 28.665334037965494 db
