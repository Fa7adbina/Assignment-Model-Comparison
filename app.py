from flask import Flask, request, jsonify
from scraper import scrape_website
from models import query_openai_model, query_replicate_model
from comparison import compare_responses
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

app = Flask(__name__)

# Initialize Pinecone
pinecone = Pinecone(
    api_key='c1c2a453-27bf-45a5-9bd1-e46a93144a03'
)
index = pinecone.Index('web-content')

# Load the sentence transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')

    # Query the vector database
    search_results = query_vector_db(user_question)
    
    # Create requests for the models
    responses = {
        "gpt-3.5-turbo": query_openai_model('gpt-3.5-turbo', user_question, search_results),
        "gpt-4": query_openai_model('gpt-4', user_question, search_results),
        "Llama-2-70b-chat": query_replicate_model('Llama-2-70b-chat', user_question, search_results),
        "Falcon-40b-instruct": query_replicate_model('Falcon-40b-instruct', user_question, search_results)
    }
    
    # Compare the responses
    best_response = compare_responses(responses)
    
    return jsonify(best_response)

def query_vector_db(question):
    # Encode the question to a vector
    question_vector = model.encode(question).tolist()

    # Query Pinecone and retrieve data
    query_response = index.query(vector=question_vector, top_k=5)
    matches = query_response['matches']
    return [{"text": match["metadata"]["text"]} for match in matches]

if __name__ == '__main__':
    app.run(debug=True, port=5000)
