"""
Author BrainDead#6105

Qualifier description:
https://github.com/python-discord/code-jam-6-qualifier/tree/master/alternative-1-datetime-parsing

- Supports everything from basic and advanced requirements + ordinal dates.
- Decimal places are supported for h/m/s and precision is for all digits.
  For example 21.577 will be 21h 34m 37s and 200000ms
- Script does not check for mixing date formats (simple/extended)

"""


import re
import datetime
from typing import Tuple, Union, Any, List, Generator


DATE_VALUE_SEPARATOR = "-"
TIME_VALUE_SEPARATOR = ":"
DATE_TIME_SEPARATOR = "T"
DECIMAL_FRACTION = "."

# First tuple represents possible params to datetime and second represents it's allowed ranges
# (both ints are including). Dict not used to squeeze performance.
_allowed_time_name_arguments = ("hour", "minute", "second", "microsecond")
_time_name_arguments_ranges = ((0, 23), (0, 59), (0, 59), (0, 999999))


def parse_iso8601(timestamp: str, *, force_leading_zeroes: bool = True) -> datetime.datetime:
    """Parse an ISO-8601 formatted time stamp."""
    if type(timestamp) is not str:
        raise TypeError("Passed timestamp has to be a string.")
    elif not timestamp:
        raise ValueError("Passed timestamp has to be a non-empty string.")

    date, *time = timestamp.split(DATE_TIME_SEPARATOR)
    if not date:
        raise ValueError("Date part of timestamp cannot be empty.")
    elif len(time) > 1:
        raise ValueError("Too many times. Invalid format")

    year, month, day = parse_date(date, force_leading_zeroes=force_leading_zeroes)

    time = time[0] if time else None
    datetime_time_params = {}
    tz_info = None
    if time:
        # We have an extended date format aka <date>T<time>
        # <time> can have a possible timezone addition
        time, *timezone = re.split("([Z+-])", time, maxsplit=2)
        datetime_time_params = parse_time(time)

        if len(timezone) > 2:
            raise ValueError("Too many timezones. Invalid format.")
        elif timezone:
            tz_info = construct_tz_info(timezone)

    return datetime.datetime(year=year, month=month, day=day,
                             tzinfo=tz_info, **datetime_time_params)


def parse_date(date: str, *, force_leading_zeroes: bool = True) -> Tuple[int, int, int]:
    """

    Notes about skipping standard:
    ISO-8601 standard defines YYYY-MM as valid date but as the qualifier requires us to return a
    datetime.datetime object, which requires day as argument, that format is dropped.

    Thus supported date formats are:
    basic date format:          YYYYMMDD
    extended date format:       YYYY-MM-DD
    basic ordinal format:       YYYYDDD
    extended ordinal format:    YYYY-DDD

    :param date: string representing date in one of the supported formats.
    :param force_leading_zeroes: bool, default True. Only affects extended format and does not work
                                 for basic format.
                                 Standard defines that date values have to be padded with
                                 leading zeros, however for example converting day "02" or "2" is
                                 the same for Python. If this is set to True a ValueError is raised
                                 for "2" because it does not adhere to standard. False does not
                                 raise a value error.
    :return: tuple of 3 ints representing  year, month and day
    """
    date_value_separator_count = date.count(DATE_VALUE_SEPARATOR)

    if date_value_separator_count == 0:
        # We are dealing with one of the basic formats.
        if len(date) == 8:
            # Basic date format YYYYMMDD
            year_month_day = date[0:4], date[4:6], date[6:8]
            year, month, day = (int(date_value) for date_value in year_month_day)
        elif len(date) == 7:
            # Basic ordinal format YYYYDDD
            # Example "19810405" is also "1981095" as ordinal date
            year, ordinal_date = int(date[0:4]), date[4:7]
            month, day = _deal_with_ordinal_date(ordinal_date, _is_leap_year(year))
        else:
            raise ValueError("Invalid basic date format.")

    elif date_value_separator_count == 1:
        # We are dealing with extended ordinal format YYYY-DDD
        # Example "1981-04-05" is also "1981-095" as ordinal date
        year, ordinal_date = date.split(DATE_VALUE_SEPARATOR)
        if force_leading_zeroes:
            check_valid_ordinal_date(year, ordinal_date)
        year = int(year)
        month, day = _deal_with_ordinal_date(ordinal_date, _is_leap_year(year))

    elif date_value_separator_count == 2:
        # We are dealing with extended date format YYYY-MM-DD
        year, month, day = date.split(DATE_VALUE_SEPARATOR)
        if force_leading_zeroes:
            check_valid_date_arguments_lengths(year, month, day)

        year, month, day = int(year), int(month), int(day)
    else:
        raise ValueError("Too many date value separators passed. "
                         "Can't separate year, month and day apart.")

    return year, month, day


