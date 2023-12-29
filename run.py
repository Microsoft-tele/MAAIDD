import src.package.h.config as cfg

from src.package.h.logger import SingletonLogger
from src.package.topology.topology import Topology
from src.package.agent.model import MyModel

import numpy as np


class Main(object):
    def __init__(self):
        """
        You can set some args at here
        """
        pass

    def run(self):
        self.__str__()
        sample_topology, laplacian = Topology().generate_sample_topology()
        sample_interval = cfg.sample_interval  # 采样间隔，单位秒
        model = MyModel(num=7, adjacency_matrix=sample_topology, sample_interval=sample_interval)
        total_duration = cfg.total_duration  # 总采样持续时间，单位秒
        spread_interval_time = cfg.spread_interval_time
        spread_interval = int(spread_interval_time // sample_interval)
        # 生成时间戳列表
        time_stamps = np.arange(0, total_duration + sample_interval, sample_interval)
        cnt = spread_interval
        for i in time_stamps:  # control tim here
            # Every 5 timestamp go spreading
            if cnt == spread_interval:
                model.t = i
                model.step(is_update_control=True)
                cnt = 0
            else:
                model.t = i
                model.step(is_update_control=False)
            cnt += 1
            print("Current timestamp: ", cnt)

        input("Press any key to continue...")
        print(model.df_data)
        print(model.df_data.shape)


if __name__ == "__main__":
    main = Main()
    main.run()
