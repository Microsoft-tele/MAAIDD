import sys
import pathlib

# 获取项目路径
project_path = pathlib.Path(__file__).resolve().parents[3]
sys.path.append(str(project_path))

node_num = 7                # node number
sample_interval = 0.05      # sampling interval
total_duration = 20         # total sampling time, units (s)
spread_interval_time = 0.7  # duration between control variable spread

alpha = 1.5                 # which is strength among different agents
is_draw_process = False     # whether drawing track draft when running simulation, if you want to use this function, you should rewrite it
