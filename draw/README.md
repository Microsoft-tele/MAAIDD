# Drawing figure about simulation dataset

## 1. Drawing with time going(with animation)
```sh
python ./draw.py
```
Remember to change path of loaded dataset
```python
df_collect = pd.read_csv("D:\\git\\MAAIDD\\result\\7-80-20240102-0103\\data\\df_collect", compression="gzip")
```

## 2. Drawing directly(without animation)
```sh
python ./draw_with_no_animation.py
```
Remember to change path of loaded dataset
```python
df_collect = pd.read_csv("D:\\git\\MAAIDD\\result\\7-80-20240102-0103\\data\\df_collect", compression="gzip")
```