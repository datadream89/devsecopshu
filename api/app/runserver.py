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
    <div className="max-w-xl mx-auto p-4 bg-white shadow rounded space-y-4">
      <h2 className="text-2xl font-bold">Tell us about yourself</h2>

      <input
        type="number"
        name="age"
        placeholder="Age"
        value={formData.age}
        onChange={handleChange}
        className="w-full p-2 border rounded"
      />

      <select
        name="maritalStatus"
        value={formData.maritalStatus}
        onChange={handleChange}
        className="w-full p-2 border rounded"
      >
        <option value="">Marital Status</option>
        <option value="single">Single</option>
        <option value="married">Married</option>
      </select>

      <select
        name="hasChildren"
        value={formData.hasChildren}
        onChange={handleChange}
        className="w-full p-2 border rounded"
      >
        <option value="">Do you have children?</option>
        <option value="yes">Yes</option>
        <option value="no">No</option>
      </select>

      <fieldset>
        <legend className="font-semibold">Health Conditions</legend>
        {['Diabetes', 'Cardiac', 'Mental Health'].map((condition) => (
          <label key={condition} className="block">
            <input
              type="checkbox"
              name="healthIssues"
              value={condition}
              checked={formData.healthIssues.includes(condition)}
              onChange={handleChange}
              className="mr-2"
            />
            {condition}
          </label>
        ))}
      </fieldset>

      <fieldset>
        <legend className="font-semibold">Lifestyle Habits</legend>
        {['Fitness', 'Nutrition'].map((habit) => (
          <label key={habit} className="block">
            <input
              type="checkbox"
              name="lifestyleHabits"
              value={habit}
              checked={formData.lifestyleHabits.includes(habit)}
              onChange={handleChange}
              className="mr-2"
            />
            {habit}
          </label>
        ))}
      </fieldset>

      <button
        onClick={recommendCircles}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Recommend Circles
      </button>
    </div>
  );
};

export default UserProfileForm;
