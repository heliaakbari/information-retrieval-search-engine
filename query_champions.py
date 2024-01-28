import re
import json 
import math
from parsivar import FindStems
from general_normalization import General_normalization
normalizer = General_normalization();
stemmer = FindStems()

query_sentence = input().strip()
query_sentence = normalizer.normalize(query_sentence)
q_terms = re.split(r'\s+', query_sentence)
q_dic ={}
N_q = 0

with open('docs/tf_idf_docs.json') as json_file:
    tf_idf= json.load(json_file)
with open('docs/doc_vector_size.json') as json_file:
    doc_size= json.load(json_file)
with open('docs/champions_list.json') as json_file:
    champions_list= json.load(json_file)
N_docs = len(doc_size)
not_in_tf_idf = []
for term in q_terms:
        term = stemmer.convert_to_stem(term).split('&')[0]
        if term not in champions_list:
            not_in_tf_idf.append(term)
        else:      
            N_q +=1
            if term not in q_dic :
                q_dic[term] = 1
            else :
                q_dic[term] += 1


length = 0

for term in q_dic:
        if term not in not_in_tf_idf:
            q_dic[term]= ( 1 + math.log2(q_dic[term])) * math.log2(N_docs/tf_idf[term][0])  
            length += math.pow(q_dic[term],2)
        

length = math.sqrt(length)    
for term in q_dic:
   if term not in not_in_tf_idf:
        q_dic[term] /= length 

print(q_dic)

doc_scores ={}
for term in q_dic:
    if term not in not_in_tf_idf:
        for doc in champions_list[term]:
            if doc in doc_scores:
                doc_scores[doc] += q_dic[term] * tf_idf[term][1][doc] / doc_size[doc]
            else:
                doc_scores[doc] = q_dic[term] * tf_idf[term][1][doc] / doc_size[doc]

sorted_docs = sorted(doc_scores.items(), key=lambda x:x[1],reverse=True)

with open('docs/IR_data_news.json') as json_file:
    documents =json.load(json_file)

result_dic = []
for i in range (min(10,len(sorted_docs))):
    result_dic.append((sorted_docs[i],documents[sorted_docs[i][0]]))

with open("results_champion/"+query_sentence+".json", "w") as outfile: 
    json.dump(result_dic,outfile,indent=None)