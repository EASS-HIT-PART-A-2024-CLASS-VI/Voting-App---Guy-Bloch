import React, { useState, useEffect } from 'react';
import { getCandidates, addCandidate, castVote, fetchResults, deleteCandidate } from './api';

function App() {
  const [candidates, setCandidates] = useState([]);
  const [name, setName] = useState('');
  const [results, setResults] = useState([]);

  // Load candidates on component mount
  useEffect(() => {
    loadCandidates();
  }, []);

  const loadCandidates = async () => {
    try {
      const response = await getCandidates();
      setCandidates(response);
    } catch (error) {
      console.error('Error loading candidates:', error);
    }
  };

  const handleAddCandidate = async () => {
    if (!name.trim()) {
      alert('Please enter a candidate name');
      return;
    }

    try {
      await addCandidate({ name });
      setName('');
      loadCandidates();
    } catch (error) {
      console.error('Error adding candidate:', error);
    }
  };

const handleVote = async (id) => {
  try {
    await castVote(id);
    loadCandidates();
  } catch (error) {
    console.error('Error casting vote:', error);
  }
};


  const handleDelete = async (id) => {
    try {
      await deleteCandidate(id);
      loadCandidates();
    } catch (error) {
      console.error('Error deleting candidate:', error);
    }
  };

  const handleShowResults = async () => {
    try {
      const response = await fetchResults();
      setResults(response);
    } catch (error) {
      console.error('Error fetching results:', error);
    }
  };

  return (
    <div>
      <h1>Voting App</h1>
      <div>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Candidate Name"
        />
        <button onClick={handleAddCandidate}>Add Candidate</button>
      </div>

      <h2>Candidates</h2>
      <ul>
        {candidates.map((c) => (
          <li key={c.id}>
            {c.name} - Votes: {c.votes}
            <button onClick={() => handleVote(c.id)}>Vote</button>
            <button onClick={() => handleDelete(c.id)}>Delete</button>
          </li>
        ))}
      </ul>

      <button onClick={handleShowResults}>Show Results</button>

      <h2>Results</h2>
      <ul>
        {results.map((c) => (
          <li key={c.id}>
            {c.name} - Votes: {c.votes}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
