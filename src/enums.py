import enum


class ProjCat(enum.IntEnum):
    normal = 10
    explaination = 20
    story = 30


class Dep(enum.IntEnum):
    d30 = 30
    d40 = 40
    d51 = 51
    d52 = 52
    d59 = 59
    d60 = 60
    d71 = 71
    d72 = 72
    d73 = 73


class LeafState(enum.IntEnum):
    droped_e = -93
    droped_f = -92
    droped_m = -91
    delayed = -80
    waiting = -10
    finished = 0
    normal = 10
    paused_fin = 21
    paused_tmp = 22


class MangoType(enum.IntEnum):
    unknown = -10
    text = 20
    audio_flac = 51
    audio_wav = 52
    picture_png = 61
    picture_jpg = 62
    video_mp4 = 71
    video_mkv = 72


class ProgressState(enum.IntEnum):
    s0 = 0
    s5 = 50
    s7_1 = 71
    s7_2 = 72
    s7_3 = 73
