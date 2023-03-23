
YouTube chapters extraction:
Implement a function to extract YouTube chapters (timestamps and titles) from the video description or metadata.
If the chapters are not available, consider implementing an alternative method, such as using an NLP model to detect topic changes in the transcription.

Adapt the existing transcription process:
Modify the current transcription process to work with YouTube chapters. Transcribe each chapter separately and store the transcriptions in a structured format, such as a dictionary or a DataFrame, with chapter information.

Chapter-based context extraction:
Develop a function to extract context from each chapter separately. This function should be able to identify questions within chapters and extract relevant context for each question.

Embedding generation for chapters:
Modify the existing embedding generation process to work with the chapter-based context. Generate embeddings for each question's context within the chapters.

Training data preparation:
Combine the chapter-based context and embeddings into a single dataset suitable for training a model. Ensure that the data format is consistent with the input requirements of the target model.

Update the OpenAI API query:
Modify the existing API query function to work with chapter-based context and embeddings. Ensure that the model can effectively answer questions based on the context from the YouTube chapters.

Documentation and code refactoring:
Update the existing documentation to include the new functionality related to YouTube chapters. Make sure to provide clear instructions on how to use the new module.
Refactor the code to ensure modularity, readability, and maintainability. Separate the chapter-based functionality into a dedicated module or class, if necessary.

Testing and continuous integration:
Implement unit tests and integration tests to ensure the proper functioning of the new module and its compatibility with the existing codebase.
Set up a continuous integration (CI) pipeline to automate the testing and deployment process, ensuring that any new changes do not break existing functionality.
SNIP form "building_a_financial_advisor" example 
-*- coding: utf-8 -*-
todo
  The current name of the repo is "Financial Advisor" but it should be changed to something more general, thats just the 
      current example to get us started
  I'll be opening issues for these and posting collaboration instructions soon, feel free at the assist in any way you
      can, simply remember to create a new fork and follow common git practices for the time being. DO-NOT delete works
      of others!!! instead contribute in modules and create a pull request.
      Microservices (use of modules, classes, endpoints) is the way to go.
      Most help appreciated for continuous integration and testing (CI/CD) and documentation.
 - suggestions of better context for the question
 - use pretrained models for a more robust solution both for the embeddings and the completions
 - move from script to a web app
 - add description of channel, etc... in the prompt
 - add a way to add more context to the prompt in a more interactive way like a conversation
 - sort the context by similarity and recentness, search web for more context
 - relies on data preparation modules which should be chosen based on the data type itself
    - Input Models
      - youtube module
      - "finBERT" model for financial text classification and sentiment analysis of financial news
      - Read financial reports module (10-K, 10-Q, 8-K, etc...) and extract context using NLP 
                                                                              (base models already exist)
      - google speech to text module
      - documentation reader module
      - live streams module
      - podcast module
      - books module
      - articles module
      - research papers module
    - Ensemble DB Schemes
      - Prompt engineering
      - Context choice
      - Tokenizer module
      - Context weighting for settings optimization and preparing any assisting data needed to answer the question
      - Question Engineering
    - Live Conversions
      - Live explaining/translation of stream
      - Live summarization of stream
      - Live question answering of stream
      - Live Actions based on stream
  Not all these require either usage of embeddings or completion models. Modularity and speed are key,
      although the latter is not a priority at the moment. Proof of concept and demo creation is the priority.
      a priority at the moment. Proof of concept and demo creation is the priority.