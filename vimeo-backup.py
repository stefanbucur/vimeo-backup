#!/usr/bin/env python
#
# Copyright 2015 Stefan Bucur.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import json
import os
import subprocess

from dateutil import parser
import vimeo

v = vimeo.VimeoClient(
    token=os.environ["VIMEO_BEARER_TOKEN"],
    key=os.environ["VIMEO_API_TOKEN"],
    secret=os.environ["VIMEO_API_TOKEN_SECRET"])

next_videos_page_url = "/me/videos"

while next_videos_page_url:
    videos = v.get(next_videos_page_url).json()

    for video in videos['data']:
        video_name = "%s %s.mp4" % (parser.parse(video['created_time']).strftime('%Y-%m-%d'), video['name'])
        video_name = video_name.replace("/", "-")

        if os.path.isfile(video_name):
            print video_name, "already downloaded, skipping..."
            continue

        print "Attempting to download", video_name
        download_link = None
        if 'download' in video:
            available_downloads = {d['quality']: d for d in video['download']}
            for quality in ['original', 'hd', 'sd']:
                if quality in available_downloads:
                    download_link = available_downloads[quality]['link']
                    break

        if not download_link:
            print "Download link unavailable, skipping..."
            continue

        print "Found", quality, "quality at", download_link
        subprocess.call(["wget", "-O", video_name, download_link])
            
        print "="*80

    next_videos_page_url = videos['paging']['next']
