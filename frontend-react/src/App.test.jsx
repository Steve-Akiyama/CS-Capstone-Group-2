import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import axios from 'axios';
import '@testing-library/jest-dom';

// Mock Axios module
jest.mock('axios');

describe('App Component', () => {
  let mockDocument = 'This is a test document content';
  let mockSummary = 'This is a summary of the document';
  let mockQuestions = ['What is the purpose of this document?', 'What is the main topic?'];
  let mockResponse = { response: 'This is the AI response' };

  beforeEach(() => {
    // Reset mock behavior before each test
    axios.get.mockReset();
    axios.post.mockReset();
  });

  test('renders initial content', async () => {
    // Mock the axios GET request for document and summary
    axios.get.mockResolvedValueOnce({ data: { document: mockDocument } }) // Document
      .mockResolvedValueOnce({ data: { summary: mockSummary, questions: mockQuestions } }); // Summary and Questions

    // Render the component
    render(<App />);

    // Assert document content is rendered
    expect(await screen.findByText(mockDocument)).toBeInTheDocument();
    expect(screen.getByText(mockSummary)).toBeInTheDocument();
    expect(screen.getByText(mockQuestions[0])).toBeInTheDocument();
  });

  test('submitting a question updates answers', async () => {
    // Mock the axios GET request for document and summary
    axios.get.mockResolvedValueOnce({ data: { document: mockDocument } }) // Document
      .mockResolvedValueOnce({ data: { summary: mockSummary, questions: mockQuestions } }); // Summary and Questions

    // Mock the axios POST request for submitting answers
    axios.post.mockResolvedValueOnce(mockResponse);

    // Render the component
    render(<App />);

    // Wait for the questions to load
    await waitFor(() => screen.getByText(mockQuestions[0]));

    // Simulate user typing in the answer
    const inputField = screen.getByPlaceholderText('Your Answer');
    fireEvent.change(inputField, { target: { value: 'My answer to the first question' } });

    // Simulate form submission
    const submitButton = screen.getByText('Submit');
    fireEvent.click(submitButton);

    // Assert the answer and response are rendered in the chat
    expect(await screen.findByText('Your Answer: My answer to the first question')).toBeInTheDocument();
    expect(await screen.findByText('Response: This is the AI response')).toBeInTheDocument();
  });

  test('displays completion message when all questions are answered', async () => {
    // Mock the axios GET request for document and summary
    axios.get.mockResolvedValueOnce({ data: { document: mockDocument } }) // Document
      .mockResolvedValueOnce({ data: { summary: mockSummary, questions: mockQuestions } }); // Summary and Questions

    // Mock the axios POST request for submitting answers
    axios.post.mockResolvedValueOnce(mockResponse);

    // Render the component
    render(<App />);

    // Wait for the questions to load
    await waitFor(() => screen.getByText(mockQuestions[0]));

    // Simulate answering all questions
    const inputField = screen.getByPlaceholderText('Your Answer');
    const submitButton = screen.getByText('Submit');
    
    fireEvent.change(inputField, { target: { value: 'My answer to the first question' } });
    fireEvent.click(submitButton);

    fireEvent.change(inputField, { target: { value: 'My answer to the second question' } });
    fireEvent.click(submitButton);

    // Assert that the completion message is displayed
    expect(screen.getByText('All questions answered!')).toBeInTheDocument();
  });
});