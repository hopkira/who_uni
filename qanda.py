#!/usr/bin/env python
# coding: utf-8

import numpy as np
import openai
import pandas as pd
import tiktoken

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"
openai.api_key_path = ".env"
MAX_SECTION_LEN = 500
SEPARATOR = "\n"
ENCODING = "gpt2"  # encoding for text-davinci-003
encoding = tiktoken.get_encoding(ENCODING)
separator_len = len(encoding.encode(SEPARATOR))

def load_embeddings(filename):
    """
    Read the document embeddings and their keys from a CSV.
    
    fname is the path to a CSV with exactly these named columns: 
        "title", "heading", "0", "1", ... up to the length of the embedding vectors.
    """
    
    df = pd.read_csv(filename)
    max_dim = 1535
    return {
           (r.title, r.mistress, r.synopsis): [r[str(i)] for i in range(max_dim + 1)] for index, r in df.iterrows()
    }

def get_embedding(text: str, model: str=EMBEDDING_MODEL):
    result = openai.Embedding.create(
      model=model,
      input=text
    )
    return result["data"][0]["embedding"]


def vector_similarity(x, y):
    """
    Returns the similarity between two vectors.
    
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))


def order_document_sections_by_query_similarity(query, contexts):
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections. 
    
    Return the list of document sections, sorted by relevance in descending order.
    """
    query_embedding = get_embedding(query)
    
    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)
    
    return document_similarities

def build_prompt(question: str, context_embeddings: dict) -> str:
    text = ""
    most_relevant_document_sections = order_document_sections_by_query_similarity(question, context_embeddings)
    for section in most_relevant_document_sections:
        score, content = section
        story, mistress, synopsis = content
        length = len(text)
        syn_length = len(synopsis)
        if (length + syn_length + separator_len) > MAX_SECTION_LEN:
            print(syn_length)
            break
        text = (SEPARATOR + text + synopsis).replace("\n"," ")
    header = """Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say "Insufficient data." Always use the word "affirmative" instead of "yes" and "negative" instead of "no".\n\nContext:\n"""
    return header + "" + text + "\n\n Q: " + question + "\n A:"


class Backhistory():
    '''
    Question and answer capability
    '''
    def __init__(self) -> None:
        self.document_embeddings = load_embeddings("k9_story_vectors_500.csv")

    def get_answer(self, question:str):
        prompt = build_prompt(
            question,
            self.document_embeddings
        )
        answer = openai.Completion.create(
            engine=COMPLETIONS_MODEL,
            prompt=prompt,
            temperature=0.0,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return answer["choices"][0]["text"]