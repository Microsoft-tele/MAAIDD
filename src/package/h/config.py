import os
import sys
import pathlib
import time

# get project root path
project_path = pathlib.Path(__file__).resolve().parents[3]
sys.path.append(str(project_path))

# TODO: Should set const config variable to yaml or json

node_num = 50  # node number
sample_interval = 0.01  # sampling interval
total_duration = 80  # total sampling time, units (s)
spread_interval_time = 0.4  # duration between control variable spread
alpha = 1.5  # which is strength among different agents

is_random_graph = True  # Remember if you set this as False, node number must be 7
is_draw_process = False  # whether drawing track draft when running simulation, if you want to use this function, you should rewrite it
is_show_log = True  # True: print all log on terminal, otherwise, just print log to file


class ProjectPath(object):
    def __init__(self, exp_id="default"):
        self.exp_id = exp_id
        self.project_path = project_path
        self.result_path_dir = os.path.join(self.project_path, "result")
        self._check()
        self._create_dir()

    def _check(self):
        if self.exp_id == "default":
            raise Exception("Please set your experiment id")

    def _create_dir(self):
        for key, value in self.__dict__.items():
            if key.__contains__("dir"):
                os.makedirs(value, exist_ok=True)

    def get_data_save_path(self):
        dir_path = os.path.join(self.result_path_dir, self.exp_id, "data")
        os.makedirs(dir_path, exist_ok=True)
        return os.path.join(os.path.join(dir_path, "df_collect"))

    def get_topology_save_path(self):
        dir_path = os.path.join(self.result_path_dir, self.exp_id, "topology")
        os.makedirs(dir_path, exist_ok=True)
        return os.path.join(os.path.join(dir_path, f"topology_{self.exp_id}.pickle"))

    def get_log_save_path(self):
        dir_path = os.path.join(self.result_path_dir, self.exp_id, "log")
        os.makedirs(dir_path, exist_ok=True)
        return os.path.join(os.path.join(dir_path, f"log_{self.exp_id}.log"))

    def get_readme_save_path(self):
        dir_path = os.path.join(self.result_path_dir, self.exp_id)
        os.makedirs(dir_path, exist_ok=True)
        return os.path.join(os.path.join(dir_path, f"README.md"))


if __name__ == '__main__':
    current_time = time.strftime("%Y%m%d-%H%M")
    path_controller = ProjectPath(current_time)
    data_path = path_controller.get_data_save_path()
    log_path = path_controller.get_log_save_path()
