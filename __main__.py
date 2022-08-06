import functools
import typing
from moviepy.editor import *

clip = VideoFileClip("media/sauls_gone.mp4", has_mask=True)
duration = clip.duration
w, h = clip.size

opinions = [
    # this is where your scathing takes go to die
]

text_config = {"font": "Impact", "font_size": 27, "bg_color": "white"}


def compile_text(tokens: typing.List[str]):
    def _offset(clips: typing.List[TextClip]):
        t = 0
        for clip in clips:
            yield clip.with_start(t).with_duration(duration /
                                                   len(opinions))
            t += duration / len(opinions)

    return _offset(
        map(
            lambda tok: TextClip(
                tok,
                duration=duration / len(opinions),
                size=(w, 125),
                **text_config).with_position(("center")), tokens))


# print(clip.with_start)
text = CompositeVideoClip([*compile_text(opinions)],
                          bg_color=(255, 255, 255))

audio = AudioFileClip("./media/perfect_girl.mp3")

color_clip = ColorClip((w, h + 125), (255, 255, 255))

caption = CompositeVideoClip([color_clip, text])

composite = CompositeVideoClip([caption, clip.with_position(("bottom"))])
composite.audio = CompositeAudioClip([audio]).with_duration(duration)
composite.duration = duration
composite.write_videofile("the_fog_is_coming.mp4", 30)
composite.write_gif("the_fog_is_coming.gif", 30)
composite.close()
