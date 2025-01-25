// Imports react and necessary libraries
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

const BASE_URL = window.location.origin.includes('localhost')
    ? 'http://localhost:8000'  // If running locally, assume backend is on localhost:8000
    : 'http://52.15.75.24:8000/';  // Replace with your production backend URLconsole.log("API Base URL:", BASE_URL);

const App = () => {
    // BACKEND
    const dataFetched = useRef(false);              // Data fetch reference; true if summary/textbook data has been fetched. False otherwise.
    
    // USER Q/A
    const [answer, setAnswer] = useState('');       // Answer from the user (Textbox content)
    const [questions, setQuestions] = useState([]); // Questions generated by the LLM
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0); // IDX of the currently shown question
    const [answers, setAnswers] = useState([]);     // Answer set from the user

    // DOCUMENT CONTENT
    const [summary, setSummary] = useState('');     // Summary of the document content
    const [document, setDocument] = useState('');  // Document content
    const [score, setScore] = useState(0)
    

    useEffect(() => {
        const fetchDocument = async () => {
            try {
                const res = await axios.get(`${BASE_URL}/retrieve-document`);
                setDocument(res.data.document)
            } catch (error) {
                console.error("Error fetching document:", error.response || error)
            }
        };
        fetchDocument();
    });

    // Fetch summary and questions on page load
    useEffect(() => {
        const fetchSummaryAndQuestions = async () => {
            try {
                const res = await axios.get(`${BASE_URL}/generate-summary-and-questions`);
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
    
    // Function to handle user submissions
    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent page reload on submission
        try {
            // Get the current question's answer from the input field (the user's response)
            const userAnswer = answer;
    
            // Make a POST request to the backend with the question and user's answer
            const res = await axios.post(`${BASE_URL}/query`, { 
                question: questions[currentQuestionIndex], 
                user_answer: userAnswer 
            });
        
            // Store the user's response to the current question in the answers state
            setAnswers([
                ...answers,
                { question: questions[currentQuestionIndex], user_answer: userAnswer, response: res.data.response, score: res.data.score }
            ]);
    
            setAnswer(''); // Clear the input field for the next question
            setScore(Number(res.data.score) + Number(score))
            setCurrentQuestionIndex(currentQuestionIndex + 1); // Move to the next question
        } catch (error) {
            console.error("Error querying LLM:", error); // Log any errors
        }
    };
    

    return (
        <div className="app-container">
            <h1 className="app-title">TutorAI: Textbook Learning Assistant</h1>

            {/* Textbook Content Section */}
            <div className="textbook-container">
                <h2>Textbook Content:</h2>
                <p className="textbook-content">{document}</p>
            </div>

            {/* Summary Section */}
            <div className="summary-container">
                <h2>Textbook Summary:</h2>
                <p className="summary-content">{summary}</p>
            </div>

            {/* Chat Section */}
            <div className="chat-container">
                <h3>Questions and Responses:</h3>
                {questions.slice(0, currentQuestionIndex + 1).map((q, index) => (
                    <div key={index} className="chat-bubble-container">
                        <div className="chat-bubble user-bubble">
                            <strong>Question {index + 1}:</strong> {q}
                        </div>
                        {answers[index] && (
                            <div className="chat-bubble user-answer">
                                <strong>Your Answer:</strong> {answers[index].user_answer}
                            </div>
                        )}
                        {answers[index] && (
                            <div className="chat-bubble ai-response">
                                <strong>Response:</strong> {answers[index].response}
                                <br></br>
                                <strong>Score:</strong> {answers[index].score}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Current Question Section */}

            {currentQuestionIndex > 0 &&
            <div className="current-question">
                <h3>Current Score:</h3>
                <p>{score}/{currentQuestionIndex * 10}</p>
            </div>
            }

            {/* Input Form Section */}
            <form className="input-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    placeholder="Your Answer"
                />
                <button type="submit">Submit</button>
            </form>

            {/* Completion Message */}
            {currentQuestionIndex >= questions.length && (
                <p className="completion-message">All questions answered!</p>
            )}
        </div>
    );
};

export default App;
