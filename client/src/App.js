import React, { useState } from "react"; // changed

import "./App.css";

import { Col, Container, Row } from "react-bootstrap";
import axios from "axios";

import ResultList from "./components/ResultList";
import Search from "./components/Search";
import config from "./config";

const API_URL = config.apiUrl;

function App() {
  const [results, setResults] = useState([]);

  const search = async (query, datetime) => {
    let params = { query: query };

    if (datetime) {
      params.start_date = datetime;
    }

    try {
      const response = await axios({
        method: "get",
        url: `${API_URL}/entries/`,
        params: params,
      });
      setResults(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const postEntry = async (text, datetime) => {
    try {
      await axios({
        method: "post",
        url: `${API_URL}/entries/`,
        data: {
          text: text,
          timestamp: datetime,
        },
      });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Container className="pt-3">
      <h1>FastAPI - Elasticsearch PoC</h1>
      <p className="lead">Use the controls below to search.</p>
      <Row>
        <Col lg={4}>
          <Search search={search} postEntry={postEntry} />
        </Col>
      </Row>
      <Row>
        <Col lg={8}>
          <ResultList results={results} />
        </Col>
      </Row>
    </Container>
  );
}

export default App;
