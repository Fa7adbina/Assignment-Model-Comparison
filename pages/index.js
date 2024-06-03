import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');

  const handleQuery = async () => {
    try {
      const response = await axios.post('/api/query', { question: query });
      setResults(response.data);
      setError('');
    } catch (error) {
      console.error('Error querying data:', error);
      setError('An error occurred while querying the data.');
    }
  };

  return (
    <div>
      <h1>Query Pinecone Data</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query"
      />
      <button onClick={handleQuery}>Search</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        {results.map((result, index) => (
          <div key={index}>
            <p>{result}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
