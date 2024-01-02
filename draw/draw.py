import pandas as pd
import matplotlib.pyplot as plt

# 从 gzip 压缩文件读取数据
df_collect = pd.read_csv("D:\\git\\MAAIDD\\result\\7-80-20240102-0103\\data\\df_collect", compression="gzip")

# 选择 agent_id 列为 1 的行
df_list = []
for agent_id in df_collect["AgentID"].unique():
    df_agent_id = df_collect[df_collect['AgentID'] == agent_id]
    df_list.append(df_agent_id)

# 创建轨迹图
plt.subplots(figsize=(10, 10))

for idx in range(len(df_list[0])):
    for agent_id in df_collect["AgentID"].unique():

        plt.scatter(df_list[int(agent_id)][:idx+1].X, df_list[int(agent_id)][:idx+1].Y, label=f"Step {idx + 1}", color='blue', s=5)
    plt.pause(0.1)  # 暂停一小段时间以展示轨迹过程

# 设置图表标题和标签
plt.title('Agent ID 1 Trajectory')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

# 显示图例
plt.legend()


plt.show()
