from os import getenv

import openai
import pandas as pd

openai.api_key = getenv("OPENAI_API_KEY")

# Read the data
df = pd.read_csv("questions_w_context_n_embedding.csv")

# Prepare the data for training e.g. {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
data = []
for index, row in df.iterrows():
    print(f'{row["context"] = }')
    print(f'{row["question"] = }')

    exit()
    data.append({"prompt": row["context"], "completion": row["question"]})

# save the data to a file
df = pd.DataFrame(data)
df.to_csv("questions_w_context_n_embedding_training.csv")


print("Data saved to file")
# After you’ve fine-tuned a model, remember that your prompt has to end with the indicator string ` ->` for the model to start generating completions, rather than continuing with the prompt. Make sure to include `stop=["\n"]` so that the generated texts ends at the expected place.
# Once your model starts training, it'll approximately take 15.24 minutes to train a `curie` model, and less for `ada` and `babbage`. Queue will approximately take half an hour per job ahead of you.

exit()
# Train the model
response = openai.Completion.create(
    engine="davinci",
    prompt="",
    max_tokens=1024,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n", "###"],
    data=data,
)

# Print the training loss
print(response["model"]["training_loss"])




# import nltk
# nltk.download('punkt')
# from nltk.tokenize import word_tokenize
#
# # Load and pre-process the context data
# text = "The climate crisis is a pressing issue that affects us all. Climate change is causing sea levels to rise, temperatures to increase, and natural disasters to become more frequent. It is up to all of us to take action and work towards a more sustainable future."
#
# # Tokenize the text
# tokens = word_tokenize(text)
#
# # Convert the text to lowercase
# tokens = [token.lower() for token in tokens]
#
# # Remove stop words and punctuation
# stop_words = set(nltk.corpus.stopwords.words("english"))
# tokens = [token for token in tokens if token not in stop_words and token.isalpha()]
#
# import openai
#
# # Initialize the OpenAI API client
# openai.api_key = "YOUR_API_KEY"
#
# # Generate responses using the context data
# response = openai.Completion.create(
#     engine="davinci",
#     prompt=" ".join(tokens),
#     max_tokens=1024,
#     n=1,
#     stop=None,
#     temperature=0.5,
# )
#
# # Print the generated response
# print(response["choices"][0]["text"])
