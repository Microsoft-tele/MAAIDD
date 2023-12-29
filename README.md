# MAAIDD

# 1. Introduce
This project focus on analysing the effect on different Multi-agent dynamic system and graph.

## Dynamic function

$$
\dot x_i(t)=f(x_i(t),t)- \alpha \sum_{j=1}^{N}  l_{ij}x_j(t_k), t_k \le t < t_{k+1},k \in N, i=1,2, \cdots, N
$$

# 2. Usage

Strongly recommend use miniconda or conda
```sh
conda create --name=MAAIDD python=3.8
conda activate MAAIDD
```

## 2.1. Clone
```sh
git clone https://github.com/LosFurina/MAAIDD.git
```
## 2.2. Install requirement
```sh
pip install -r ./requirement
```
## 2.3. Run and save data

- You have no need to add any parameters when running, all parameters have been set below

- Please confirm you have changed correct arguments at config.py which relates to final data saving path
```sh
python run.py
```

# 3. Config file (valid)

All parameters have been set at src/package/h/config.py

You can change it follow your project

## 3.1. parameters introduce

| Variable              | Value                |
|-----------------------|----------------------|
| `node_num`            | 7                    |
| `sample_interval`     | 0.05                 |
| `total_duration`      | 20                   |
| `spread_interval_time`| 0.7                  |
| `alpha`               | 1.5                  |
| `is_draw_process`     | False                |

# 4. Issue

Please open issue following request

# 5. Connect us

EthanLee0302@proton.me