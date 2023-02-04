from io import BytesIO
from typing import Iterable
from typing import Union
import fastf1
from fastf1 import plotting
from fastf1.core import Laps
from fastf1.core import Session

from mikbot.f1 import plotting_utils

plotting.setup_mpl()
fastf1.Cache.enable_cache('fastf1-cache')


def lap_times(year: int, gp: Union[int, str], drivers: Iterable[str]) -> BytesIO:
    session: Session = fastf1.get_session(year, gp, 'RACE')
    session.load()
    laps: list[Laps] = [session.laps.pick_driver(driver) for driver in drivers]
    data = [
        (driver['LapNumber'], driver['LapTime'], driver.iloc[0]['Driver'])
        for driver in laps
    ]
    unique_drivers = {lap.iloc[0]['Driver'] for lap in laps}
    title = f'{session.event.EventName} ({", ".join(unique_drivers)})'
    fig, ax = plotting_utils.create_plot(data, title, 'lap', 'time')
    return plotting_utils.fig_to_file(fig)
