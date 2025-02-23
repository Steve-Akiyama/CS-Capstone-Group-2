import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

const BASE_URL = window.location.origin.includes('localhost')
    ? 'http://localhost:8000'  // If running locally, assume backend is on localhost:8000
    : 'http://52.15.75.24:8000';  // Replace with your production backend URL

const App = () => {
    const dataFetched = useRef(false);
    const chatContainerRef = useRef(null); // Reference for the chat container

    const [answer, setAnswer] = useState('');
    const [questions, setQuestions] = useState(() => {
        const saved = localStorage.getItem("questions");
        return saved ? JSON.parse(saved) : [];
    });
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(() => {
        const saved = localStorage.getItem("currentQuestionIndex");
        return saved ? JSON.parse(saved) : 0;
    });
    const [answers, setAnswers] = useState(() => {
        const saved = localStorage.getItem("answers");
        return saved ? JSON.parse(saved) : [];
    });
    const [summary, setSummary] = useState(() => {
        const saved = localStorage.getItem("summary");
        return saved ? JSON.parse(saved) : '';
    });
    const [score, setScore] = useState(() => {
        const saved = localStorage.getItem("score");
        return saved ? JSON.parse(saved) : 0;
    });
    const [submitDisabled, setSubmitDisabled] = useState(false);
    const [currentModule, setCurrentModule] = useState('6.1');
    const [nextSectionClicked, setNextSectionClicked] = useState(false); // Track button click state

    // Save state changes to localStorage
    useEffect(() => {
        localStorage.setItem("questions", JSON.stringify(questions));
    }, [questions]);

    useEffect(() => {
        localStorage.setItem("currentQuestionIndex", JSON.stringify(currentQuestionIndex));
    }, [currentQuestionIndex]);

    useEffect(() => {
        localStorage.setItem("answers", JSON.stringify(answers));
    }, [answers]);

    useEffect(() => {
        localStorage.setItem("summary", JSON.stringify(summary));
    }, [summary]);

    useEffect(() => {
        localStorage.setItem("score", JSON.stringify(score));
    }, [score]);

    // Extract fetch logic into a function so we can call it on mount or on reset
    const initializeContent = async () => {
        try {
            const res = await axios.get(`${BASE_URL}/generate-summary-and-questions`, { 
                params: { section: currentModule } 
            });
            setSummary(res.data.summary);
            setQuestions(res.data.questions);
            dataFetched.current = true;
        } catch (error) {
            console.error("Error fetching summary and questions:", error);
        }
    };

    // Fetch document once when the component mounts
    useEffect(() => {
        const fetchDocument = async () => {
            try {
                const res = await axios.get(`${BASE_URL}/retrieve-document`);
                // setDocument(res.data.document); // Uncomment if needed
            } catch (error) {
                console.error("Error fetching document:", error.response || error);
            }
        };
        fetchDocument();
    }, []);

    // Fetch summary and questions on page load if not already saved in localStorage
    useEffect(() => {
        if (!questions.length || !summary) {
            initializeContent();
        }
    }, []); // Runs once on mount

    // Reset function to clear stored state and re-fetch content
    const handleReset = async () => {
        // Clear localStorage
        localStorage.removeItem("questions");
        localStorage.removeItem("currentQuestionIndex");
        localStorage.removeItem("answers");
        localStorage.removeItem("summary");
        localStorage.removeItem("score");

        // Reset state variables
        setQuestions([]);
        setCurrentQuestionIndex(0);
        setAnswers([]);
        setSummary('');
        setScore(0);

        // Optionally reset other state variables if needed (like currentModule)
        setCurrentModule('6.1');
        dataFetched.current = false; // allow re-fetching

        // Re-fetch the summary and questions without reloading the entire page
        await initializeContent();
    };

    // Function to update summary and append new questions
    const updateSummaryAndQuestions = async () => {
        if (nextSectionClicked) return; // Prevent further clicks if already clicked
        
        try {
            setNextSectionClicked(true); // Disable button when clicked

            const res = await axios.get(`${BASE_URL}/generate-summary-and-questions`,
                { params: { section: incrementModule(currentModule) } }
            );

            // Increment the module number
            const newModule = incrementModule(currentModule);
            setCurrentModule(newModule);

            // Update the summary
            setSummary(res.data.summary);

            // Append new questions to existing questions
            setQuestions((prevQuestions) => [...prevQuestions, ...res.data.questions]);

            setNextSectionClicked(false);
        } catch (error) {
            console.error("Error updating summary and questions:", error);
        }
    };

    // Function to increment the module (e.g., 1.1 -> 1.2, 2.4 -> 2.5)
    const incrementModule = (module) => {
        const [chapter, section] = module.split('.').map(Number);
        const updatedSection = section + 1;
        return `${chapter}.${updatedSection}`;
    };

    // Function to handle user submissions
    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitDisabled(true);

        try {
            const userAnswer = answer;
            const res = await axios.post(`${BASE_URL}/query`, { 
                question: questions[currentQuestionIndex], 
                user_answer: userAnswer,
                summary: summary
            });

            setAnswers([
                ...answers,
                { 
                    question: questions[currentQuestionIndex], 
                    user_answer: userAnswer, 
                    response: res.data.response, 
                    score: res.data.score 
                }
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

    // Auto-scroll to the bottom of the chat container whenever the questions or answers change
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [answers, currentQuestionIndex]);

    // If summary or questions are not loaded yet, show a loading message
    if (!summary || questions.length === 0) {
        return (
            <div className="app-container">
                <p>Loading...</p>
            </div>
        );
    }

    return (
        <div className="app-container">
            <div className="summary-container">
                <div className="summary-header">
                    <h3>
                        Psychology2e Section {currentModule} Summary:
                        <button onClick={handleReset} className="reset-button">Reset Page</button>
                    </h3>
                </div>
                <p className="summary-content">{summary}</p>
            </div>
            <div className="chat-container" ref={chatContainerRef}>
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
                                <br />
                                <strong>Score:</strong> {answers[index].score}
                            </div>
                        )}
                    </div>
                ))}
            </div>
            {currentQuestionIndex < questions.length && (
                <form className="input-form" onSubmit={handleSubmit}>
                    <input
                        type="text"
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                        placeholder="Your Answer"
                    />
                    {currentQuestionIndex > 0 && (
                        <div className="current-question">
                            <h4>Current Score: {score}/{currentQuestionIndex * 10}</h4>
                        </div>
                    )}
                    <button type="submit" disabled={submitDisabled}>Submit</button>
                </form>
            )}
            {currentQuestionIndex >= questions.length && currentQuestionIndex > 1 && (
                <div className="completion-container">
                    <p className="completion-message">All questions answered in section {currentModule}!</p>
                    {currentQuestionIndex > 0 && (
                        <div className="current-question">
                            <h4>Current Score: {score}/{currentQuestionIndex * 10}</h4>
                        </div>
                    )}
                    {currentModule !== "6.4" && (
                        <button 
                            className="next-section-button" 
                            onClick={updateSummaryAndQuestions} 
                            disabled={nextSectionClicked}
                        >
                            Move to section {incrementModule(currentModule)}
                        </button>
                    )}
                </div>
            )}
        </div>
    );
};

export default App;
