import functools
import typing
from moviepy.editor import *

clip = VideoFileClip("media/sauls_gone.mp4", has_mask=True)
duration = clip.duration
w, h = clip.size

opinions = [
    "\"hey check out this cool discord bot\ni made\"",
    "[[ insert text here ]]",
    "manjaro linux users explaining why\nthey don't use arch linux instead",
    "\"ok\"",
    "rustaceans telling me python is slow for\nthe sixty quintillionth time",
    "my chemistry teacher begging me not\nto drink tetraethyl lead\n(i'm about to go vroom vroom)",
    "\"a monad is a monoid in\nthe category of endofunctors\"",
    "my \"therapist\" telling me\ni have schizophrenia\n(she's a skinwalker)",
    "furries telling me i'm a bad person\n(i burnt their house down)",
    "average systemd fan", "average initd enjoyer",
    "the 12 gauge barrel entering my mouth\n(it fits perfectly)",
    "average beatles fan", "average math rock enjoyer",
    "average color theory fan", "average music theory enjoyer",
    "average /g/ fan", "average /sci/ enjoyer", "\"AJR is the worst band\"",
    "\"МОНГОЛ УЛСЫН VНДСЭН ХУУЛЬ\"", "\"Танцевать and Судно are\noverrated\"",
    "Free Space",
    "i'm stuck in the body of a new mexican\nlawyer\n(my pleas for help are falling on deaf ears)",
    "the family of the \"man\" i euthanized telling me\ni'm the spawn of the devil",
    "average calculus fan", "average algebraic topology enjoyer",
    "average imperative programming fan",
    "average functional programming enjoyer",
    "i have discovered a truly marvelous\nproof of this, which this margin\nis too narrow to contain.",
    "dwm supremacy",
    "Traceback (most recent call last):\n  File \"_.py\", line 1, in <module>\nTypeError: you suck at programming",
    """main = readLn >>= print . (\\x -> x*x*x)""",
    "me when it rains for the seventy\nfemtillionth time in summer",
    "changed fans explaining why a game about\nbeing vored by latex furries is\nthe epitome of game development",
    "gnome users explaining how they tolerate\n internal scuffles over a file\npicker for the 60 gazillionth time",
    """108.88.178.226\n6056 Flowering Plum Ave,\nLas Vegas, NV 89142""",
    "fiddle simps telling me that what she\ndid is acceptable\n(i don't care)",
    "i'm all out of shitty opinions gg"
]

text_config = {"font": "Impact", "font_size": 27, "bg_color": "white"}


def compile_text(tokens: typing.List[str]):

    def _offset(clips: typing.List[TextClip]):
        t = 0
        for clip in clips:
            yield clip.with_start(t).with_duration(duration / len(opinions))
            t += duration / len(opinions)

    return _offset(
        map(
            lambda tok: TextClip(tok,
                                 duration=duration / len(opinions),
                                 size=(w, 125),
                                 **text_config).with_position(("center")),
            tokens))


# print(clip.with_start)
text = CompositeVideoClip([*compile_text(opinions)], bg_color=(255, 255, 255))

audio = AudioFileClip("./media/perfect_girl.mp3")

color_clip = ColorClip((w, h + 125), (255, 255, 255))

caption = CompositeVideoClip([color_clip, text])

composite = CompositeVideoClip([caption, clip.with_position(("bottom"))])
composite.audio = CompositeAudioClip([audio]).with_duration(duration)
composite.duration = duration
composite.write_videofile("the_fog_is_coming.mp4", 30)
composite.write_gif("the_fog_is_coming.gif", 30)
composite.close()
