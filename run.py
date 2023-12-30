import pickle
import time

import src.package.h.config as cfg

from src.package.h.logger import SingletonLogger
from src.package.topology.topology import Topology
from src.package.agent.model import MyModel

import numpy as np

current_time = time.strftime("%Y%m%d-%H%M")
my_path = cfg.ProjectPath(current_time)
logger_ins = SingletonLogger(my_path)


class Main(object):
    def __init__(self):
        """
        You can set some args at here
        """
        # TODO: If you want add args from terminal, you can ues args package
        pass

    def run(self):
        self.__str__()
        # TODO: set graph here
        if cfg.is_random_graph:
            sample_topology, laplacian = Topology().generate_random_topology(cfg.node_num, 3)
            init_states = np.random.uniform(low=-10, high=10, size=(cfg.node_num, 2))
        else:
            sample_topology, laplacian = Topology().generate_sample_topology()  # laplacian is useless. please notice, we calculate it in inner function
            init_states = None

        interval_time_x = cfg.sample_interval  # sampling interval unit(s)
        model = MyModel(num=cfg.node_num, adjacency_matrix=sample_topology, sample_interval=interval_time_x, init_states=init_states)
        total_duration = cfg.total_duration  # total sample duration
        interval_time_u = cfg.spread_interval_time
        interval_step_u = int(interval_time_u // interval_time_x)
        # generate timestamp list
        time_stamps = np.arange(0, total_duration + interval_time_x, interval_time_x)
        cnt = interval_step_u
        for i in time_stamps:  # control tim here
            # Every 5 timestamp go spreading
            if cnt == interval_step_u:
                logger_ins.logger.warning("Spreading control variable---")
                model.t = i
                model.step(is_update_control=True)
                cnt = 0
            else:
                model.t = i
                model.step(is_update_control=False)
            cnt += 1

        model.df_data.to_csv(my_path.get_data_save_path(), compression="gzip")
        with open(my_path.get_topology_save_path(), "wb") as f:
            pickle.dump(sample_topology, f)

        logger_ins.logger.info("Finished generating, please check the output at {}".format(my_path.get_data_save_path()))
        logger_ins.logger.info("Finished generating, please check the output at {}".format(my_path.get_topology_save_path()))


if __name__ == "__main__":
    main = Main()
    main.run()
