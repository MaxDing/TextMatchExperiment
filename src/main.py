from elasticsearch import Elasticsearch
import glob
es = Elasticsearch([{'host':'192.168.3.156','port':9200}], timeout=3600)




random_kb_symptoms_folder_path = "/home/maxding/TextMatchExperiment/data/sourceData/random_kb_symptoms"
def readRandomKBSymptoms(folder_path):
    random_symptom_set_dict = {}
    for n in range(2,11,2):
        random_symptom_set_dict[n] = {}
        for filename in glob.glob(folder_path+'/n='+str(n)+'/*'):
            f = open(filename,'r')
            index = int(filename.split('/')[-1])
            symptoms = f.read()
            random_symptom_set_dict[n][index] = symptoms.split('\n')
    return random_symptom_set_dict


def retriveTopKDocumentsFromEs(k,symptoms):
    ###read the random symptoms
    
    should_query_list = []
    for symptom in symptoms:
        match_phrase_dict = {
            "match_phrase":{
                "context":symptom
            }
        }
        should_query_list.append(match_phrase_dict)
    query_sql = {
        "query": {
            "bool":{
            "should":should_query_list,
            "minimum_should_match": "50%"
            }
        }
    }
    print(query_sql)
    query_sql['query']['bool']['should'] = should_query_list
    data = es.search(index="textmatch_paragraph", body=query_sql)
    #print(data)
    context_data = data['hits']['hits']
    top_k_context_dict_data = context_data[:k]
    top_k_context = [t['_source']['context'] for t in top_k_context_dict_data]
    for context in top_k_context:
        print('------------------------')
        print(context)

#retriveTopKDocumentsFromEs(10,symptoms=['发热','咳嗽','头痛','癌症'])
x = readRandomKBSymptoms(random_kb_symptoms_folder_path)
print(x)