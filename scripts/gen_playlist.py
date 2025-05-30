#!/usr/bin/env python3

import json
import yt_dlp
import sys

INPUT_FILE = "songs.txt"
OUTPUT_FILE = "results.json"

def search_youtube(query):
    ydl_opts = {
        'skip_download': True,
        'default_search': 'ytsearch',
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in info and info['entries']:
                return info['entries'][0]['id']
        except Exception as e:
            print(f"Error searching for {query}: {e}")
    return None

def parse_line(line):
    if ' - ' not in line:
        return None, None
    artist, title = line.strip().split(' - ', 1)
    return artist.strip(), title.strip()

def main():
    output = []

    with open(INPUT_FILE, 'r', encoding='utf-8') as file:
        for line in file:
            artist, title = parse_line(line)
            if not title:
                continue

            query = f"{title} {artist}" if artist else title
            print(f"Searching for: {query}")
            video_id = search_youtube(query)

            if video_id:
                entry = {
                    "id": video_id,
                    "answerTime": 30,
                    "artist": artist,
                    "from": 0,
                    "origin": "",
                    "time": 30,
                    "title": title
                }
                output.append(entry)
            else:
                print(f"No video found for: {query}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(output, out_file, indent=2, ensure_ascii=False)
        print(f"\nOutput written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

