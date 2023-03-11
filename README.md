# Task 1.

The [Patterned Pixel Grouping (PPG)](https://web.archive.org/web/20160923211135/https://sites.google.com/site/chklin/demosaic/) algorithm was implemented in Python3

Run:

```
pip3 install -r requirements.txt
python3 main.py --bayer_path [Path to CFA_RGB] --output_path result.bmp
```

CFA_RGB must be in BMP format!

## Results

### General results

You can find the results of the algorithm, in addition to the manually run results, in the folder.
As a result, the physical resolution of the image itself does not change in any way. 
At the same time, color quality loses and artifacts appear. They are especially noticeable in the first image in the folder 1_example
in the gray noise area, where it is quite difficult to restore the gray color. 
Also small artifacts are observed in the interference area of the picture.
The overall quality of the picture decreases. This can be understood from the text on the box on the right
Mickey Mouse. The optical resolution goes down. This can be seen in the fact that
thin close together stripes begin to merge at 16-17 for the vertical and horizontal
samples.

Two more SD and FULL HD resolution images have been added. The Bayer matrix was restored using the `from_bmp_to_bayer.py` script,
which simply took one or another pixel color according to the matrix pattern.

The speed of the algorithms was evaluated with the time utility. Metrics were obtained using `metrics.py`.
The `--help` flag is available for each program. More details can be found in the README of each example
in the experiments folder. Brief summary:

### First example.

Resolution 4176x2073
Total running time: 114.07 seconds
Speed: ~0.04 megapixels/sec
MSE: 82.57761358406663, PSNR: 28.962180328529232 db

### Second example.

640x426 resolution
Running time: 3.692 seconds
Speed: ~0.074 megapixels/sec
MSE: 88.14021053403756, PSNR: 28.67906277325488 db

### Third example.

Resolution 1920x1080
Running time: 32.71 seconds
Speed: ~0.063 megapixels/sec
MSE: 88.41927652994792, PSNR: 28.665334037965494 db


Translated with www.DeepL.com/Translator (free version)
