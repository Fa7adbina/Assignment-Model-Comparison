import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { question } = req.body;

    try {
      const response = await axios.post('http://localhost:5000/ask', { question });
      res.status(200).json(response.data);
    } catch (error) {
      console.error('Error querying data:', error);
      res.status(500).json({ error: 'Failed to query data' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
