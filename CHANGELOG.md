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

### Next Steps (Current branch only)
- Fix an issue where accessing the program through a domain name listing causes the connection between backend and frontend to be severed.