import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

exp_id1 = "100-100-20240107-2359"
exp_id2 = "100-100-20240108-2204"

project_dir = "D:\\git\\MAAIDD"

data1_path = os.path.join(project_dir, "result", exp_id1, "data", "df_collect")
data2_path = os.path.join(project_dir, "result", exp_id2, "data", "df_collect")

data1 = pd.read_csv(data1_path, compression="gzip")
data2 = pd.read_csv(data2_path, compression="gzip")

print(data1.columns)
print(data2.columns)

collect_df_list = []
for unique_id in data1["AgentID"].unique():
    df_agent_id = data1[data1["AgentID"] == unique_id][
        ["X", "Y", "UX", "UY", "DotX", "DotY"]].reset_index(drop=True)
    collect_df_list.append(df_agent_id)

# 将 DataFrame 转换为 NumPy 数组
collect_np_list = [df.values for df in collect_df_list]
# 使用 numpy.concatenate 将数组拼接成三维矩阵
# [timestamp, feature, node_num]
result_matrix1 = np.stack(collect_np_list, axis=-1)

collect_df_list = []
for unique_id in data2["AgentID"].unique():
    df_agent_id = data2[data2["AgentID"] == unique_id][
        ["X", "Y", "UX", "UY", "DotX", "DotY"]].reset_index(drop=True)
    collect_df_list.append(df_agent_id)

# 将 DataFrame 转换为 NumPy 数组
collect_np_list = [df.values for df in collect_df_list]
# 使用 numpy.concatenate 将数组拼接成三维矩阵
# [timestamp, feature, node_num]
result_matrix2 = np.stack(collect_np_list, axis=-1)

print(result_matrix1.shape)
print(result_matrix2.shape)

import matplotlib.pyplot as plt

# 假设 result_matrix1 和 result_matrix2 已经定义

ith_x1 = result_matrix1[:, 0, 0]
ith_y1 = result_matrix1[:, 1, 0]

ith_x2 = result_matrix2[:, 0, 0]
ith_y2 = result_matrix2[:, 1, 0]

# 绘制散点图并设置颜色和图例
plt.scatter(ith_x1, ith_y1, label='Curve 1', color='blue')
plt.scatter(ith_x2, ith_y2, label='Curve 2', color='orange')

# 添加图例
plt.legend()

# 显示图形
plt.show()


