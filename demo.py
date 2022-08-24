from demo_func import *
from datetime import timedelta

video_uri = "gs://cloud-samples-data/video/JaneGoodall.mp4"
# mode = vi.LabelDetectionMode.SHOT_MODE
# segment = vi.VideoSegment(
#     start_time_offset=timedelta(seconds=0),
#     end_time_offset=timedelta(seconds=37),
# )
#
# results = detect_shot_changes(video_uri)
# print_video_shots(results)
#
# results = detect_labels(video_uri, mode, [segment])
# print_video_labels(results)
# print_shot_labels(results)

language_code = "en-GB"
segment = vi.VideoSegment(
    start_time_offset=timedelta(seconds=55),
    end_time_offset=timedelta(seconds=80),
)

results = transcribe_speech(video_uri, language_code, [segment])
print_video_speech(results)
print_word_timestamps(results)
