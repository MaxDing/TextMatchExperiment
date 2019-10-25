from elasticsearch import Elasticsearch
es = Elasticsearch([{'host':'192.168.3.156','port':9200}], timeout=3600)


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

retriveTopKDocumentsFromEs(10,symptoms=['发热','咳嗽','头痛','癌症'])
# body = {
#     "query": {
#         "bool":{
#           "should":[
#             {
#               "match_phrase": {
#                 "context": "发热"
#               }
#             },
#             {
#               "match_phrase": {
#                 "context": "咳嗽"
#               }
#             },
#             {
#               "match_phrase": {
#                 "context": "头痛"
#               }
#             },
#             {
#               "match_phrase": {
#                 "context": "癌症"
#               }
#             }
            
#           ],
#           "minimum_should_match": "50%"
#         }
    
#     },
#     "highlight": {
#       "fields": {
#         "context": {}
#       }
#     }
# }
# print(body)
# data = es.search(index="textmatch_paragraph", body=body)
# print(data)