#!/usr/bin/env python

"""This is the main file that controls everything about the project.
"""

import sys
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

youtube_argparser = ArgumentParser(description="""A project to easily search
        for, and download videos from youtube""")
youtube_argparser.add_argument("action", help="the action to take (i.e search, download, etc)")
youtube_argparser.add_argument("query", help="arguments for the action.", nargs="*")
youtube_argparser.add_argument("-f", "--fields", metavar="fs",
                               help="specifies the fields to get from the video.")
youtube_argparser.add_argument("-L", "--limit", metavar="L", help="the number of videos to find.",
                               default=5)
youtube_argparser.add_argument("-l", "--lang", metavar="l", help="filters the language.",
                               default="en")
youtube_argparser.add_argument("-r", "--region", metavar="r", help="filters the region.",
                               default="US")
youtube_argparser.add_argument("-m", "--no-menu", action="store_true",
                               help="disables selection of results. displays in the console instead")
youtube_argparser.add_argument("-c", "--clipboard",
                               help="""store output in the clipboard. requires the
                               xclip package on Linux.""",
                               action="store_true")
youtube_args = youtube_argparser.parse_args()
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
        limit, language, region, = int(youtube_args.limit), youtube_args.lang, youtube_args.region
        results = search_function(search_query, limit=limit, language=language,
                                  region=region).result()["result"]

        
        _, selected_results = definitions.select(results, ">>>: ",
                                                 definitions.search_format())

        for result in selected_results:
            print(result["link"])
    except KeyError:
        print(f"{search_type} is not a valid search option.")
    except ValueError as e:
        print(e)

elif action == "info":
    pass

