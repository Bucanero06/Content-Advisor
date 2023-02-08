# -*- coding: utf-8 -*-
# todo - suggestions of better context for the question
# todo - use pretrained models for a more robust solution both for the embeddings and the completions
# todo - move from script to a web app

import openai
import whisper
import pandas as pd
from pytube import YouTube
from getpass import getpass
from openai.embeddings_utils import get_embedding
from helper_functions import ask_question, is_part_of_question, combine_episodes

pd.set_option('display.max_columns', None)

pre_context_prompt = "Answer the following question using only the context below. Answer in the style of Ben Carlson a financial advisor and podcaster. If you don't know the answer for certain, say I don't know."
question = "Should I buy a house with cash?"

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDINGS_MODEL = "text-embedding-ada-002"
SKIP_TRAINING = False
ASK_QUESTION = False
#
SKIP_DOWNLOAD_AND_TRANSCRIBE = False
SKIP_EMBEDDINGS = False

if SKIP_EMBEDDINGS: SKIP_DOWNLOAD_AND_TRANSCRIBE = True  # ungainly

# Check which values for skip are valid and set the correct values
# openai.api_key = getpass("Enter your OpenAI API Key")
openai.api_key = "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"
df = pd.read_csv('questions.csv')
print(f'{df = }')

# Set names for dirs and file locations
INPUT_DIR_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS = 'episodes_w_context_n_embedding'
PREFIX_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS = 'question_w_context_n_embedding'
OUTPUT_FILE_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS = 'questions_w_context_n_embedding.csv'
#
INPUT_DIR_FOR_EPISODES_WITH_CONTEXT = 'episodes_w_context'
PREFIX_FOR_EPISODES_WITH_CONTEXT = 'question_w_context'
OUTPUT_FILE_FOR_EPISODES_WITH_CONTEXT = 'questions_w_context.csv'
#
TEMP_DIR_FOR_TRANSCRIPTION = 'transcription'
TEMP_PREFIX_FOR_TRANSCRIPTION = 'transcription'


# Let's just get the questions for a single episode and make this work before we download and transcribe all episodes in bulk
def get_question_context(row):
    global transcription_output

    question_segments = list(
        filter(lambda segment: is_part_of_question(segment, row['start'], row['end']),
               transcription_output['segments']))
    # include question from timestamp in the context
    context = row['question']
    for segment in question_segments:
        context += segment['text']

    return context


# Read in all the episodes with context and embeddings and save to a single csv file for training the model on


if not SKIP_TRAINING:
    for episode in df['episode'].unique()[:1]:
        print(f'{episode = }')

        if not SKIP_DOWNLOAD_AND_TRANSCRIBE:
            # Get rows for episode
            episode_df = df[df['episode'] == episode].copy()
            print(f'{episode_df = }')

            # Download audio from YouTube for episode
            # ['_age_restricted', '_author', '_embed_html', '_fmt_streams', '_initial_data', '_js', '_js_url', '_metadata',
            # '_player_config_args', '_publish_date', '_title', '_vid_info', '_watch_html', 'age_restricted',
            # 'allow_oauth_cache', 'author', 'bypass_age_gate', 'caption_tracks', 'captions', 'channel_id', 'channel_url',
            # 'check_availability', 'description', 'embed_html', 'embed_url', 'fmt_streams', 'from_id', 'initial_data', 'js',
            # 'js_url', 'keywords', 'length', 'metadata', 'publish_date', 'rating', 'register_on_complete_callback',
            # 'register_on_progress_callback', 'stream_monostate', 'streaming_data', 'streams', 'thumbnail_url', 'title',
            # 'use_oauth', 'vid_info', 'video_id', 'views', 'watch_html', 'watch_url']
            youtube_video_url = episode_df['url'].iloc[0]  # assume all urls are the same for the episode
            youtube_video = YouTube(youtube_video_url)
            stream = youtube_video.streams.filter(only_audio=True).first()
            stream.download(filename=f'{TEMP_PREFIX_FOR_TRANSCRIPTION}_{episode}.mp4')
            print(f'{youtube_video.description = }')

            # Transcribe audio
            print("Transcribing audio...")
            model = whisper.load_model('base')
            transcription_output = model.transcribe(f'{TEMP_PREFIX_FOR_TRANSCRIPTION}_{episode}.mp4')
            print(f"{transcription_output['text'] = }")

            # Get context for each question
            print("Getting question context...")
            episode_df['context'] = episode_df.apply(get_question_context, axis=1)
            episode_df.to_csv(f'{INPUT_DIR_FOR_EPISODES_WITH_CONTEXT}/{PREFIX_FOR_EPISODES_WITH_CONTEXT}_{episode}.csv')
        else:
            # Read in the episode with context
            episode_df = pd.read_csv(
                f'{INPUT_DIR_FOR_EPISODES_WITH_CONTEXT}/{PREFIX_FOR_EPISODES_WITH_CONTEXT}_{episode}.csv')

        if not SKIP_EMBEDDINGS:
            # Get embeddings for each question
            episode_df['embedding'] = episode_df['context'].apply(
                lambda row: get_embedding(row, engine=EMBEDDINGS_MODEL))
            episode_df.to_csv(
                f'{INPUT_DIR_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS}/{PREFIX_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS}_{episode}.csv')
        else:
            # Read in the episode with context and embeddings
            episode_df = pd.read_csv(
                f'{INPUT_DIR_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS}/{PREFIX_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS}_{episode}.csv')

    # Delete the audio file
    try:
        import os

        os.remove('temp_financial_advisor.mp4')
    except:
        pass

    # combine all the episodes into a single csv file questions_w_context_n_embedding.csv
    combine_episodes(
        input_dir=INPUT_DIR_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS,
        prefix=PREFIX_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS,
        output_file=OUTPUT_FILE_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS)
else:
    episode_df = pd.read_csv(OUTPUT_FILE_FOR_EPISODES_WITH_CONTEXT_AND_EMBEDDINGS)

if ASK_QUESTION:
    ask_question(episode_df=episode_df, pre_context_prompt=pre_context_prompt, question=question,
                 completion_model=COMPLETIONS_MODEL,
                 embedding_model=EMBEDDINGS_MODEL,
                 temperature=1,
                 max_tokens=500,
                 top_p=1,
                 frequency_penalty=0,
                 presence_penalty=0,
                 )
