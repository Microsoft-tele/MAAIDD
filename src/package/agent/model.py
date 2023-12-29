import random
import sys
import pathlib

import pandas as pd

project_path = pathlib.Path(__file__).resolve().parents[3]
sys.path.append(str(project_path))

from typing import Any
from matplotlib import pyplot as plt

import mesa
import numpy as np
import src.package.h.config as cfg

from src.package.h.logger import SingletonLogger
from src.package.agent.agent import SingleAgent
from src.package.topology.topology import Topology

logger_ins = SingletonLogger()


class MyModel(mesa.Model):
    """
    # TODO: Docstring for MyModel(remember to change the name of system)
    Anonymous model
    """

    def __init__(self, num: int, adjacency_matrix: np.ndarray, sample_interval: float, *args: Any, **kwargs: Any):
        """
        Initialization method
        :param num: number of agents
        :param adjacency_matrix: initial adjacency matrix
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.num_agents = num  # number of agents
        self.schedule = mesa.time.RandomActivation(self)  # controller of mesa(python package)
        self.t = 0  # current time
        self.sample_interval = sample_interval  # sample interval, in this sample is 0.1

        self.adj = adjacency_matrix  # adjacency load from another class
        degrees = np.sum(self.adj, axis=0)  # degree matrix calculate from adjacency
        self.laplacian_matrix = np.diag(degrees) - self.adj  # laplacian matrix which is L = D - W

        self.df_data = None  # used to save collected data

        # add every single agent to schedule
        init_states = [
            [1.25, 0.05],
            [-0.5, 0.175],
            [0, 0],
            [1.5, -0.75],
            [3.0, -0.65],
            [1.75, 0.45],
            [0.55, 0.6]
        ]
        # we can load this from a random list, this init_state matrix is a sample from book
        for unique_id in range(self.num_agents):
            agent = SingleAgent(unique_id, self, init_x=init_states[unique_id][0], init_y=init_states[unique_id][1])
            self.schedule.add(agent)

        # some attribute for drawing
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        plt.ion()
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('Agent Positions')
        # 添加图例
        self.ax.legend()

    def _calculate_new_control_variable(self, alpha=cfg.alpha):
        """
        calculate latest u and update self.u
        """
        current_time = self.t
        current_state = []
        for agent in self.schedule.agents:
            # get all states from single agent
            states = [agent.state_x(0)(current_time), agent.state_x(1)(current_time)]
            current_state.append(states)

        # convert list to np, which could be convenient to calculate matrix
        current_state = np.array(current_state)
        # calculate new control variable from current position
        new_control_matrix = -alpha * np.dot(self.laplacian_matrix, current_state)

        for unique_id in range(self.num_agents):
            # put new control variable to every single agent
            self.schedule.agents[unique_id].ux = new_control_matrix[unique_id][0]
            self.schedule.agents[unique_id].uy = new_control_matrix[unique_id][1]

    def _update_plot(self, iths=None):
        # 从模型中获取 agent 的位置
        if iths is None:
            iths = [0, 1, 2, 3, 5, 6]

        agent_positions = np.array([(agent.x, agent.y) for agent in self.schedule.agents])
        # logger_ins.logger.info(f"\nPositions of agents:\n {agent_positions}")

        # 绘制 agent 的位置
        for ith in iths:
            if ith == 0:
                color = "blue"
            elif ith == 1:
                color = "red"
            elif ith == 2:
                color = "green"
            elif ith == 3:
                color = "yellow"
            elif ith == 4:
                color = "orange"
            elif ith == 5:
                color = "purple"
            elif ith == 6:
                color = "cyan"

            self.ax.scatter(agent_positions[:, 0][ith], agent_positions[:, 1][ith], color=color, s=5)

        # 在绘制中暂停，以便图形可以更新
        plt.pause(0.001)

    def step(self, is_update_control=False):
        # if attach condition then change control variable
        if is_update_control:
            self._calculate_new_control_variable()

        self.schedule.step()
        if cfg.is_draw_process:
            self._update_plot()

        for ith in range(len(self.schedule.agents)):
            logger_ins.logger.info(f"Agent Position: {self.schedule.agents[ith].__str__()}")

        agent_series_list = [agent.__to_pd_series__() for agent in self.schedule.agents]
        df_agents = pd.concat(agent_series_list, axis=1).T
        self.df_data = pd.concat([self.df_data, df_agents], axis=0)
        return df_agents


if __name__ == "__main__":
    pass
