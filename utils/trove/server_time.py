from datetime import datetime, timedelta, UTC

from models.constants import files_cache


class ServerTime:
    def __init__(self, page):
        self.page = page
        self.trove_time = timedelta(hours=11)
        self.dragon_duration = timedelta(days=3)
        self.dragon_interval = timedelta(days=14)
        self.fluxion_interval = timedelta(days=7)
        self.first_week_buff = datetime(2020, 3, 23, tzinfo=UTC)
        self.first_luxion = datetime(2024, 3, 1, tzinfo=UTC)
        self.first_corruxion = datetime(2024, 3, 8, tzinfo=UTC)
        self.first_fluxion = datetime(2023, 7, 11, tzinfo=UTC)

    def __str__(self):
        return self.now.strftime("%a, %b %d\t\t%H:%M")

    @property
    def now(self):
        return datetime.now(UTC) - self.trove_time

    # Daily
    @property
    def daily_buffs(self):
        return files_cache["daily_buffs.json"]

    @property
    def current_daily_buffs(self):
        return self.daily_buffs[str(self.now.weekday())]

    # Weekly

    @property
    def weekly_buffs(self):
        return files_cache["weekly_buffs.json"]

    @property
    def current_weekly_buffs(self):
        week_length = 60 * 60 * 24 * 7
        weeks = (self.now.timestamp() - self.first_week_buff.timestamp()) // week_length
        time_split = weeks / 4
        time_find = (time_split - int(time_split)) * 4
        return self.weekly_buffs[str(int(time_find))]

    # Dragons

    def _calculate_dragon(self, first):
        delta = self.now - first
        completed, current = divmod(
            int(delta.total_seconds()), int(self.dragon_interval.total_seconds())
        )
        next_luxion = first + (completed + 1) * self.dragon_interval
        return completed, next_luxion, current

    def is_dragon(self, first):
        return self._calculate_dragon(first)[2] < self.dragon_duration.total_seconds()

    def next_dragon(self, first):
        return self._calculate_dragon(first)[1]

    def until_next_dragon(self, first):
        return self.next_dragon(first) - self.now

    def previous_dragon(self, first):
        completed, next_dragon, current = self._calculate_dragon(first)
        return next_dragon - self.dragon_interval

    def end_dragon(self, first):
        if self.is_dragon(first):
            return self.previous_dragon(first) + self.dragon_duration
        else:
            return self.next_dragon(first) + self.dragon_duration

    def until_end_dragon(self, first):
        return self.end_dragon(first) - self.now

    # Fluxion

    def _calculate_fluxion(self):
        delta = self.now.timestamp() - self.first_fluxion.timestamp()
        completed, current = divmod(delta, self.dragon_interval.total_seconds())
        phase, current = divmod(current, self.fluxion_interval.total_seconds())
        next_phase = (
            self.first_fluxion + (completed * 2 + (phase + 1)) * self.fluxion_interval
        )
        return completed, phase, current, next_phase

    def is_fluxion(self):
        return self._calculate_fluxion()[2] < self.dragon_duration.total_seconds()

    def is_fluxion_voting(self):
        return self._calculate_fluxion()[1] == 0

    def is_fluxion_selling(self):
        return self._calculate_fluxion()[1] == 1

    def next_fluxion(self):
        return self._calculate_fluxion()[3]

    def until_next_fluxion(self):
        return self.next_fluxion() - self.now

    def previous_fluxion(self):
        return self.next_fluxion() - self.fluxion_interval

    def end_fluxion(self):
        if self.is_fluxion():
            return self.previous_fluxion() + self.dragon_duration
        else:
            return self.next_fluxion() + self.dragon_duration

    def until_end_fluxion(self):
        return self.end_fluxion() - self.now
