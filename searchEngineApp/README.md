# Movie Search Engine

A sophisticated full-stack movie search engine built with Flask that combines information retrieval techniques with intelligent ranking algorithms to deliver relevant and engaging search results.

## Features

### 🔍 Smart Search
- **Inverted Index**: Fast O(1) lookup of movies by keywords using an inverted index data structure
- **TF-IDF Scoring**: Relevance ranking using Term Frequency-Inverse Document Frequency algorithm
- **Trie-based Autocomplete**: Efficient prefix-based suggestions as users type
- **Spell Checking**: Intelligent typo correction using modified DFS on a trie with edit distance constraints (up to 3 edits)

### 📊 Advanced Ranking Algorithm
Results are ranked based on a weighted combination of factors:
- **75% Relevance**: TF-IDF score with 2x boost for title matches vs description matches
- **15% Popularity**: Trending score from The Movie Database (TMDb)
- **5% Rating**: User review scores (0-10 scale)
- **5% Budget**: Production budget (indicates major studio releases)

The algorithm:
1. Filters results by relevance (top 20)
2. Normalizes all factors to 0-100 scale
3. Combines weights to produce final score between 0-100

### ⚡ Performance Optimizations
- **JSON Caching**: Inverted index and trie tree are cached to JSON for fast reloads
- **On-demand Tree Deserialization**: Tree is reconstructed from JSON only when needed
- **Efficient Data Structures**: 
  - Trie for autocomplete and spell checking
  - Inverted index for full-text search
  - Set operations for query filtering

## Architecture

```
searchEngineApp/
├── app.py                 # Flask web application
├── search.py              # Core search engine logic
├── tree.py                # Trie data structure for autocomplete/spell check
├── templates/
│   └── index.html         # Web UI
├── movies copy.csv        # Movie dataset (~9,780 movies)
├── inverted_index.json    # Cached inverted index
└── tree.json              # Cached trie structure
```

## Technology Stack

- **Backend**: Python 3, Flask
- **Data Structures**: Trie, Inverted Index
- **Algorithms**: TF-IDF, Levenshtein Distance, DFS
- **Data**: Movie database with title, overview, genres, actors, ratings, popularity, and budget

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

## How It Works

### Indexing Phase
1. **Read Database**: Load movies from CSV file
2. **Build Inverted Index**: Create token → [docIDs] mappings
3. **Build Trie**: Construct prefix tree from all indexed terms
4. **Cache to JSON**: Save structures for fast future loads

### Search Phase
1. **Tokenize Query**: Split into individual terms
2. **Resolve Unknown Terms**:
   - Check inverted index for exact matches
   - Use autocomplete (trie traversal) for partial matches
   - Use spell check (modified DFS with edit distance) for typos
3. **Calculate Relevance Scores**:
   - TF-IDF for each token
   - Title matches weighted 2x higher than description matches
4. **Apply Multi-factor Ranking**:
   - Normalize relevance, popularity, rating, and budget to 0-100
   - Calculate weighted final score
5. **Return Top 10 Results**

### Spell Checking Algorithm
The spell checker uses a modified DFS on the trie that tracks edit distance:
- **Substitution**: Replace character (cost: 1)
- **Deletion**: Remove character (cost: 1)
- **Insertion**: Add character (cost: 1)
- **Match**: No cost

It progressively tries edit distances 1, 2, then 3 until it finds at least 3 suggestions.

## Example Searches

- **Exact match**: "Avengers" → Returns Avengers movies with highest relevance
- **Partial match**: "aven" → Autocompletes to "avengers", "avenged", etc.
- **Typo correction**: "avangers" → Suggests "avengers" (1 edit away)
- **Multi-word**: "batman superman" → Boosts Batman v Superman due to both tokens in title

## Performance

- **Startup**: ~1-2 seconds (or instant with cached JSON)
- **Search**: <100ms for most queries
- **Index Size**: ~60K unique terms
- **Dataset**: 9,780 movies

## Future Enhancements

- Add collaborative filtering for personalized recommendations
- Implement phrase matching for multi-word queries
- Add genre-based filtering
- Include voice search capability
- Expand to TV shows and cast information
- Add search history and trending searches

## License

MIT License

## Author

Developed as a learning project in information retrieval and web development.
