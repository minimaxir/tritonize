# tritonize Examples

These examples of `tritonize` use the [Lenna test image](http://www.ece.rice.edu/~wakin/images/).

## Command-Line Arguments For Examples

### 3-Colors

```shell
python tritonize.py -i Lenna.png -c "#1a1a1a" "#FFFFFF" "#2c3e50" -b 10
```

### 4-Colors

```shell
python tritonize.py -i Lenna.png -c "#1a1a1a" "#FFFFFF" "#2c3e50" "#c0392b" -b 6
```

### 5-Colors

```shell
python tritonize.py -i Lenna.png -c "#1a1a1a" "#FFFFFF" "#2c3e50" "#c0392b" "#7f8c8d"
```

### Transparent

```shell
python tritonize.py -i Lenna.png -c "(0, 0, 0, 0)" "(26, 26, 26, 128)" "(255, 255, 255, 255)" -b 2
```