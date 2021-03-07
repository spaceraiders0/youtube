#!/usr/bin/env python

"""This is the main file that controls everything about the project.
"""

import definitions
from argparse import ArgumentParser
import youtubesearchpython as YTS

youtube_argparser = ArgumentParser(description="""A project to easily search
        for, and download videos from youtube""")
youtube_argparser.add_argument("action", help="the action to take (i.e search, download, etc)")
youtube_argparser.add_argument("subcommands", nargs="*",
                               help="extra information for an action. usually a query")
youtube_argparser.add_argument("-t", "--title", action="store_true",
                               help="shows the title ")
youtube_argparser.add_argument("-l", "--link", action="store_true",
                               help="shows the link ")
youtube_argparser.add_argument("-u", "--uploader", action="store_true",
                               help="shows the uploader ")
youtube_argparser.add_argument("-v", "--views", action="store_true",
                               help="shows the short-form views ")
youtube_argparser.add_argument("-i", "--image", action="store_true",
                               help="shows the thumbnail ")
youtube_argparser.add_argument("-T", "--time", action="store_true",
                               help="shows the published time ")
youtube_argparser.add_argument("-L", "--length", action="store_true",
                               help="shows the length ")
youtube_argparser.add_argument("-V", "--no-short", action="store_true",
                               help="Use long-form views instead of short-form")
youtube_argparser.add_argument("-m", "--no-menu", action="store_true",
                               help="disables selection of results. displays in the console instead")
youtube_args = youtube_argparser.parse_args()

print(YTS.Video.getInfo("https://www.youtube.com/watch?v=BaPoNErgdjM"))

#results = YTS.VideosSearch('NoCopyrightSounds', limit=2).result()["result"]
#
#for key, value in results[0].items():
#    print(key, value)

#definitions.select(results, option_format=lambda o: o["title"])

if youtube_args.action == "search":
    search_type, query = youtube_args.subcommands
elif youtube_args.action == "info":
    link_type = youtube_args.subcommands[0]
    link = youtube_args.subcommands[1]
    info_types = youtube_args.subcommands[2:]

    print(f"Getting {', '.join(info_types)} from {link_type} {link}")