def _is_leap_year(year: int) -> bool:
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


def _deal_with_ordinal_date(ordinal_date: str, leap_year: bool) -> Tuple[int, int]:
    """
    Source: https://en.wikipedia.org/wiki/Ordinal_date
    :param ordinal_date: str representing ordinal date. Example "095" represents 4th month 5th day
    :param leap_year: bool representing is it a leap year or not.
    :return: tuple of 2 ints representing month and day that were converted from param ordinal_date
    """
    leap_year_i = 2 if leap_year else 3
    ordinal_date = int(ordinal_date)
    month = ordinal_date // 30 + 1
    day = ordinal_date % 30 + leap_year_i - int(0.6*(month + 1))
    if day < 0:
        days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if leap_year:
            days_per_month[1] += 1

        day = days_per_month[month] + day
        month -= 1

    return month, day


def check_valid_ordinal_date(year: str, ordinal_date: str):
    """
    Checks the length of passed params to adhere to standard.
    For example year has to be in YYYY format and will always be 4 characters.
    :param year: str that needs to have length 4
    :param ordinal_date: str that needs to have length 3
    :raise ValueError: if any of the string params don't have necessary length
    """
    _check_year_length(year)
    if len(ordinal_date) != 3:
        raise ValueError("Ordinal date has to have 3 chars in format DDD")


def check_valid_date_arguments_lengths(year: str, month: str, day: str):
    """
    Checks the length of passed params to adhere to standard.
    For example year has to be in YYYY format and will always be 4 characters.
    :param year: str that needs to have length 4
    :param month: str that needs to have length 2
    :param day: str that needs to have length 2
    :raise ValueError: if any of the string params don't have necessary length
    """
    _check_year_length(year)
    if len(month) != 2:
        raise ValueError("Date month has to have 2 chars in format MM")
    elif len(day) != 2:
        raise ValueError("Date day has to have 2 chars in format DD")


def _check_year_length(year: str):
    if len(year) != 4:
        raise ValueError("Date year has to have 4 chars in format YYYY")


def parse_time(time_timestamp: str, *,
               force_leading_zeroes: bool = True,
               allow_seconds: bool = True) -> dict:
    """
    Supported formats:

    Extended formats:
    hh:mm:ss.sss
    hh:mm:ss
    hh:mm

    Basic formats:
    hhmmss.ssss
    hhmmss
    hhmm
    hh

    Decimal fractions are supported for all (h/m/s).
    (fraction may only be added to the lowest order time element in the representation)

    :param time_timestamp: str representing time in one of the supported formats
    :param force_leading_zeroes: bool, default True. Only affects extended format and does not work
                                 for basic format.
                                 Standard defines that date values have to be padded with
                                 leading zeros, however for example converting day "02" or "2" is
                                 the same for Python. If this is set to True a ValueError is raised
                                 for "2" because it does not adhere to standard. False does not
                                 raise a value error.
    :param allow_seconds: bool, default True. Whether to allow parsing seconds.
                          For example standard does not allow seconds in timezone time.
                          If this is True and seconds are found it will raise ValueError
    :return:
    """
    time_value_separator_count = time_timestamp.count(TIME_VALUE_SEPARATOR)

    if time_value_separator_count == 0:
        # We are dealing with basic format.
        basic_format, *decimal = time_timestamp.split(DECIMAL_FRACTION)

        if len(decimal) > 1:
            raise ValueError("Too many decimals. Invalid format")
        decimal = float("." + decimal[0]) if decimal else None

        # Our supported formats are very specific
        if len(basic_format) not in (2, 4, 6):
            raise ValueError("Incorrectly formatted basic time format.")

        datetime_time_params = _construct_datetime_time_params_dict(get_chunks(basic_format, 2))

    elif time_value_separator_count in (1, 2):
        # We are dealing with extended format.
        time_timestamp, *decimal = time_timestamp.split(DECIMAL_FRACTION)

        if len(decimal) > 1:
            raise ValueError("Too many decimals. Invalid format")
        decimal = float("." + decimal[0]) if decimal else None

        time_timestamp = time_timestamp.split(TIME_VALUE_SEPARATOR)
        if force_leading_zeroes:
            _check_valid_time_values_length(time_timestamp)

        datetime_time_params = _construct_datetime_time_params_dict(time_timestamp)
    else:
        raise ValueError("Too many time value separators passed. "
                         "Can't separate hours, minutes and seconds apart.")

    if not allow_seconds and datetime_time_params.get("second", None) is not None:
        raise ValueError(f"Seconds are not allowed in timestamp {time_timestamp}")
    elif decimal:
        _deal_with_time_decimal(datetime_time_params, decimal)

    _check_valid_time_range(datetime_time_params)
    return datetime_time_params


