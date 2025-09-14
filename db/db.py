from dataclasses import dataclass


@dataclass
class DbResponse:
    is_session_closed: bool
    current_rest_duration_ms: int
    sessions_n: int

class Db:
    def __init__(self, limits):
        self.day_start_ms = limits["day_start_ms"]
        self.day_end_ms = limits["day_end_ms"]
        self.session_n_max = limits["session_n_max"]
        self.session_duration_ms = limits["session_duration_ms"]
        self.minimal_rest_period_ms = limits["minimal_rest_period_ms"]

    def get_today_beginning_ms(self):
        return 0

    def get_sessions_info(self):
        # "select from sessions (start_time, end_time) where start_day > {}".format(today_start_ms)
        ret = DbResponse(
            is_session_closed=True,
            last_session_end_ms=0,
            sessions_n=2
        )

        return ret

