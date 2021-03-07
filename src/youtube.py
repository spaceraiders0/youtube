#!/usr/bin/env python

"""This is the main file that controls everything about the project.
"""

import sys
import clipboard
import constants
import definitions
from argparse import ArgumentParser
import youtubesearchpython as YTS

search = {
    "video": YTS.VideosSearch,
    "channel": YTS.ChannelsSearch,
    "playlist": YTS.PlaylistsSearch,
}
info = {
    "video": (YTS.Video.get, definitions.video_info)
}

yt_parser = ArgumentParser(description="""A project to easily search for, and
                           download videos from youtube""")
yt_parser.add_argument("action", help="""the action to take (i.e search,
                       download, etc)""")
yt_parser.add_argument("query", help="arguments for the action.", nargs="*")
yt_parser.add_argument("-f", "--fields", help="""specifies th fields to get from
                       the video.""", metavar="fs")
yt_parser.add_argument("-L", "--limit", help="the number of videos to find.",
                       metavar="L", default=5)
yt_parser.add_argument("-l", "--lang", help="filters the language.",
                       metavar="l", default="en")
yt_parser.add_argument("-r", "--region", help="filters the region.",
                       metavar="r", default="US")
yt_parser.add_argument("-m", "--no-menu", help="""disables selection of results.
                       displays in the console instead""", action="store_true")
yt_parser.add_argument("-c", "--clipboard", help="""store links in the clipboard.
                       requires the xclip package on Linux.""",
                       action="store_true")
youtube_args = yt_parser.parse_args()
action = youtube_args.action.lower()

# Make sure there are not too many arguments passed.
try:
    action_arg_count = constants.ACTION_ARGS[action]
    given_arg_count = len(youtube_args.query)

    if action_arg_count not in [-1, given_arg_count]:
        print(f"'{action}' takes {action_arg_count} arguments. You gave {given_arg_count}.")
        sys.exit(1)
except KeyError:
    print(f"{action} is not an action.")

if action == "search":
    search_type, search_query = youtube_args.query
    search_type = search_type.lower()

    try:
        search_function = search[search_type]
        limit = int(youtube_args.limit)
        language = youtube_args.lang
        region = youtube_args.region
        results = search_function(search_query, limit=limit, language=language,
                                  region=region).result()["result"]

        _, selected_results = definitions.select(results, ">>>: ",
                                                 definitions.search_format())

        # Copy the links to the clipboard.
        if youtube_args.clipboard is True:
            links = " ".join(info["link"] for info in selected_results)
            clipboard.copy(links)
    except KeyError:
        print(f"{search_type} is not a valid search option.")
    except ValueError as e:
        print(e)

elif action == "info":
    pass

