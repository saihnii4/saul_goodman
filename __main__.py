import argparse
import os.path
import sys
import time
import traceback
import typing

from colorama import init
from moviepy.editor import *
from termcolor import colored

TEXT_CONFIG = {"font": "Impact", "font_size": 27, "bg_color": "white"}

OPINIONS = ["kill", "me"]

parser = argparse.ArgumentParser(description="It's Showtime!")
parser.add_argument(
    "-g", "-gif", "--gif", default=False, help="Generates a gif", action="store_true"
)

parser.add_argument(
    "-m", "-mov", "--mov", help="Generates video", default=False, action="store_true"
)

parser.add_argument(
    "-out", "--out", help="File destination", default="out/%d.mp4" % (time.time())
)

parser.add_argument(
    "-source" "--source",
    help="Sets source material for overlay (default: media/sauls_gone.mp4)",
    default="media/sauls_gone.mp4",
)

parser.add_argument("-fps", "--fps", help="Sets frame rate for video", default=60)

parser.add_argument(
    "-f",
    "-format",
    "--format",
    "-codec",
    "--codec",
    help="Sets encoding for video (default: libx264)",
    default="libx264",
)

parser.add_argument(
    "-a", "--audio", help="Sets audio source material", default="media/perfect_girl.mp3"
)

args = parser.parse_args()


def main():
    init()

    def compile_text(tokens: typing.List[str]):
        def _offset(clips: typing.List[TextClip]):
            t = 0
            for clip in clips:
                yield clip.with_start(t).with_duration(duration / len(OPINIONS))
                t += duration / len(OPINIONS)

        return _offset(
            map(
                lambda tok: TextClip(
                    tok, duration=duration / len(OPINIONS), size=(w, 125), **TEXT_CONFIG
                ).with_position(("center")),
                tokens,
            )
        )

    clip = VideoFileClip("media/sauls_gone.mp4", has_mask=True)
    duration = clip.duration
    w, h = clip.size

    try:
        text = CompositeVideoClip([*compile_text(OPINIONS)], bg_color=(255, 255, 255))
    except IndexError:
        print(
            colored(
                "You haven't entered your opinions yet. Doublecheck __main__.py and try again",
                "red",
            )
        )
        print("Original traceback:")
        print(traceback.format_exc())
        sys.exit(1)

    audio = AudioFileClip(args.audio)
    color_clip = ColorClip((w, h + 125), (255, 255, 255))
    caption = CompositeVideoClip([color_clip, text])

    composite = CompositeVideoClip([caption, clip.with_position(("bottom"))])
    composite.audio = CompositeAudioClip([audio]).with_duration(duration)
    composite.duration = duration

    if args.mov:
        composite.write_videofile(args.out, 30, codec=args.format)

    if args.gif:
        composite.write_gif("".join(os.path.splitext(args.out)[:-1]) + ".gif", 30)

    print(colored("Program has finished execution, if nothing happened, double-check your arguments", "green"))

    composite.close()

if __name__ == "__main__":
    main()
