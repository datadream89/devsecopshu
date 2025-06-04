import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import UserProfileForm from './components/UserProfileForm';

function App() {
  const [recommendedCircles, setRecommendedCircles] = useState([]);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <UserProfileForm onCircleRecommendation={setRecommendedCircles} />
      {recommendedCircles.length > 0 && (
        <div className="mt-6 p-4 bg-green-100 rounded shadow">
          <h3 className="text-lg font-bold mb-2">Recommended Circles</h3>
          <ul className="list-disc pl-5">
            {recommendedCircles.map((circle, idx) => (
              <li key={idx}>{circle}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
