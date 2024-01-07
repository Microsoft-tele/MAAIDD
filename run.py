import pickle
import time

import src.package.h.config as cfg

from src.package.h.logger import SingletonLogger
from src.package.topology.topology import Topology
from src.package.agent.model import MyModel

import numpy as np

current_time = time.strftime("%Y%m%d-%H%M")
exp_id = f"{cfg.node_num}-{cfg.total_duration}-{current_time}"
my_path = cfg.ProjectPath(exp_id=exp_id)
logger_ins = SingletonLogger(my_path)


class Main(object):
    def __init__(self):
        """
        You can set some args at here
        """
        # TODO: If you want add args from terminal, you can ues args package
        pass

    def __to_readme__(self):
        self.__str__()
        return f""" # {my_path.exp_id}
        
Hyperparameters        | Value 
|----------------------|---------------|
| `node_num`           | {cfg.node_num} |
| `sample_interval`    | {cfg.sample_interval} |
| `total_duration`     | {cfg.total_duration} |
| `spread_interval_time`| {cfg.spread_interval_time} |
| `alpha`              | {cfg.alpha} |
| `is_draw_process`    | {cfg.is_draw_process} |
| `is_show_log`        | {cfg.is_show_log}   |
| `network`            | {cfg.network} |
| `is_random_graph`    | {cfg.is_random_graph} |
        """

    def run(self):
        self.__str__()
        # TODO: set graph here
        if cfg.network is not None:
            # TODO: loading topology from AIDD is what next we should be going
            if cfg.network["is_load_from_file"] is True:
                with open("D:/git/MAAIDD/result/100-100-20240107-2359/topology/topology.pickle", "rb") as f:
                    sample_topology: np.ndarray = pickle.load(f)

                with open("D:/git/MAAIDD/result/100-100-20240107-2359/init_state/init_state.pickle", "rb") as f:
                    init_states = pickle.load(f)
                logger_ins.logger.info("Load topology and initial states from file!")
            else:
                sample_topology, laplacian = Topology.generate_er_ws_ba_graph(num_nodes=cfg.node_num, net=cfg.network)
                init_states = np.random.uniform(low=-10, high=10, size=(cfg.node_num, 2))
        elif cfg.is_random_graph:
            sample_topology, laplacian = Topology().generate_random_topology(cfg.node_num, 3)
            init_states = np.random.uniform(low=-10, high=10, size=(cfg.node_num, 2))
        else:
            sample_topology, laplacian = Topology().generate_sample_topology()  # laplacian is useless. please notice, we calculate it in inner function
            init_states = None

        model = MyModel(num=cfg.node_num, adjacency_matrix=sample_topology, sample_interval=cfg.sample_interval,
                        init_states=init_states)
        total_duration = cfg.total_duration  # total sample duration
        interval_time_u = cfg.spread_interval_time
        interval_time_x = cfg.sample_interval  # sampling interval unit(s)
        interval_step_u = int(interval_time_u // interval_time_x)
        # generate timestamp list
        time_stamps = np.arange(0, total_duration + interval_time_x, interval_time_x)
        cnt = interval_step_u
        for i in time_stamps:  # control tim here
            # Every 5 timestamp go spreading
            if cnt == interval_step_u:
                logger_ins.logger.warning("Spreading control variable---")
                model.t = i
                model.step(is_update_control=True, alpha=cfg.alpha)
                cnt = 0
            else:
                model.t = i
                model.step(is_update_control=False, alpha=cfg.alpha)
            cnt += 1

        model.df_data.to_csv(my_path.get_data_save_path(), compression="gzip")
        logger_ins.logger.info(
            "Finished generating, please check collected data at {}".format(my_path.get_data_save_path()))

        with open(my_path.get_topology_save_path(), "wb") as f:
            pickle.dump(sample_topology, f)
            logger_ins.logger.info(
                "Finished generating, please check topology data at {}".format(my_path.get_topology_save_path()))

        with open(my_path.get_init_state_save_path(), "wb") as f:
            pickle.dump(init_states, f)
            logger_ins.logger.info(
                "Finished generating, please check initial states at {}".format(my_path.get_init_state_save_path()))

        with open(my_path.get_readme_save_path(), "w+") as f:
            f.write(self.__to_readme__())
            logger_ins.logger.info(
                "Finished generating, please check README at {}".format(my_path.get_readme_save_path()))


if __name__ == "__main__":
    main = Main()
    main.run()
