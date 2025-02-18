import axios from 'axios';
import API_URL from './config';

// Axios instance with baseURL
const api = axios.create({
  baseURL: API_URL,
});

// Fetch all candidates
export const getCandidates = async () => {
  try {
    const response = await api.get('/candidates');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch candidates:', error);
    throw error;
  }
};

// Add a candidate
export const addCandidate = async (candidateData) => {
  try {
    const response = await api.post('/candidates', {
      name: candidateData.name.trim(),
    });
    return response.data;
  } catch (error) {
    console.error('Failed to add candidate:', error.response?.data || error.message);
    throw error;
  }
};

// Cast a vote
export const castVote = async (candidateId) => {
  try {
    const response = await api.post('/vote/', { candidate_id: candidateId });
    return response.data;
  } catch (error) {
    console.error('Failed to cast vote:', error.response?.data || error.message);
    throw error;
  }
};

// Fetch voting results
export const fetchResults = async () => {
  try {
    const response = await api.get('/results');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch results:', error);
    throw error;
  }
};

// Delete a candidate
export const deleteCandidate = async (candidateId) => {
  try {
    const response = await api.delete(`/candidates/${candidateId}`);
    return response.data;
  } catch (error) {
    console.error('Failed to delete candidate:', error.response?.data || error.message);
    throw error;
  }
};