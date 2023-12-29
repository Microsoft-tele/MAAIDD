import numpy as np
import pandas as pd
from mesa import Agent, Model

from src.package.h.logger import SingletonLogger

logger_ins = SingletonLogger()


class SingleAgent(Agent):
    def __init__(self, unique_id: int, model: Model, init_x=0., init_y=0., init_ux=0., init_uy=0., init_dot_x=0., init_dot_y=0.):
        super().__init__(unique_id, model)
        # Attributes of every single agent [x, y] which is info of position and control variable(u)
        self.x = init_x
        self.y = init_y
        self.ux = init_ux
        self.uy = init_uy
        self.x_dot = init_dot_x
        self.y_dot = init_dot_y
        self.sample_interval = self.model.sample_interval

    def __str__(self):
        return f"""\n[agent id:{self.unique_id}] [current time:{self.model.t:.2f}] [x:{self.x:.3f}] [y:{self.y:.3f}] [ux:{self.ux:.3f}] [uy:{self.uy:.3f}] [dot_x:{self.x_dot:.3f}] [dot_y:{self.y_dot:.3f}]"""

    def __to_pd_series__(self):
        data = {
            'AgentID': self.unique_id,
            'CurrentTime': self.model.t,
            'X': self.x,
            'Y': self.y,
            'UX': self.ux,
            'UY': self.uy,
            'DotX': self.x_dot,
            'DotY': self.y_dot
        }
        return pd.Series(data)

    def state_x(self, ith: int):
        self.__str__()
        # above code is in order to ignore err from pycharm, not important

        def x1(t):
            return 0.15 * np.sin(t)

        def x2(t):
            return 0.15 * np.cos(t)

        if ith == 0:
            return x1
        if ith == 1:
            return x2
        else:
            logger_ins.logger.error("Input err for ith")
            raise RuntimeError("Invalid input")

    def dynamic_update(self):
        """
        Simulate dynamic update
        """
        x_dot_t = self.state_x(0)(self.model.t) + self.ux
        y_dot_t = self.state_x(1)(self.model.t) + self.uy
        self.x_dot = x_dot_t
        self.y_dot = y_dot_t
        self.x = self.x + x_dot_t * self.sample_interval
        self.y = self.y + y_dot_t * self.sample_interval

    def step(self):
        """
        Step for this agent
        :return:
        """
        self.dynamic_update()


if __name__ == "__main__":
    pass
