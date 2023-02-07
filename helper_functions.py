def preprocess_questions_naive(raw_file_name, output_file_name=None):
    """Data Manipulation for questions, for now specific to current sample"""
    if output_file_name is not None: assert isinstance(output_file_name, str)
    import csv
    import pandas as pd
    df = pd.DataFrame(columns=['episode', 'url', 'start_timestamp', 'start', 'end', 'question', 'context'])
    i = 0
    with open(raw_file_name) as csv_file:
        reader = csv.reader(csv_file)

        # skip the header row in the csv file
        next(reader)

        for row in reader:
            # assign each column in the row to a variable and split questions on carriage return
            episode, url, questions = row
            question_list = questions.split("\n")

            # for each question in the list, extract the timestamp and convert it to seconds for youtube
            for question in question_list:
                pieces = question.split('-')
                timestamp = pieces[0]
                minutes, seconds = timestamp.split(':')
                seconds = int(seconds) + (int(minutes.lstrip()) * 60)

                # add a new row to the dataframe
                df.loc[i] = [episode, url, timestamp, seconds, seconds, " ".join(pieces[1:]), ""]

                try:
                    df.loc[i - 1]['end'] = df.loc[i]['start']
                except:
                    print(f"skipping row {i} because there is no previous row")

                i += 1

                df['end'][df['end'] < df['start']] = 0
                df['end'][df['start'] == df['end']] = 0
    if output_file_name:
        df.to_csv(output_file_name)

    return df


def is_part_of_question(segment, start, end):
    if segment['start'] > start:
        if segment['end'] < end or end == 0:
            return True

    return False


# def get_question_context(row, transcription_output):
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


def ask_question(episode_df, question, completion_model='text-embedding-ada-002'):
    from openai.embeddings_utils import get_embedding,cosine_similarity

    question_vector = get_embedding(question, engine=completion_model)

    episode_df["similarities"] = episode_df['embedding'].apply(lambda x: cosine_similarity(x, question_vector))
    episode_df = episode_df.sort_values("similarities", ascending=False).head(4)

    print(f'{episode_df = }')

    episode_df.to_csv("sorted.csv")

    context = []
    for i, row in episode_df.iterrows():
        context.append(row['context'])

    print(f'{context = }')

    text = "\n".join(context)
    print(f'{text = }')

    context = text

    print(f'{context = }')


    prompt = f"""Answer the following question using only the context below. Answer in the style of Ben Carlson a financial advisor and podcaster. If you don't know the answer for certain, say I don't know.

    Context:
    {context}

    Q: {question}
    A:"""

    import openai
    completion = openai.Completion.create(
        prompt=prompt,
        temperature=1,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model=completion_model
    )["choices"][0]["text"].strip(" \n")

    print(f'{completion = }')
    return completion