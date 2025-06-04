## Step 6: src/index.css

css
@tailwind base;
@tailwind components;
@tailwind utilities;


---

### Step 7: src/index.js

jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-700">Welcome to Cigna Circles MVP!</h1>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);


---

### Step 8: public/index.html

html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title> MVP</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>


---

### Step 9: Install Webpack and Babel

powershell
npm install -D webpack webpack-cli webpack-dev-server babel-loader @babel/core @babel/preset-env @babel/preset-react css-loader style-loader postcss-loader


---

### Step 10: webpack.config.js

js
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  devServer: {
    static: './public',
    hot: true,
    open: true,
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};


---

### Step 11: .babelrc

json
{
  "presets": ["@babel/preset-env", "@babel/preset-react"]
}


---

### Step 12: postcss.config.js

js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};


---

### Step 13: Add scripts in package.json

json
"scripts": {
  "start": "webpack serve --mode development --open",
  "build": "webpack --mode production"
}


---

### Step 14: Run

powershell
npm start
