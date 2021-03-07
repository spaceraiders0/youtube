"""This file contains important definitions like selecting from a list of
directories.
"""

import os
import re
import sys
import constants


def clear() -> None:
    """Clears the screen in a platform-independant way.
    """

    try:
        clear_command = constants.clear_commands[sys.platform]
        os.system(clear_command)
    except KeyError:
        print(f"Could not run clear command. Wrong platform. ({sys.platform})")


def index_collect(source: list, range_format: str) -> set:
    """Retrieves indexes from strings in a way that allows for ranges,
    and selecting multiple. These are not guaranteed to be valid indexes.
    It should also be noted that ranges work identically to Python's list
    slicing. A range of 1-4 will start at 1, and stop before reaching four.
    You will end up with a set of {1, 2, 3}, instead of {1, 2, 3, 4}

    Formats:
    All Options: -
    Options A-Z: A-Z
    All Options After Z: Z-
    All Options Before Z: -Z
    Specific Options: A, B, C, D

    These are free to be mixed and matched, but do note that an index will
    never show up more than once, due to them being stored in a set.

    :param source: the place where indexes are retrieved
    :type source: list
    :param range_format: the string to generate indexes from
    :type range_format: str
    :return: the indexes collected
    :rtype: set
    """

    specifiers = re.split(constants.INDEXES, re.sub("\s*", "", range_format))
    indexes = set()

    if range_format == "" or specifiers == [""]:
        return indexes

    # Collect all valid index specifiers
    for spec in specifiers:
        delimiter_count = spec.count(constants.RANGE_DELIMITER)

        if delimiter_count == 0:  # Regular Index
            indexes.add(int(spec))
        elif delimiter_count == 1:  # Range
            delimiter_index = spec.find(constants.RANGE_DELIMITER)
            start, stop = spec[:delimiter_index], spec[delimiter_index + 1:]

            if len(start) == 0 and len(stop) == 0:  # All options
                start = 0
                stop = len(source)
            elif len(start) == 0:  # All before N
                start = 0
                stop = int(stop)
            elif len(stop) == 0:  # All after N
                start = int(start)
                stop = len(source)

            indexes.update(range(int(start), int(stop)))
        else:                       # Too many delimiters
            raise ValueError(f"Ranges must only have one delimiter. {spec}")

    return indexes


def select(options: list, prompt: str = ">>>: ",
           option_format: callable = lambda o: o) -> [set, list]:
    """Selects a single option out of a possible list. Allows for the mixing,
    and matching of range syntax.

    :param options: the options to select from
    :type options: list
    :param prompt: the prompt that will be given for input
    :type prompt: str, defaults to '>>>: '
    :param option_format: how the option should be displayed
    :type option_format: callable, defaults to lambda o: o
    :return: the indexes selected, and the values selected.
    :rtype: set, list
    """

    while True:
        clear()

        # Padding options so it looks cleaner.
        largest_number: str = len(str(len(options) - 1))

        for index in range(len(options)):
            justified_number = str(index).rjust(largest_number)
            print(f"{justified_number}: {option_format(options[index])}")

        try:
            indexes = index_collect(options, input(prompt))

            return [indexes, [options[index] for index in indexes]]
        except (ValueError, IndexError):
            continue


def video_info(video: dict) -> dict:
    """Extracts the data from a video dictionary and simplifies it.
    """

    info = {}

    info["id"] = video["id"]
    info["link"] = video["link"]
    info["views"] = int(video["viewCount"]["text"])
    info["title"] = video["title"]
    info["keywords"] = video["keywords"]
    info["channel_name"] = video["channel"]["name"]
    info["channel_id"] = video["channel"]["id"]
    info["channel_link"] = video["channel"]["link"]
    info["publish_date"] = video["publishDate"]
    info["upload_date"] = video["uploadDate"]
    info["average_rating"] = int(video["averageRating"])
    info["description"] = video["description"]

    suffix = 1

    for thumbnail_dict in video["thumbnails"]:
        info[f"url_x{suffix}"] = thumbnail_dict["url"]
        info[f"url_x{suffix}"] = thumbnail_dict["url"]
        info[f"width_x{suffix}"] = thumbnail_dict["width"]
        info[f"height_x{suffix}"] = thumbnail_dict["height"]

        suffix += 1

    return info


def search_format() -> callable:
    """Returns the formatter for the video's information.

    :return: the string formatter
    :rtype: callable
    """
    
    return lambda o: f"{o['channel']['name']} - {o['title']}"
