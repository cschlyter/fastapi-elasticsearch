import React from "react";
import { Formik } from "formik";
import { Button, Col, Form, Row } from "react-bootstrap";
import "./search.css";

function Search({ search, postEntry }) {
  const onSubmit = async (values, actions) => {
    if (values.submitType === "search") {
      await search(values.query, values.datetime);
    } else {
      await postEntry(values.query, values.datetime);
    }
  };

  return (
    <Formik
      initialValues={{
        query: "",
        datetime: "",
        submitType: "",
      }}
      onSubmit={onSubmit}
    >
      {({ handleChange, handleSubmit, values, setFieldValue }) => (
        <Form noValidate onSubmit={handleSubmit}>
          <Form.Group controlId="query">
            <Form.Label>Text query</Form.Label>
            <Col>
              <Form.Control
                type="text"
                name="query"
                placeholder="Enter a search term."
                value={values.query}
                onChange={handleChange}
              />
            </Col>
          </Form.Group>

          <Form.Group controlId="datetime">
            <Form.Label>Datetime</Form.Label>
            <Col>
              <Form.Control
                type="datetime-local"
                name="datetime"
                value={values.datetime}
                onChange={handleChange}
              />
            </Col>
          </Form.Group>

          <Form.Group as={Row} className="search-buttons">
            <Col>
              <Button
                type="submit"
                variant="primary"
                onClick={() => setFieldValue("submitType", "search")}
              >
                Search
              </Button>
              <Button
                type="submit"
                variant="secondary"
                className="ml-2"
                onClick={() => setFieldValue("submitType", "post")}
              >
                Post
              </Button>
            </Col>
          </Form.Group>
        </Form>
      )}
    </Formik>
  );
}

export default Search;
