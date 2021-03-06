import datetime

import astropy.units as u
from sunpy.physics.differential_rotation import diff_rot

__all__ = ['MidnightRotation']


class MidnightRotation:
    """
    A class to rotate the coordinates of an observation
    to its coordinates at the nearest midnight.
    """
    def get_nearest_midnight(self, obsdate: str, fmt='%Y-%m-%d %H:%M:%S'):
        """
        For a given observation time and date, returns the datetime of the nearest midnight.

        Parameters
        ----------
        obsdate : str
            The observation time and date.
        fmt : str, optional
            The format in which obsdate is represented, by default '%Y-%m-%d %H:%M:%S'

        Returns
        -------
        nearest_midnight : datetime.datetime
            The datetime of the nearest midnight.

        Examples
        --------
        >>> from pythia.cleaning.midnight_rotation import MidnightRotation
        >>> midnight_rotation = MidnightRotation()
        >>> obsdate = '2000-01-01 12:47:02'
        >>> midnight_rotation.get_nearest_midnight(obsdate)
        datetime.datetime(2000, 1, 2, 0, 0)
        >>> obsdate = '2000-01-01 11:47:02'
        >>> midnight_rotation.get_nearest_midnight(obsdate)
        datetime.datetime(2000, 1, 1, 0, 0)
        """
        current = datetime.datetime.strptime(obsdate, fmt)
        if current.hour >= 12:
            current = current + datetime.timedelta(days=1)
        return current.replace(hour=0, minute=0, second=0, microsecond=0)

    def get_seconds_to_nearest_midnight(self, obsdate: str, fmt='%Y-%m-%d %H:%M:%S'):
        """
        For a given observation time and date, returns the seconds to the nearest midnight.

        Parameters
        ----------
        obsdate : str
            The observation time and date.
        fmt : str, optional
            The format in which obsdate is represented, by default '%Y-%m-%d %H:%M:%S'

        Returns
        -------
        seconds_to_nearest_midnight : int
            Returns the seconds to the nearest midnight.
            Returned seconds are negative if the nearest midnight is of the same day.

        Examples
        --------
        >>> from pythia.cleaning.midnight_rotation import MidnightRotation
        >>> midnight_rotation = MidnightRotation()
        >>> obsdate = '2000-01-01 12:47:02'
        >>> midnight_rotation.get_seconds_to_nearest_midnight(obsdate)
        40378.0
        >>> obsdate = '2000-01-01 11:47:02'
        >>> midnight_rotation.get_seconds_to_nearest_midnight(obsdate)
        -42422.0
        """
        timedifference = self.get_nearest_midnight(obsdate, fmt) - datetime.datetime.strptime(obsdate, fmt)
        return timedifference.total_seconds()

    def get_longitude_at_nearest_midnight(self, obsdate: str, latitude: u.deg,
                                          fmt='%Y-%m-%d %H:%M:%S', **kwargs):
        """
        Returns the Longitude at midnight, for a given Latitude and observation date.

        Parameters
        ----------
        obsdate : str
            The observation time and date.
        latitude : u.deg
            latitude of the observation
        fmt : str, optional
            The format in which obsdate is represented, by default '%Y-%m-%d %H:%M:%S'
        kwags : dict
            Keyword arguments passed to `~sunpy.physics.differential_rotation.diff_rot`

        Returns
        -------
        longitude : u.deg
            longitude of the observation at midnight.

        Examples
        --------
        >>> import astropy.units as u
        >>> from pythia.cleaning.midnight_rotation import MidnightRotation
        >>> midnight_rotation = MidnightRotation()
        >>> latitude = 443.92976 * u.deg
        >>> latitude
        <Quantity 443.92976 deg>
        >>> obsdate = '2000-01-01 12:47:02'
        >>> midnight_rotation.get_longitude_at_nearest_midnight(obsdate, latitude)
        <Longitude 4.87918286 deg>
        """
        seconds_to_midnight = self.get_seconds_to_nearest_midnight(obsdate, fmt=fmt) * u.s
        return diff_rot(seconds_to_midnight, latitude, **kwargs)
