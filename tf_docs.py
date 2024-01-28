
import json
import math
import itertools
with open('docs/pos_index.json') as json_file:
    pos_index = json.load(json_file)

tf_idf = {}
doc_squared = {}
#champions list maker:
champions_list ={}
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
    #making champions list:
    champions_list[term] = []
    sorted_frequency = sorted(tf_idf[term][1].items(), key= lambda x : x[1], reverse=True)
    for i in range(min(50,len(sorted_frequency))):
        champions_list[term].append(sorted_frequency[i][0])



for doc in doc_squared:
    doc_squared[doc] = math.sqrt(doc_squared[doc]);


with open("docs/doc_vector_size.json", "w") as outfile: 
    json.dump(doc_squared,outfile,indent=None)

with open("docs/tf_idf_docs.json", "w") as outfile: 
    json.dump(tf_idf,outfile,indent=None)

with open("docs/champions_list.json", "w") as outfile: 
    json.dump(champions_list,outfile,indent=None)

        