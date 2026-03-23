# Movie Search Engine

A movie search engine built with Flask that combines information retrieval techniques with ranking algorithms to deliver relevant search results.

## Features
- **Inverted Index**: Fast O(1) lookup of movies by keywords using an inverted index data structure
- **TF-IDF Scoring**: Relevance ranking using Term Frequency-Inverse Document Frequency algorithm
- **Tree-based Autocomplete**: Efficient prefix-based suggestions as users type
- **Spell Checking**: Intelligent typo correction using modified DFS on a tree with edit distance constraints (up to 3 edits)

### Ranking
Results are ranked based on a weighted combination of factors:
- **70% Relevance**: TF-IDF score with 10x boost for title matches vs description matches
- **10% Popularity**: Trending score from The Movie Database (TMDb)
- **10% Rating**: User review scores (0-10 scale)
- **10 Budget**: Production budget (indicates major studio releases)

The algorithm:
1. Filters results by relevance (top 20) using inverted index and TF-IDF
2. Normalizes all factors to 0-100 scale
3. Combines weights to produce final score between 0-100

### ⚡ Performance Optimizations
- **JSON Caching**: Inverted index and trie tree are cached to JSON for fast reloads
- **On-demand Tree Deserialization**: Tree is reconstructed from JSON only when needed
- **Efficient Data Structures**: 
  - Trie for autocomplete and spell checking
  - Inverted index for full-text search
  - Set operations for query filtering
 
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


