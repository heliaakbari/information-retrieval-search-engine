import re
import json
from parsivar import FindStems
from general_normalization import General_normalization
normalizer = General_normalization();
stemmer = FindStems()

f = open('docs/IR_data_news.json',encoding="utf-8")
data = json.load(f)
f.close()
terms = []
pos_index = {}
for docno in data:
    doc = data[str(docno)]["content"]
    normalized_doc = normalizer.normalize(doc).strip()
    tokenized_doc = re.split(r'\s+', normalized_doc)
    if docno == "0": 
        with open("docs/docs0_normalized.txt", "w",encoding="utf-8") as outfile: 
            outfile.write(str(normalized_doc))
        with open("docs/docs0_tokenized.txt", "w",encoding="utf-8") as outfile: 
            outfile.write(" ")
        with open("docs/docs0_stemmed.txt", "w",encoding="utf-8") as outfile: 
            outfile.write(" ")
    
        with open("docs/final_tokens.txt", "w",encoding="utf-8") as outfile: 
            outfile.write(" ")
    
        with open("docs/docs0_stemmed_diff.txt", "w",encoding="utf-8") as outfile: 
            outfile.write(" ")
        
        for token in tokenized_doc:
            with open("docs/docs0_tokenized.txt", "a",encoding="utf-8") as outfile: 
                outfile.write("'"+token+"'"+" ")

    for pos, term in enumerate(tokenized_doc):   
        term = stemmer.convert_to_stem(term).split('&')[0]
        if docno == "0":    
            terms.append(term)
            with open("docs/docs0_stemmed.txt", "a",encoding="utf-8") as outfile: 
                outfile.write("'"+term+"'"+" ")
            with open("docs/docs0_stemmed_diff.txt", "a",encoding="utf-8") as outfile: 
                if tokenized_doc[pos] != term :
                    outfile.write("'"+tokenized_doc[pos]+"->"+term+"'"+" ")
        # If term already exists in the positional index dictionary.
        if term in pos_index:
            # Check if the term has existed in that DocID before.
            if docno in pos_index[term][1]:
                #pos_index[term][1][docno][1].append(pos) 
                pos_index[term][1][docno][0] += 1   
                pos_index[term][1][docno][1].append(pos)   
            else:
                # Increment total freq by 1.
                pos_index[term][0] = pos_index[term][0] + 1
                pos_index[term][1][docno] = []
                pos_index[term][1][docno].append(1)
                pos_index[term][1][docno].append([pos])
 
        # If term does not exist in the positional index dictionary 
        # (first encounter).
        else:
            # Initialize the list.
            pos_index[term] = []
            # The total frequency is 1.
            pos_index[term].append(1)
            # The postings list is initially empty.
            pos_index[term].append({})      
            # Add doc ID to postings list.
            pos_index[term][1][docno] = []
            pos_index[term][1][docno].append(1)
            pos_index[term][1][docno].append([pos])

sorted_pos_index = sorted(pos_index.items(), key=lambda x:x[1][0],reverse=True)
file2 = open("docs/max_freq_deleted.txt", "w",encoding="utf-8")
for i in range(30) :
    del_token = sorted_pos_index.pop(0)
    file2.write(del_token[0]+" "+str(del_token[1][0])+" \n");
    while terms.__contains__(del_token[0]):
        terms.remove(del_token[0])
file2.close()
sorted_pos_index = dict(sorted_pos_index)
with open("docs/pos_index.json", "w") as outfile: 
    json.dump(sorted_pos_index,outfile,indent=None)

with open("docs/final_tokens.txt", "a", encoding="utf-8") as outfile:  
    for term in terms:
         outfile.write("'"+term+"'"+" ")
