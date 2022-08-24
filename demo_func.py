from google.cloud import videointelligence_v1 as vi
from typing import Optional, Sequence


def detect_shot_changes(video_uri: str) -> vi.VideoAnnotationResults:
    video_client = vi.VideoIntelligenceServiceClient()
    features = [vi.Feature.SHOT_CHANGE_DETECTION]
    request = vi.AnnotateVideoRequest(input_uri=video_uri, features=features)

    print(f'Processing video: "{video_uri}"...')
    operation = video_client.annotate_video(request)

    return operation.result().annotation_results[0]  # Single video


def print_video_shots(results: vi.VideoAnnotationResults):
    shots = results.shot_annotations
    print(f" Video shots: {len(shots)} ".center(40, "-"))
    for i, shot in enumerate(shots):
        t1 = shot.start_time_offset.total_seconds()
        t2 = shot.end_time_offset.total_seconds()
        print(f"{i+1:>3} | {t1:7.3f} | {t2:7.3f}")


def detect_labels(
        video_uri: str,
        mode: vi.LabelDetectionMode,
        segments: Optional[Sequence[vi.VideoSegment]] = None,
) -> vi.VideoAnnotationResults:
    video_client = vi.VideoIntelligenceServiceClient()
    features = [vi.Feature.LABEL_DETECTION]
    config = vi.LabelDetectionConfig(label_detection_mode=mode)
    context = vi.VideoContext(segments=segments, label_detection_config=config)
    request = vi.AnnotateVideoRequest(
        input_uri=video_uri,
        features=features,
        video_context=context,
    )

    print(f'Processing video "{video_uri}"...')
    operation = video_client.annotate_video(request)

    return operation.result().annotation_results[0]  # Single video


def print_video_labels(results: vi.VideoAnnotationResults):
    labels = results.segment_label_annotations
    sort_by_first_segment_confidence(labels)

    print(f" Video labels: {len(labels)} ".center(80, "-"))
    for label in labels:
        categories = category_entities_to_str(label.category_entities)
        for segment in label.segments:
            confidence = segment.confidence
            t1 = segment.segment.start_time_offset.total_seconds()
            t2 = segment.segment.end_time_offset.total_seconds()
            print(
                f"{confidence:4.0%}",
                f"{t1:7.3f}",
                f"{t2:7.3f}",
                f"{label.entity.description}{categories}",
                sep=" | ",
            )


def sort_by_first_segment_confidence(labels: Sequence[vi.LabelAnnotation]):
    labels.sort(key=lambda label: label.segments[0].confidence, reverse=True)


def category_entities_to_str(category_entities: Sequence[vi.Entity]) -> str:
    if not category_entities:
        return ""
    entities = ", ".join([e.description for e in category_entities])
    return f" ({entities})"


def print_shot_labels(results: vi.VideoAnnotationResults):
    labels = results.shot_label_annotations
    sort_by_first_segment_start_and_confidence(labels)

    print(f" Shot labels: {len(labels)} ".center(80, "-"))
    for label in labels:
        categories = category_entities_to_str(label.category_entities)
        print(f"{label.entity.description}{categories}")
        for segment in label.segments:
            confidence = segment.confidence
            t1 = segment.segment.start_time_offset.total_seconds()
            t2 = segment.segment.end_time_offset.total_seconds()
            print(f"{confidence:4.0%} | {t1:7.3f} | {t2:7.3f}")


def sort_by_first_segment_start_and_confidence(labels: Sequence[vi.LabelAnnotation]):
    def first_segment_start_and_confidence(label):
        first_segment = label.segments[0]
        ms = first_segment.segment.start_time_offset.ToMilliseconds()
        return (ms, -first_segment.confidence)

    labels.sort(key=first_segment_start_and_confidence)

'''
---
'''


def transcribe_speech(
        video_uri: str,
        language_code: str,
        segments: Optional[Sequence[vi.VideoSegment]] = None,
) -> vi.VideoAnnotationResults:
    video_client = vi.VideoIntelligenceServiceClient()
    features = [vi.Feature.SPEECH_TRANSCRIPTION]
    config = vi.SpeechTranscriptionConfig(
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    context = vi.VideoContext(
        segments=segments,
        speech_transcription_config=config,
    )
    request = vi.AnnotateVideoRequest(
        input_uri=video_uri,
        features=features,
        video_context=context,
    )

    print(f'Processing video "{video_uri}"...')
    operation = video_client.annotate_video(request)

    return operation.result().annotation_results[0]  # Single video


def print_video_speech(results: vi.VideoAnnotationResults, min_confidence: float = 0.8):
    def keep_transcription(transcription: vi.SpeechTranscription) -> bool:
        return min_confidence <= transcription.alternatives[0].confidence

    transcriptions = results.speech_transcriptions
    transcriptions = [t for t in transcriptions if keep_transcription(t)]

    print(f" Speech Transcriptions: {len(transcriptions)} ".center(80, "-"))
    for transcription in transcriptions:
        first_alternative = transcription.alternatives[0]
        confidence = first_alternative.confidence
        transcript = first_alternative.transcript
        print(f" {confidence:4.0%} | {transcript.strip()}")


def print_word_timestamps(
        results: vi.VideoAnnotationResults, min_confidence: float = 0.8
):
    def keep_transcription(transcription: vi.SpeechTranscription) -> bool:
        return min_confidence <= transcription.alternatives[0].confidence

    transcriptions = results.speech_transcriptions
    transcriptions = [t for t in transcriptions if keep_transcription(t)]

    print(" Word Timestamps ".center(80, "-"))
    for transcription in transcriptions:
        first_alternative = transcription.alternatives[0]
        confidence = first_alternative.confidence
        for word in first_alternative.words:
            t1 = word.start_time.total_seconds()
            t2 = word.end_time.total_seconds()
            word = word.word
            print(f"{confidence:4.0%} | {t1:7.3f} | {t2:7.3f} | {word}")