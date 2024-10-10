import numpy as np
import math
#Write a Python application program (main file called DocSearch.py) thatimplements document searching based on vector-based document matching aswell as inverted index


#building the dictionary
unique_words = {}

docs = open("docs.txt","r")
for line in docs:
    words = line.split() 
    for word in words:
        if word not in unique_words:
            unique_words[word] = True   
    

docs.close()
print("Words in dictionary:", len(unique_words))
#print(unique_words)

#building an inverted index
inverted_index = {}

docs = open("docs.txt","r")
line_count = 1
for line in docs:
    words = line.split() 
    for word in words:
        if word in inverted_index:
            inverted_index[word].add(line_count)
        else:
            inverted_index[word] = {line_count}
    line_count += 1
docs.close()

#print(inverted_index)

# Document searching - queries
queries = open("queries.txt", "r")

for query in queries:
    query = query.strip() 
    print("Query:", query)

    relevant_docs = []
    for word in query.split():
        if word in inverted_index:
            if not relevant_docs:
                relevant_docs.extend(inverted_index[word])
            else:
                relevant_docs = [doc_id for doc_id in inverted_index[word] if doc_id in relevant_docs]
    
    print("Relevant documents:", " ".join(map(str, relevant_docs)))

    # Working out vectors and angles
    # Let x = doc vector, y = query vector
    angle_doc = {}
    for doc_id in relevant_docs:
        # Doc vector
        x = np.zeros(len(unique_words))

        docs = open("docs.txt","r")
        for i, line in enumerate(docs, 1):
            if i == doc_id:
                words = line.split()
                for word in words:
                    if word in unique_words:
                        index = list(unique_words.keys()).index(word)
                        x[index] += 1 
                break

        # Query vector
        y = np.zeros(len(unique_words))
        docs = open("docs.txt", "r")
        for i, line in enumerate(docs, 1):
            if i == doc_id:
                words = line.split()
                
                for word in query.split():
                    if word in words:
                        index = list(unique_words.keys()).index(word)
                        y[index] = 1
                break
        docs.close()

        # Angle calc
        norm_x = np.linalg.norm(x)
        norm_y = np.linalg.norm(y)
        cos_theta = np.dot(x,y) / (norm_x * norm_y)
        theta = math.degrees(math.acos(cos_theta))

        theta = round(theta, 5)
        angle_doc[doc_id] = theta
    
    # Sort angles and print
    sorted_angles = sorted(angle_doc.items(), key=lambda x: x[1])
    for key, value in sorted_angles:                
        print(key, value)

queries.close()


