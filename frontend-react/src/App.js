// Imports react and necessary libraries
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

const App = () => {
    // State to store the user input
    const [question, setQuestion] = useState('');
    // State to store the response from backend
    const [response, setResponse] = useState('');
    // States to store summary and questions
    const [summary, setSummary] = useState('');
    const [questions, setQuestions] = useState([]);
    // State to track the current question index
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    // State to track answers for each question
    const [answers, setAnswers] = useState([]);
    // Ref to track if data has been fetched
    const dataFetched = useRef(false);

    // Fetch summary and questions on page load
    useEffect(() => {
        const fetchSummaryAndQuestions = async () => {
            try {
                const res = await axios.get('http://localhost:8000/generate-summary-and-questions');
                if (!dataFetched.current) { // Check to make sure summary and questions are blank
                    setSummary(res.data.summary);
                    setQuestions(res.data.questions);
                    dataFetched.current = true; // Mark data as fetched
                }
            } catch (error) {
                console.error("Error fetching summary and questions:", error);
            }
        };
        fetchSummaryAndQuestions();
    }, []);

    // Function to handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent page reload on submission
        try {
            // Make a POST request to the backend with the user question
            const res = await axios.post('http://localhost:8000/query', { question });
            setResponse(res.data.response); // Update the response state with the response from backend
            // Store the user's response to the current question
            setAnswers([...answers, { question, response: res.data.response }]);
            setQuestion(''); // Clear the input field for the next question
        } catch (error) {
            console.error("Error querying LLM:", error); // Log any errors
        }
    };

    // Function to handle moving to the next question
    const handleNextQuestion = () => {
        setCurrentQuestionIndex(currentQuestionIndex + 1); // Move to the next question
        setResponse(''); // Clear the response from previous question
    };

    return (
        <div>
            <h1>TutorAI: Textbook Learning Assistant</h1>

            {/* Display Summary */}
            <h2>Textbook Summary:</h2>
            <p>{summary}</p>

            {/* Display all previous questions and answers */}
            <h3>Questions and Responses:</h3>
            {questions.slice(0, currentQuestionIndex + 1).map((q, index) => (
                <div key={index}>
                    <p><strong>Question {index + 1}:</strong> {q}</p>
                    {answers[index] && (
                        <p><strong>Your Answer:</strong> {answers[index].question}</p>
                    )}
                    {answers[index] && (
                        <p><strong>Response:</strong> {answers[index].response}</p>
                    )}
                </div>
            ))}

            {/* Display the current question */}
            <h3>Current Question:</h3>
            {questions.length > 0 && <p>{questions[currentQuestionIndex]}</p>}

            {/* Display question input form */}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Your Answer"
                />
                <button type="submit">Submit</button>
            </form>

            {/* Display Response */}
            <div>
                <h2>Response:</h2>
                <p>{response}</p>
            </div>

            {/* Display Next Question button */}
            {currentQuestionIndex < questions.length - 1 && (
                <button onClick={handleNextQuestion}>Next Question</button>
            )}

            {/* Optionally, show a message when all questions have been answered */}
            {currentQuestionIndex >= questions.length && (
                <p>All questions answered!</p>
            )}
        </div>
    );
};

export default App;
