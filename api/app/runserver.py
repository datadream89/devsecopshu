import React, { useState } from 'react';

const healthCircles = {
  Diabetes: 'Diabetes Support Circle',
  Cardiac: 'Heart Health Circle',
  'Mental Health': 'Mental Wellness Circle',
};

const lifestyleCircles = {
  Fitness: 'Fitness Circle',
  Nutrition: 'Healthy Eating Circle',
};

const otherCircles = {
  senior: 'Active Aging Circle',
  parenting: 'Parenting Circle',
  single: 'Young Adults Circle',
};

const UserProfileForm = ({ onCircleRecommendation }) => {
  const [formData, setFormData] = useState({
    age: '',
    maritalStatus: '',
    hasChildren: '',
    healthIssues: [],
    lifestyleHabits: [],
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (type === 'checkbox') {
      const field = formData[name];
      const updated = checked
        ? [...field, value]
        : field.filter((v) => v !== value);
      setFormData({ ...formData, [name]: updated });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const recommendCircles = () => {
    const circles = [];

    formData.healthIssues.forEach((issue) => {
      if (healthCircles[issue]) circles.push(healthCircles[issue]);
    });

    formData.lifestyleHabits.forEach((habit) => {
      if (lifestyleCircles[habit]) circles.push(lifestyleCircles[habit]);
    });

    const age = parseInt(formData.age, 10);
    if (age >= 60) circles.push(otherCircles.senior);
    if (formData.hasChildren === 'yes') circles.push(otherCircles.parenting);
    if (formData.maritalStatus === 'single' && age < 35) {
      circles.push(otherCircles.single);
    }

    onCircleRecommendation([...new Set(circles)]);
  };

  return (
    <div className="max-w-2xl mx-auto bg-white shadow-lg rounded-2xl p-8 mt-10 border border-gray-100">
      <h2 className="text-3xl font-bold text-blue-700 mb-6">Join Cigna Circles</h2>

      {/* Age Input */}
      <div className="mb-5">
        <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
        <input
          type="number"
          name="age"
          value={formData.age}
          onChange={handleChange}
          placeholder="Enter your age"
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Marital Status */}
      <div className="mb-5">
        <label className="block text-sm font-medium text-gray-700 mb-1">Marital Status</label>
        <select
          name="maritalStatus"
          value={formData.maritalStatus}
          onChange={handleChange}
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select...</option>
          <option value="single">Single</option>
          <option value="married">Married</option>
        </select>
      </div>

      {/* Children */}
      <div className="mb-5">
        <label className="block text-sm font-medium text-gray-700 mb-1">Do you have children?</label>
        <select
          name="hasChildren"
          value={formData.hasChildren}
          onChange={handleChange}
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Select...</option>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </div>

      {/* Health Conditions */}
      <div className="mb-5">
        <h3 className="text-md font-semibold text-gray-700 mb-2">Health Conditions</h3>
        <div className="space-y-2">
          {['Diabetes', 'Cardiac', 'Mental Health'].map((condition) => (
            <label key={condition} className="flex items-center space-x-2 text-sm">
              <input
                type="checkbox"
                name="healthIssues"
                value={condition}
                checked={formData.healthIssues.includes(condition)}
                onChange={handleChange}
                className="accent-blue-600"
              />
              <span>{condition}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Lifestyle Habits */}
      <div className="mb-5">
        <h3 className="text-md font-semibold text-gray-700 mb-2">Lifestyle Habits</h3>
        <div className="space-y-2">
          {['Fitness', 'Nutrition'].map((habit) => (
            <label key={habit} className="flex items-center space-x-2 text-sm">
              <input
                type="checkbox"
                name="lifestyleHabits"
                value={habit}
                checked={formData.lifestyleHabits.includes(habit)}
                onChange={handleChange}
                className="accent-green-600"
              />
              <span>{habit}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Submit Button */}
      <div className="mt-8 text-right">
        <button
          onClick={recommendCircles}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium shadow"
        >
          Recommend Circles
        </button>
      </div>
    </div>
  );
};

export default UserProfileForm;
