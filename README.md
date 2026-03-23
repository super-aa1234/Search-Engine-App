# Movie Search Engine

A movie search engine built with Flask that combines information retrieval techniques with ranking algorithms to deliver relevant search results.

## Features
- **Inverted Index**: Fast O(1) lookup of movies by keywords using an inverted index data structure
- **Tree**: Precomputed Tree of words allows fast autocomplete and spell check of words. 
- **TF-IDF Scoring**: Relevance ranking using Term Frequency-Inverse Document Frequency algorithm
- **Tree-based Autocomplete**: Efficient prefix-based suggestions as users type
- **Spell Checking**: Intelligent typo correction using modified DFS on tree with edit distance constraints (up to 3 edits)
- **JSON Caching**: Inverted index and tree are cached to JSON for fast reloads


### Ranking
Results are ranked based on a weighted combination of factors:
- **70% Relevance**: TF-IDF score with 10x boost for title matches vs description matches
- **10% Popularity**: Trending score from The Movie Database (TMDb)
- **10% Rating**: User review scores (0-10 scale)
- **10 Budget**: Production budget (indicates major studio releases)

### Algorithm:
1. Splits query into tokens
2. Uses inverted-index to find relevant results for each token
3. If tokens not in inverted-index uses spell-check and autocomplete to find matches
4. Ranks based on TF-IDF and 10x weight for token in title vs description
5. Takes top 20 candidates
4. Normalizes all factors(rating, popularity, etc.) to 0-100 scale and does weighted average.
5. Takes final top 10 in ranked order. 

## Getting Started

### Prerequisites
- Python 3.7+
- pip

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd searchEngineApp
```

2. Install dependencies
```bash
pip install flask
```

3. Run the application
```bash
flask --app app run --debug
```

Visit `http://localhost:5000` in your browser.


