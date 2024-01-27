
import json
import math

with open('docs/pos_index.json') as json_file:
    pos_index = json.load(json_file)
N= 12202

tf_idf = {}
doc_squared = {}
for term in pos_index:
    tf_idf[term]=[]
    tf_idf[term].append(pos_index[term][0])
    tf_idf[term].append({})
    for docno in pos_index[term][1] : 
        tf_idf[term][1][docno]= ( 1 + math.log2(pos_index[term][1][docno][0])) # * math.log2(N/pos_index[term][0])
        if docno in doc_squared:
            doc_squared[docno]+=  math.pow(tf_idf[term][1][docno],2)
        else :
            doc_squared[docno] = math.pow(tf_idf[term][1][docno],2)

for doc in doc_squared:
    doc_squared[doc] = math.sqrt(doc_squared[doc]);


with open("docs/doc_vector_size.json", "w") as outfile: 
    json.dump(doc_squared,outfile,indent=None)

with open("docs/tf_idf_docs.json", "w") as outfile: 
    json.dump(tf_idf,outfile,indent=None)

        