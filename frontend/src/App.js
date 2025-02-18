import React, { useState, useEffect } from 'react';
import { getCandidates, addCandidate, castVote, fetchResults, deleteCandidate } from './api';
import ResultsChart from './ResultsChart';

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
      loadCandidates(); // Refresh candidate list
    } catch (error) {
      console.error('Error adding candidate:', error);
    }
  };

  const handleVote = async (id) => {
    try {
      await castVote(id);
      loadCandidates(); // Refresh after voting
    } catch (error) {
      console.error('Error casting vote:', error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteCandidate(id);
      loadCandidates(); // Refresh after deletion
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

      {/* Add Candidate Section */}
      <div>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Candidate Name"
        />
        <button onClick={handleAddCandidate}>Add Candidate</button>
      </div>

      {/* Candidates List */}
      <h2>Candidates</h2>
      <ul>
        {candidates.map((c) => (
          <li key={c.id}> {/* Use c.id instead of c._id */}
            {c.name} - Votes: {c.votes}
            <button onClick={() => handleVote(c.id)}>Vote</button>
            <button onClick={() => handleDelete(c.id)}>Delete</button>
          </li>
        ))}
      </ul>

      {/* Show Results Button */}
      <button onClick={handleShowResults}>Show Results</button>

      {/* Results Section */}
      <h2>Results</h2>
      <ul>
        {results.map((c) => (
          <li key={c.id}> {/* Use c.id instead of c._id */}
            {c.name} - Votes: {c.votes} - {c.percentage.toFixed(2)}%
          </li>
        ))}
      </ul>

      {/* Results Chart */}
      {results.length > 0 && (
        <>
          <h2>Voting Results Chart</h2>
          <ResultsChart results={results} />
        </>
      )}
    </div>
  );
}

export default App;