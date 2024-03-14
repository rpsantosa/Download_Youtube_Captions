import pytube
import os

url = #youtube url
DATA_YOUTUBE = # Directory to download both video and captions

def extract_text(json_data):
    """Extracts the transcribed text from the JSON data.

    Args:
        json_data (dict): The JSON data structure.

    Returns:
        str: The concatenated transcribed text.
    """

    text = ""
    for event in json_data['events']:
        if 'segs' in event:
            for segment in event['segs']:
                text += segment['utf8'] + " "  # Add a space after each word

    return text.strip()  # Remove any trailing spaces

def download_video_and_transcript(youtube_url, output_path=DATA_YOUTUBE):
    """Downloads video and transcripts from a YouTube URL to a specified directory.

    Args:
        youtube_url (str): The URL of the YouTube video.
        output_path (str, optional): The path to the directory where the files will be saved. 
                                     Defaults to "path/to/mydata".
    """

    try:
        youtube = pytube.YouTube(youtube_url)

        # Create the output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        # Download the video
        video = youtube.streams.get_highest_resolution()
        print(f"Downloading video: '{youtube.title}'")
        video_filepath = video.download(output_path=output_path)
        print("Video download complete!")

        # Download transcripts (if available)
        try:
            captions = youtube.captions['a.pt'] 
            if captions:
                # captions_text = captions.generate_srt_captions()
                # print("Captions download complete!")

                # # Save captions to a file
                # captions_filepath = os.path.join(output_path, f"{youtube.title}.srt")
                # with open(captions_filepath, "w", encoding="utf-8") as f:
                #     f.write(captions_text)
                caps = captions.json_captions
                json_data = extract_text(caps)
                text_file = os.path.join(DATA_YOUTUBE, 'captions_json_f.txt')
                with open(text_file, 'w') as f:
                        f.write(json_data) 
            else:
                print("No captions found for this video.")

        except Exception as e:
            print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# USAGE
# download_video_and_transcript(url)
