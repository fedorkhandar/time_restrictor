from pids import PidProcessor
import json
import time
import datetime
from screen_protector import ScreenProtector
from db import Db
from transitions import Machine

class Restrictor(object):
    states = ['sleeping', 'waiting_session', 'waiting_rest', 'waiting_asleep']

    def read_conig(self):
        with open("config.json", "r") as fp:
            self.config = json.load(fp)
    
    def is_day_started(self):
        now_ms = int(time.time() * 1000)
        ms_per_day = 24 * 60 * 60 * 1000  # 86400000
        ms_since_midnight = now_ms - (now_ms // ms_per_day)

        return ms_since_midnight >= self.config["limits"]["day_starts_ms"]

    def __init__(self, name):
        self.name = name
        self.read_conig()

        self.sessions_left = self.config["limits"]["sessions_n_max"]
        self.db = Db(self.config["config"]["db_name"], self.config["limits"])
        self.pid_processor = PidProcessor()

        initial_state = "waiting_session" if self.is_day_started() else "sleeping"
        self.fsm = Machine(model=self, states=Restrictor.states, initial=initial_state)

        # self.fsm.add_transition(...)

    def get_restricted(self):
        windows = self.pid.get_windows()
        self.restricted = set()
        for window in windows:
            for title in self.config["restricted_apps"]:
                if (
                    window["process_name"].find(title) >= 0
                    or window["title"].find(title) >= 0
                ):
                    self.restricted.add(window["pid"])
   
        
    def run(self):
        while True:
            self.get_restricted()
            

            
            # time.sleep(self.config["config"]["period_sec"])
            # restricted = self.check_restricted(self)
            # if restricted:
            #     db_response = self.db.get_sessions_info()

            #     if db_response["is_session_closed"]:
            #         session_left_n = self.config["limits"]["sessions_n_max"] - db_response["sessions_n"]
                    
            #         if db_response["current_rest_duration_ms"] < self.config["limits"]["minimal_rest_period_ms"] or session_left_n == 0:
            #             # minimize target windows
            #             for pid in restricted:
            #                 self.pid_processor.minimize_window_by_pid(pid)

            #             # show screen saver
            #             sp = ScreenProtector(
            #                 session_left_n
            #             )


            #             sp.run()
            #         else:
            #             self.db.session_start()


def main():
    r = Restrictor()
    r.run()
        

if __name__ == "__main__":
    main()
