import csv
import math
import json
import os
# from rapidfuzz import fuzz
from tree import *


class searchEngine:
    def __init__(self, filename):
        self.filename = filename
    
    def readDatabase(self):
        self.dataList = []
        count = 0
        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                # Extract: title, overview, tags, genres, director, actors, popularity, rating, budget
                movie_data = [
                    row.get('title', ''),
                    row.get('overview', ''),
                    row.get('tags', ''),
                    row.get('genres', ''),
                    row.get('director', ''),
                    row.get('actors', ''),
                    row.get('popularity', '0'),
                    row.get('rating', '0'),
                    row.get('budget', '0')
                ]
                self.dataList.append(movie_data)
                count += 1     
         
    def createInvertedIndex(self):
        # Check if inverted index already exists in JSON
        index_file = "inverted_index.json"
        if os.path.exists(index_file):
            with open(index_file, 'r') as f:
                self.invertedIndex = json.load(f)
            print("Inverted index loaded from cache with " + str(len(self.invertedIndex.keys())) + " unique words.")
            return
        
        self.invertedIndex = {}
        id = 0
        for item in self.dataList:
            # Skip popularity (item[6]) - index only up to item[5] (actors)
            for i in range(1, 6):
                tokens = item[i].split(" ")
                for token in tokens:
                    onlyToken = ''.join(c for c in token if c.isalnum()).lower()
                    if (onlyToken in self.invertedIndex.keys()):
                        self.invertedIndex[onlyToken].append(id)
                    else:
                        self.invertedIndex[onlyToken] = [id]
                    self.invertedIndex[onlyToken] = list(set(self.invertedIndex[onlyToken]))
            id += 1
        
        # Save inverted index to JSON
        with open(index_file, 'w') as f:
            json.dump(self.invertedIndex, f)
        print("Inverted index created with " + str(len(self.invertedIndex.keys())) + " unique words.")
    
    def createTree(self):
        # Check if tree already exists in JSON
        tree_file = "tree.json"
        if os.path.exists(tree_file):
            with open(tree_file, 'r') as f:
                tree_data = json.load(f)
            self.tree = Tree()
            self.tree.deserialize(tree_data)
            print("Tree loaded from cache with " + str(len(self.invertedIndex.keys())) + " words.")
            return
        
        self.tree = Tree(list(self.invertedIndex.keys()))
        
        # Save tree to JSON
        with open(tree_file, 'w') as f:
            json.dump(self.tree.serialize(), f)
        print("Tree created with " + str(len(self.invertedIndex.keys())) + " words.")

    def setIntersection(self, a, b):
        intersection = []
        pointer1 = 0
        pointer2 = 0
        while (pointer1 < len(a) and pointer2 < len(b)):
            e1 = a[pointer1]
            e2 = b[pointer2]
            if (e1 == e2):
                intersection.append(e1)
                pointer1 += 1
                pointer2 += 1
            elif (e1 < e2):
                pointer1 += 1
            elif (e1 > e2):
                pointer2 += 1
            # print(e1, e2)
                
        return intersection       
    
    def setUnion(self, a, b):
        union = []
        pointer1 = 0
        pointer2 = 0

        while pointer1 < len(a) and pointer2 < len(b):
            e1 = a[pointer1]
            e2 = b[pointer2]

            if e1 == e2:
                if not union or union[-1] != e1:
                    union.append(e1)
                pointer1 += 1
                pointer2 += 1

            elif e1 < e2:
                if not union or union[-1] != e1:
                    union.append(e1)
                pointer1 += 1

            else:
                if not union or union[-1] != e2:
                    union.append(e2)
                pointer2 += 1

        while pointer1 < len(a):
            if not union or union[-1] != a[pointer1]:
                union.append(a[pointer1])
            pointer1 += 1

        while pointer2 < len(b):
            if not union or union[-1] != b[pointer2]:
                union.append(b[pointer2])
            pointer2 += 1

        return union
      
    def autoComplete(self, word):
        # Use tree to find possible completions
        node = self.tree.root
        prefix = word
        
        # Traverse the tree following the input word
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # Word prefix not found in tree
                return []
        
        # DFS to find all words that start with the given prefix
        completions = []
        def dfs(node, path):
            if node.is_word:
                completions.append(path)
            for char, child in node.children.items():
                dfs(child, path + char)
        
        dfs(node, prefix)
        
        return completions
    
    def spellCheck(self, word, max_distance):
        # use tree to find possible corrections
        # check for words within 2 edits (insertions, deletions, substitutions)
        spellCorrections = []
                
        def dfs_with_distance(node, word, index, current_distance, path):
            # If we've exceeded max distance, prune this branch
            if current_distance > max_distance:
                return
            
            # If we've processed all characters in word
            if index == len(word):
                # Allow remaining characters in tree (insertions)
                def find_words(n, dist, p):
                    if dist > max_distance:
                        return
                    if n.is_word:
                        spellCorrections.append(p)
                    for char, child in n.children.items():
                        find_words(child, dist + 1, p + char)
                
                find_words(node, current_distance, path)
                return
            
            current_char = word[index]
            
            # Try matching the current character (no edit needed)
            if current_char in node.children:
                dfs_with_distance(node.children[current_char], word, index + 1, current_distance, path + current_char)
            
            # Try substitution (replace current char with any child char)
            for char, child in node.children.items():
                if char != current_char:
                    dfs_with_distance(child, word, index + 1, current_distance + 1, path + char)
            
            # Try deletion (skip current character in word)
            dfs_with_distance(node, word, index + 1, current_distance + 1, path)
            
            # Try insertion (add a character from tree without advancing in word)
            for char, child in node.children.items():
                dfs_with_distance(child, word, index, current_distance + 1, path + char)
        
        dfs_with_distance(self.tree.root, word, 0, 0, "")
        
        return spellCorrections
        
    def search(self, query):
        tokens = query.split(" ")
        scores = {}
        
        newTokens = []
        for token in tokens:
            onlyToken = ''.join(c for c in token if c.isalnum()).lower()
            if onlyToken in self.invertedIndex:
                newTokens.append(onlyToken)
            else:
                newTokens.extend(self.autoComplete(onlyToken))
                # If no tokens found within 1 edit, try 2 edits, then 3 edits
                spellchecks = self.spellCheck(onlyToken, 1)
                if (len(spellchecks) < 3):
                    spellchecks = self.spellCheck(onlyToken, 2)
                    if (len(spellchecks) < 3):
                        spellchecks = self.spellCheck(onlyToken, 3)
                newTokens.extend(spellchecks)
        print(newTokens)
            
        for token in newTokens:
            onlyToken = ''.join(c for c in token if c.isalnum()).lower()

            if onlyToken not in self.invertedIndex:
                continue
            
            frequency = len(self.invertedIndex[onlyToken])
            idf = math.log(len(self.dataList) / frequency) if frequency > 0 else 0
            for docID in self.invertedIndex[onlyToken]:

                # Initialize score if first time seeing doc
                if docID not in scores:
                    scores[docID] = 0

                # Check if token is in title
                title = self.dataList[docID][0].strip().lower()
                
                # Title match (10 points for strong relevance)
                if onlyToken in title:
                    scores[docID] += 10 * idf
                
                # Description match (1 point)
                else:
                    scores[docID] += 1 * idf
        
        if not scores:
            return ["There are no results"]

        # Sort by relevance score (highest first)
        rankedDocs = sorted(scores.items(), key=lambda x: -x[1])
        
        # Take top 20 by relevance
        top_20 = rankedDocs[:20]
        
        if not top_20:
            return ["There are no results"]
        
        # Normalize relevance scores to 0-100
        max_relevance_score = top_20[0][1]
        normalized_scores = {}
        for docID, rel_score in top_20:
            normalized_rel = (rel_score / max_relevance_score) * 100 if max_relevance_score > 0 else 0
            
            # Get popularity and normalize to 0-100
            try:
                popularity = float(self.dataList[docID][6])
            except (ValueError, IndexError):
                popularity = 0
            
            # Get rating and normalize to 0-100 (ratings are 0-10)
            try:
                rating = float(self.dataList[docID][7])
            except (ValueError, IndexError):
                rating = 0
            normalized_rating = (rating / 10) * 100 if rating > 0 else 0
            
            # Get budget and normalize to 0-100 (normalize based on reasonable budget range)
            try:
                budget = float(self.dataList[docID][8])
            except (ValueError, IndexError):
                budget = 0
            # Normalize budget (assuming max budget around 10 billion)
            normalized_budget = min((budget / 10000000000) * 100, 100) if budget > 0 else 0
            
            # Normalize popularity (assuming popularity ranges roughly 0-10000)
            normalized_pop = min((popularity / 100), 100)  # Cap at 100
            
            # Final score: 70% relevance + 10% popularity + 10% rating + 10% budget
            final_score = (normalized_rel * 0.70) + (normalized_pop * 0.10) + (normalized_rating * 0.10) + (normalized_budget * 0.10)
            normalized_scores[docID] = final_score
        
        # Sort by final score
        finalRankedDocs = sorted(normalized_scores.items(), key=lambda x: -x[1])

        movies = []
        maxCap = 10

        for docID, score in finalRankedDocs[:maxCap]:
            movies.append(self.dataList[docID][0] + " (Score: " + str(round(score, 2)) + ")")

        return movies


searcher = searchEngine("movies copy.csv")

searcher.readDatabase()

searcher.createInvertedIndex()

searcher.createTree()

# print(searcher.setIntersection([1, 2, 3, 4, 7, 8], [3, 7, 8, 9, 67]))

# print(searcher.search("john wick"))
# print(searcher.tree.print_visual())

print(searcher.autoComplete("aven"))# should find avengers

print(searcher.spellCheck("aven", 1))# should find avengers
