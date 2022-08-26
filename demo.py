from demo_func import *
from datetime import timedelta

# sample video
video_uri = "gs://cloud-samples-data/video/JaneGoodall.mp4"
mode = vi.LabelDetectionMode.SHOT_MODE
segment = vi.VideoSegment(
    start_time_offset=timedelta(seconds=0),
    end_time_offset=timedelta(seconds=37),
)

'''
Takes about 20s for video_shots, video_labels & shot_labels
'''

results = detect_labels(video_uri, mode, [segment])

# print number of shots
print_video_shots(results)

# print labels overall
print_video_labels(results)

# print labels per shot
print_shot_labels(results)


'''
Speech transcription takes about ~1m more.. disabled for demo purpose
'''

# language_code = "en-GB"
# segment = vi.VideoSegment(
#     start_time_offset=timedelta(seconds=55),
#     end_time_offset=timedelta(seconds=80),
# )
#
# results = transcribe_speech(video_uri, language_code, [segment])
# print_video_speech(results)
# print_word_timestamps(results)
