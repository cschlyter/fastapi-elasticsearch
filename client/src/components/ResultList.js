import React from "react";
import Table from "react-bootstrap/Table";
import "./result-list.css";

function ResultList({ results }) {
  return (
    <div className="result-list">
      {!results && <p>Search using the left panel.</p>}
      {results && results.length === 0 && <p>No results found.</p>}
      {results && results.length > 0 && (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>ID</th>
              <th>Text</th>
              <th>Datetime</th>
            </tr>
          </thead>
          <tbody>
            {results.map((result) => (
              <tr key={result.id}>
                <td>{result.id}</td>
                <td>{result.text}</td>
                <td>{result.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
}

export default ResultList;
