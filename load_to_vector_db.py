# import json
# from sentence_transformers import SentenceTransformer
# from pinecone import Pinecone, Index, ServerlessSpec

# # Initialize Pinecone
# pinecone = Pinecone(api_key='c1c2a453-27bf-45a5-9bd1-e46a93144a03')
# index_name = 'web-content'

# # Delete old index if exists
# if index_name in pinecone.list_indexes().names():
#     pinecone.delete_index(index_name)

# # Create new index with the correct dimension
# pinecone.create_index(
#     name=index_name,
#     dimension=384,
#     metric='cosine',
#     spec=ServerlessSpec(
#         cloud='aws',
#         region='us-east-1'
#     )
# )

# index = pinecone.Index(index_name)

# # Load sentence-transformers model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# def load_data(filename):
#     with open(filename, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#     return data

# def store_in_vector_db(data):
#     # Transform data into vectors and store in Pinecone
#     for item in data:
#         vector = model.encode(item['content']).tolist()
#         index.upsert(vectors=[{"id": item['id'], "values": vector, "metadata": {"text": item['content']}}])

# # Example usage
# if __name__ == '__main__':
#     data = load_data('web_content.json')
#     store_in_vector_db(data)


from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create an instance of the Pinecone class
pc = Pinecone(api_key='API-Key')

# Specify the index name and check if it exists
index_name = 'your-index-name'
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
index = pc.Index(index_name)

# Example data
data = [
    {"id": "1", "content": "This is the first document."},
    {"id": "2", "content": "This is the second document."}
]

# Function to store data in the vector database
def store_in_vector_db(data):
    # Transform data into vectors and store in Pinecone
    for item in data:
        if 'content' in item and 'id' in item:
            vector = model.encode(item['content']).tolist()
            index.upsert(vectors=[{"id": item['id'], "values": vector, "metadata": {"text": item['content']}}])
        else:
            print(f"Item {item} does not have 'content' or 'id' key")

# Call the function
store_in_vector_db(data)

