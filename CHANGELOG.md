## [Unreleased] - 2/7/2025 - Steven Akiyama
## RAG Release
### Added
- Program now uses retrieval-augmented generation (RAG) using a basic, static retriever.
- Added the `CHANGELOG.md` file
- Created QdrantConnect, a class for retrieving points from a Qdrant Cloud DB

### Changed
- README and backend updated to reflect additions

### Fixed
- Fixed an issue where pressing the submit button multiple times before await completed would cause multiple API calls.
- Fixed an issue where edits in the submission window would cause the textbook content to be re-rendered

### Removed
- Removed shortanswer_complete_terminal, as it was depreciated and no longer functional.
- Removed vdatabase, as it wasn't implemented. 

### Next Steps
- Fix an issue where accessing the program through a domain name listing causes the connection between backend and frontend to be severed.

## [Unreleased] - 2/16/2025 - Steven Akiyama
## Chapter Progression Release
### Added
- Added the ability for users to generate and append new questions from the next subsection of the textbook.
- Added a button to do this, that displays once all submissions have been sent.

### Changed
- Modified the front-end to only show submission button & window when not all questions are answered.
- Modified the chatlogs to contain a scrolly, so the summary is always visible.

### Fixed
- Fixed an issue where accessing the program through a domain name caused the connection to fail.

### Removed
- Removed textbook content visualization, as it wasn't user-friendly post RAG implementation.

### Next Steps
- Possibly add a PDF viewer?

### Known Issues 
- New questions is oblivious to chapters (Will continue past the end of a chapter, i.e. if chapter 6 ends at 6.5, the program will continue to a non-existant 6.6, 6.7 etc.)
- Not a full issue, but currently has no memory between page loads. This is apparent with multiple subchapter usage.

## [v1.1.0] - 2/19/2025 - Steven Akiyama
## Hotfix & QOL
### Changed
- Modified the UI to better accomadate the new chatlogging.

### Fixed
- Fixed an issue with moving through sections. Questions button is still oblivious to chapters, but is hidden at the end of chapter 6 (Hard-coded)

### Next Steps
- Add options to switch between chapters
- Make chapter stopping dynamic
- Add loading notifications
- Integrate MCQs
- Integrate chatlogging

## [v1.2.0] - 2/23/2025 - Steven Akiyama
## Logging, UI & Refactoring
### Added
- Introduced `logger.py` and updated other files to integrate logging. This enhances debugging and will facilitate future improvements. Logs are stored in `app.log`.

**backend/main.py**:
- Added `qdrant_search()`, centralizing the response setup for retrieval from QDrant.

### Changed
**backend/tutorai.py**:
- Modified LLM responses to be more direct (e.g., "Your answer was fantastic!" instead of "The student's answer was fantastic!").
- Refined prompt templates for better engineering.
- Refactored LLM method calls to always require a `text` argument (formerly `text=None`).
- Added error logging for missing `text` argument.
- Implemented max-length handling for LLM inputs and responses to prevent exceeding the max token count.

**backend/main.py**:
- Set section 1.1 as the default if no value is passed. (It should always receive a value!)
- Updated `/generate-summary-and-questions` to use the generated summary for question generation. This improves response accuracy but may increase response times.
- Modified queries to return the summary for short answer evaluation, enhancing LLM responses.

**backend/qdrant.py**:
- Changed return values for each getter to return a dictionary containing title, chapter, and text. Adjusted corresponding methods/files to accommodate this change.

**frontend-react/App.jsx**:
- Updated `/query` call to include the summary, as reflected in `tutorai.py`.
- Modified the UI to display "Psychology2e" in the section header and changed it from `h4` to `h3` (slightly smaller).
- Moved the score display to align horizontally with the form submission and next section buttons, maximizing space for other UI elements.

**app/App.css**:
- Improved alignment in `.current_question` structure to accommodate the score display change.
- Enhanced `.current_question` structure for better responsiveness across screen sizes.

### Fixed
- Fixed an issue where the summary and questions failed to properly update for the new section.

**backend/tutorai.py**:
- Fixed an issue where a score of "N/A" from the LLM broke the score display in `frontend-react`. Now, `shortanswer_evaluate` returns `0` if no numerical value is passed.

**frontend-react/index.html**:
- Fixed an issue where mobile users experienced automatic zoom when typing a response. (UNCONFIRMED)

### Removed
**backend/tutorai.py**:
- Removed `document_text` as it is no longer necessary (all LLM calls now use QDrant data).

**frontend-react/App.jsx**:
- Removed the "TutorAI: Textbook Learning Assistant" header for a cleaner page layout, making space for more content.

### Next Steps
- Add options to switch between chapters.
- Make chapter stopping dynamic.
- Add loading notifications.
- Integrate MCQs.

### Known Issues
**backend/tutorai.py**:
- Summaries are occasionally cut off due to token count limitations.

## [v1.2.1] - 2/23/2025 - Steven Akiyama
## Small Hotfix
### Changed
**frontend-react\App.css**
- Updated the textbook summary area to include a scrolly, and only take max 40% of page size.

## [v1.2.2] - 2/23/2025 - Steven Akiyama
## LocalStorage, UI, App.jsx Refactor
### Added
**frontend-react\App.jsx**
- Added local storage for the tutor. No more constant reloads!
- Added a button to reload the content. (More constant reloads?)
- Added a loading message while content is loading.

### Changed
**frontend-react\App.jsx**
- Refactored a lot of the code! Figured I might as well, since I was already implementing a lot here.

**frontend-react\App.css**
- Shrunk some padding/margins to allow for more content on screen.

### Fixed
**backend\tutorai.py**
- Fixed an issue where LLM responses were cut off by token maxing. It's still somewhat possible, but *should* happen less frequently now.

### Next Steps
- Add options to switch between chapters.
- Make chapter stopping dynamic.
- Integrate MCQs.