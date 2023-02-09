# SNIP form "building_a_financial_advisor" example 
# -*- coding: utf-8 -*-
# todo
#   The current name of the repo is "Financial Advisor" but it should be changed to something more general, thats just the 
#       current example to get us started
#   I'll be opening issues for these and posting collaboration instructions soon, feel free at the assist in any way you
#       can, simply remember to create a new fork and follow common git practices for the time being. DO-NOT delete works
#       of others!!! instead contribute in modules and create a pull request.
#       Microservices (use of modules, classes, endpoints) is the way to go.
#       Most help appreciated for continuous integration and testing (CI/CD) and documentation.
#  - suggestions of better context for the question
#  - use pretrained models for a more robust solution both for the embeddings and the completions
#  - move from script to a web app
#  - add description of channel, etc... in the prompt
#  - add a way to add more context to the prompt in a more interactive way like a conversation
#  - sort the context by similarity and recentness, search web for more context
#  - relies on data preparation modules which should be chosen based on the data type itself
#     - Input Models
#       - youtube module
#       - "finBERT" model for financial text classification and sentiment analysis of financial news
#       - Read financial reports module (10-K, 10-Q, 8-K, etc...) and extract context using NLP 
#                                                                               (base models already exist)
#       - google speech to text module
#       - documentation reader module
#       - live streams module
#       - podcast module
#       - books module
#       - articles module
#       - research papers module
#     - Ensemble DB Schemes
#       - Prompt engineering
#       - Context choice
#       - Tokenizer module
#       - Context weighting for settings optimization and preparing any assisting data needed to answer the question
#       - Question Engineering
#     - Live Conversions
#       - Live explaining/translation of stream
#       - Live summarization of stream
#       - Live question answering of stream
#       - Live Actions based on stream
#   Not all these require either usage of embeddings or completion models. Modularity and speed are key,
#       although the latter is not a priority at the moment. Proof of concept and demo creation is the priority.
#       a priority at the moment. Proof of concept and demo creation is the priority.