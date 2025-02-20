## [Unreleased] - 2/7/2025 - Steven Akiyama
### Added
- Program now uses retrieval-augmented generation (RAG) using a basic, static retriever.
- Added the CHANGELOG.md file
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