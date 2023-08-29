from youtube_transcript_api import YouTubeTranscriptApi

def merge_chunks(data):
    merged_data = []

    for i in range(0, len(data), 5):
        chunk = data[i:i+5]

        # calculate the start time and duration for the merged chunk
        start_time = chunk[0]['start']
        end_time = chunk[-1]['start'] + chunk[-1]['duration']
        duration = end_time - start_time

        # merge the text of all items in the chunk
        text = ' '.join([item['text'] for item in chunk])

        merged_data.append({
            'duration': duration,
            'start': start_time,
            'text': text
        })
    return merged_data

def ingest_cc(video_id):
    cc = YouTubeTranscriptApi.get_transcript(video_id)
    merged_cc = merge_chunks(cc)