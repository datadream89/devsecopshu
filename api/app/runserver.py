import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import UserProfileForm from './components/UserProfileForm';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <UserProfileForm
    onCircleRecommendation={(circles) => {
      alert(`Recommended Circles:\n${circles.join('\n')}`);
    }}
  />
);
