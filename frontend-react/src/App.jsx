import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

const BASE_URL = window.location.origin.includes('localhost')
    ? 'http://localhost:8000'  // If running locally, assume backend is on localhost:8000
    : 'http://52.15.75.24:8000';  // Replace with your production backend URL

const App = () => {
    const dataFetched = useRef(false);
    const [answer, setAnswer] = useState('');
    const [questions, setQuestions] = useState([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState([]);
    const [summary, setSummary] = useState('');
    const [document, setDocument] = useState('');
    const [score, setScore] = useState(0);
    const [submitDisabled, setSubmitDisabled] = useState(false);

    // Fetch document once when the component mounts
    useEffect(() => {
        const fetchDocument = async () => {
            try {
                const res = await axios.get(`${BASE_URL}/retrieve-document`);
                setDocument(res.data.document);
            } catch (error) {
                console.error("Error fetching document:", error.response || error);
            }
        };
        fetchDocument();
    }, []); // Empty dependency array ensures this runs only once when the component mounts

    // Fetch summary and questions on page load
    useEffect(() => {
        const fetchSummaryAndQuestions = async () => {
            try {
                const res = await axios.get(`${BASE_URL}/generate-summary-and-questions`);
                if (!dataFetched.current) {
                    setSummary(res.data.summary);
                    setQuestions(res.data.questions);
                    dataFetched.current = true;
                }
            } catch (error) {
                console.error("Error fetching summary and questions:", error);
            }
        };
        fetchSummaryAndQuestions();
    }, []);
    
    // Function to handle user submissions
    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitDisabled(true);

        try {
            const userAnswer = answer;
            const res = await axios.post(`${BASE_URL}/query`, { 
                question: questions[currentQuestionIndex], 
                user_answer: userAnswer 
            });

            setAnswers([
                ...answers,
                { question: questions[currentQuestionIndex], user_answer: userAnswer, response: res.data.response, score: res.data.score }
            ]);

            setAnswer('');
            setScore(Number(res.data.score) + Number(score));
            setCurrentQuestionIndex(currentQuestionIndex + 1);
        } catch (error) {
            console.error("Error querying LLM:", error);
        } finally {
            setSubmitDisabled(false);
        }
    };

    return (
        <div className="app-container">
            <h1 className="app-title">TutorAI: Textbook Learning Assistant</h1>
            <div className="textbook-container">
                <h2>Textbook Content:</h2>
                <p className="textbook-content">{document}</p>
            </div>
            <div className="summary-container">
                <h2>Textbook Summary:</h2>
                <p className="summary-content">{summary}</p>
            </div>
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
            {currentQuestionIndex > 0 && (
                <div className="current-question">
                    <h3>Current Score:</h3>
                    <p>{score}/{currentQuestionIndex * 10}</p>
                </div>
            )}
            <form className="input-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    placeholder="Your Answer"
                />
                <button type="submit" disabled={submitDisabled}>Submit</button>
            </form>
            {currentQuestionIndex >= questions.length && (
                <p className="completion-message">All questions answered!</p>
            )}
        </div>
    );
};

export default App;
