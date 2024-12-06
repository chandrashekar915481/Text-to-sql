import React, { useState } from 'react';
import './SQLGenerator.css';

const INITIAL_SCHEMA = `-- Employees and Salaries
CREATE TABLE employees (
    id INT,
    name TEXT,
    department TEXT,
    salary INT
);

INSERT INTO employees (id, name, department, salary) VALUES
(1, 'John Smith', 'IT', 75000),
(2, 'Sarah Johnson', 'HR', 65000),
(3, 'Michael Brown', 'IT', 82000),
(4, 'Emily Davis', 'Marketing', 68000),
(5, 'James Wilson', 'HR', 70000),
(6, 'Lisa Anderson', 'Marketing', 71000);
CREATE TABLE sales (
    id INT,
    date DATE,
    amount DECIMAL
);

INSERT INTO sales (id, date, amount) VALUES
(1, '2023-01-15', 12500.50),
(2, '2023-01-28', 8750.75),
(3, '2023-02-10', 15200.25),
(4, '2023-02-22', 9800.50),
(5, '2023-03-05', 13600.75),
(6, '2023-03-18', 11200.25);
-- Climate Communication Projects
CREATE TABLE climate_communication (
    project_id INT,
    project_name VARCHAR(255),
    location VARCHAR(255),
    start_date DATE,
    end_date DATE,
    total_cost DECIMAL(10,2)
);

INSERT INTO climate_communication (project_id, project_name, location, start_date, end_date, total_cost) VALUES
(1, 'Project Green', 'California', '2023-01-01', '2023-12-31', 250000.00),
(2, 'Water Conservation', 'Texas', '2023-03-01', '2024-02-28', 150000.00),
(3, 'Solar Initiative', 'Nevada', '2023-06-15', '2024-06-15', 300000.00);
`;

const SQLGenerator = () => {
  const [context, setContext] = useState(INITIAL_SCHEMA);
  const [prompt, setPrompt] = useState('');
  const [expectedSQL, setExpectedSQL] = useState('');
  const [result, setResult] = useState(null);
  const [comparisonResult, setComparisonResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/generate-and-execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          context,
          prompt,
        }),
      });

      const data = await response.json();

      // Display generated SQL even if there is an error
      if (data.error) {
        setResult({ generated_sql: data.generated_sql || '' }); // Show the generated SQL
        setError(data.error); // Show the error message
        return;
      }

      // Compare generated SQL with expected SQL
      if (data.generated_sql.trim() === expectedSQL.trim()) {
        setComparisonResult('The generated SQL matches the expected SQL.');
      } else {
        setComparisonResult('The generated SQL does NOT match the expected SQL.');
      }

      setResult(data);
    } catch (err) {
      setError('Failed to process request: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sql-generator-container">
      <h1 className="sql-generator-title">SQL Query Generator</h1>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Database Schema Context:</label>
          <textarea
            className="schema-textarea"
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Enter CREATE TABLE and INSERT statements..."
          />
        </div>

        <div className="form-group">
          <label className="form-label">Natural Language Query:</label>
          <input
            type="text"
            className="query-input"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="What would you like to query?"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Expected SQL Query:</label>
          <textarea
            className="schema-textarea"
            value={expectedSQL}
            onChange={(e) => setExpectedSQL(e.target.value)}
            placeholder="Enter the expected SQL query..."
          />
        </div>

        <button
          type="submit"
          className="generate-button"
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Generate and Compare'}
        </button>
      </form>

      {comparisonResult && (
        <div className={`comparison-result ${comparisonResult.includes('NOT') ? 'error-message' : ''}`}>
          {comparisonResult}
        </div>
      )}

      {error && (
        <div className="error-message">
          <h3>Error:</h3>
          <p>{error}</p>
        </div>
      )}

      {result && (
        <div className="results-container">
          <div className="result-section">
            <h2>Generated SQL:</h2>
            <pre className="sql-code">{result.generated_sql}</pre>
          </div>

          {result.results && result.results.length > 0 && (
            <div className="result-section">
              <h2>Query Results:</h2>
              <table className="results-table">
                <thead>
                  <tr>
                    {Object.keys(result.results[0]).map((key) => (
                      <th key={key}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.results.map((row, i) => (
                    <tr key={i}>
                      {Object.values(row).map((value, j) => (
                        <td key={j}>{value}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SQLGenerator;
