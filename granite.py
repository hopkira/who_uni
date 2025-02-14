import ollama # enables working with local models
import pandas as pd # works with spreadsheets/tables
import chromadb # vector database working as long term memory

gen_model = "granite3-moe:3b"
embed_model = "granite-embedding:30m"
collection_name = "k9_ltm_gran_30m"

# Create Chroma database and collection for Long Term Memory
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name=collection_name
    )

def add_documents(documents):
    """
    Add documents to ChromaDB
    """
    for i, doc in enumerate(documents):
        response = ollama.embed(model=embed_model, input=doc)
        embeddings = response["embeddings"]
        collection.add(
            ids=[str(i)],
            embeddings=embeddings,
            documents=[doc]
        )
    print(f"Added {len(documents)} documents to K9's long term memory.")

def retrieve_document(query):
    """
    Retrieve the most relevant document
    """
    response = ollama.embed(
        model=embed_model,
        input = query
    )
    results = collection.query(
        query_embeddings=response["embeddings"],
        n_results=1
    )
    if results["documents"]:
        return results["documents"][0][0]  # Return top match
    return None

# Load initial K9 backstory into ChromaDB
df = pd.read_csv('k9_stories_500.csv')
add_documents(df['synopsis'])

# Get question from user
query = input("Ask question:")

# Retrieve the document that answers the query
data = retrieve_document(query = query)

# Generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model=gen_model,
  prompt=f"You are K9, a robot dog. Using only this data: {data} \
  generate K9's short, single sentence, response to this question: {query}"
)

print(output['response'])