def _construct_datetime_time_params_dict(
        to_iterate: Union[List[str], Generator[str, None, None]]) -> dict:
    """
    :param to_iterate: list or generator of strings. Strings represent times sorted
                       from hours to seconds. Not all elements have to be present for
                       example it can only contain one str representing hours.
                       Example input: ['21', '10', '31']
    :return: dict where keys are arguments are time names and values are it's values.
             Example: {'hour': 21, 'minute': 10, 'second': 31}
    """
    datetime_time_params = {}
    for index, time_chunk in enumerate(to_iterate):
        time_chunk = int(time_chunk)
        datetime_time_params[_allowed_time_name_arguments[index]] = time_chunk
    return datetime_time_params


def _check_valid_time_range(time_timestamp: dict):
    """
    Checks the length of passed params to adhere to standard.
    For example hour has to be in HH format and will always be 2 characters.
    :param time_timestamp: list of strings representing times going from hours -> minute -> second
                           Not all have to be present for example it can be just a list with one
                           element representing hours.
    :raise ValueError: if any of the strings in time_timestamp doesn't have length 2
    """
    for index, items in enumerate(time_timestamp.items()):
        min_including, max_including = _time_name_arguments_ranges[index]
        time_type, time_value = items
        if not min_including <= time_value <= max_including:
            raise ValueError(f"Invalid time for {time_type}")


def _check_valid_time_values_length(time_timestamp: List[str]):
    """
    Checks the length of passed params to adhere to standard.
    For example hour has to be in HH format and will always be 2 characters.
    :param time_timestamp: list of strings representing times going from hours -> minute -> second
                           Not all have to be present for example it can be just a list with one
                           element representing hours.
    :raise ValueError: if any of the strings in time_timestamp doesn't have length 2
    """
    for time_value, time_type in zip(time_timestamp, _allowed_time_name_arguments):
        if len(time_value) != 2:
            raise ValueError(f"Time {time_type} has to have 2 chars.")


def construct_tz_info(timezone: list) -> datetime.timezone:
    """
    :param timezone: list of either:
                     1: first element is sign + or -
                        second element is string representing time offset
                     2: first element is string "Z"
                        there is no second element aka offset (the timezone is utc)
    :return: datetime.timezone
    """
    tz_sign, tz_offset = timezone
    if tz_sign == "Z":
        return datetime.timezone.utc

    time_dict = parse_time(tz_offset, allow_seconds=False)
    # Our parse_time returns keys like hour, minute etc but for timedelta arguments we need plurals
    # like hours, minutes etc
    pluralized_time_dict = {name+"s": value for name, value in time_dict.items()}

    offset_multiplier = 1
    if tz_sign == "-":
        offset_multiplier = -1

    return datetime.timezone(offset_multiplier * datetime.timedelta(**pluralized_time_dict))


def get_chunks(iterable: Union[str, list, tuple], chunk_size: int) -> Any:
    """
    Helper generator function.
    :param iterable: Union[str, list, tuple] iterable to get elements from
    :param chunk_size: int, number of elements in yielded chunk
    :return: chunk from iterable containing chunk_size elements
    """
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i:i+chunk_size]


def _deal_with_time_decimal(time_dict: dict, decimal: float):
    """
    Example (this is derived from "2019-12-18T21.577"):
    time_dict is {'hour': 21}
    decimal is 0.5777

    This will modify time_dict so it looks like:
     {'hour': 21, 'minute': 34, 'second': 37, 'microsecond': 200000}
    """
    precision = 6
    if list(time_dict.keys())[-1] == "hour":
        minutes = 60 * decimal
        time_dict["minute"] = int(minutes)
        decimal_remainder = round(minutes % 1, precision)
    elif list(time_dict.keys())[-1] == "minute":
        seconds = 60 * decimal
        time_dict["second"] = int(seconds)
        decimal_remainder = round(seconds % 1, precision)
    elif list(time_dict.keys())[-1] == "second":
        microseconds = 10**6 * decimal
        time_dict["microsecond"] = int(microseconds)
        decimal_remainder = round(microseconds % 1, precision)
    else:
        decimal_remainder = 0

    if decimal_remainder != 0:
        _deal_with_time_decimal(time_dict, decimal_remainder)
