import pytest
from unittest.mock import MagicMock, patch
from tutorai import TutorAI


@pytest.fixture
def mock_openai():
    """Fixture to mock OpenAI API."""
    with patch("tutorai.OpenAI") as mock_openai_class:
        mock_openai_instance = MagicMock()
        mock_openai_class.return_value = mock_openai_instance
        yield mock_openai_instance


@pytest.fixture
def tutor_ai(mock_openai):
    """Fixture to initialize TutorAI with mocked OpenAI."""
    return TutorAI(api_key="test_api_key")


def test_initialization(tutor_ai):
    """Test the initialization of the TutorAI class."""
    assert tutor_ai.rec_accuracy == 0.85
    assert tutor_ai.req_accuracy == 0.6
    assert tutor_ai.system_message.startswith("You are a kind and helpful tutor")


def test_set_document_text(tutor_ai):
    """Test the set_document_text method."""
    new_text = "This is a new document."
    tutor_ai.set_document_text(new_text)
    assert tutor_ai.document_text == new_text


def test_summarize_text(tutor_ai, mock_openai):
    """Test the summarize_text method."""
    mock_openai.invoke.return_value = "Mocked Summary"
    tutor_ai.summarization_chain = MagicMock()
    tutor_ai.summarization_chain.invoke.return_value = "Mocked Summary"

    summary = tutor_ai.summarize_text()
    assert summary == "Mocked Summary"
    tutor_ai.summarization_chain.invoke.assert_called_once_with({"text": tutor_ai.document_text})


def test_shortanswer_questions(tutor_ai, mock_openai):
    """Test the shortanswer_questions method."""
    mock_openai.invoke.return_value = "Question 1\nQuestion 2\nQuestion 3"
    tutor_ai.shortanswer_question_chain = MagicMock()
    tutor_ai.shortanswer_question_chain.invoke.return_value = "Question 1\nQuestion 2\nQuestion 3"

    questions = tutor_ai.shortanswer_questions(count=3)
    assert questions == ["Question 1", "Question 2", "Question 3"]
    tutor_ai.shortanswer_question_chain.invoke.assert_called_once_with(
        {"count": 3, "text": tutor_ai.document_text}
    )


def test_multiplechoice_questions(tutor_ai, mock_openai):
    """Test the multiplechoice_questions method."""
    mock_openai.invoke.return_value = '{"question": "Mock question", "options": ["a", "b", "c"]}'
    tutor_ai.multiplechoice_question_chain = MagicMock()
    tutor_ai.multiplechoice_question_chain.invoke.return_value = (
        '{"question": "Mock question", "options": ["a", "b", "c"]}'
    )

    questions = tutor_ai.multiplechoice_questions(count=1, text="Sample text")
    assert questions == ['{"question": "Mock question", "options": ["a", "b", "c"]}']
    tutor_ai.multiplechoice_question_chain.invoke.assert_called_once_with(
        {"count": 1, "text": "Sample text"}
    )


def test_shortanswer_evaluate(tutor_ai, mock_openai):
    """Test the shortanswer_evaluate method."""
    mock_openai.invoke.return_value = "Score: 9\nEvaluation: Great answer."
    tutor_ai.shortanswer_evaluation_chain = MagicMock()
    tutor_ai.shortanswer_evaluation_chain.invoke.return_value = "Score: 9\nEvaluation: Great answer."

    evaluation, score = tutor_ai.shortanswer_evaluate(
        question="What is AI?", answer="Artificial Intelligence."
    )
    assert evaluation == "Great answer."
    assert score == "9"
    tutor_ai.shortanswer_evaluation_chain.invoke.assert_called_once_with(
        {"text": tutor_ai.document_text, "question": "What is AI?", "answer": "Artificial Intelligence."}
    )


def test_default_document_text(tutor_ai):
    """Test that the default document text is set correctly."""
    assert "psychological disorder" in tutor_ai.document_text


def test_empty_text_fallback(tutor_ai, mock_openai):
    """Test handling of empty text input in summarize_text."""
    tutor_ai.summarization_chain = MagicMock()
    tutor_ai.summarization_chain.invoke.return_value = "Fallback summary"

    result = tutor_ai.summarize_text(text="")
    assert result == "Fallback summary"
    tutor_ai.summarization_chain.invoke.assert_called_once_with({"text": tutor_ai.document_text})
