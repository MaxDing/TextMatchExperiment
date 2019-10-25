import random


def getRandomSymptpms(data_source_flag=1, n=10, k=5):
    if data_source_flag == 1:
        data_source_path = '/home/maxding/TextMatchExperiment/data/sourceData/kbSymptoms'
        f = open(data_source_path)
        symptoms = f.read()
        symptoms = symptoms.strip('\n')        
        symptoms = symptoms.split('\n')
        #print(symptoms)
        random_symptoms_set = []
        for i in range(k):
            numbers = [ _ for _ in range(len(symptoms))]
            random_numbers_n = random.sample(numbers,n)
            random_symptoms_n = [ symptoms[random_number] for random_number in random_numbers_n]
            random_symptoms_set.append(random_symptoms_n)
        return random_symptoms_set
    elif data_source_flag == 2:
        return []
    elif data_source_flag == 3:
        return []
    else:
        return []

def syncRandomSymptoms():
    for i in range(2,11,2):
        folder_path = '/home/maxding/TextMatchExperiment/data/sourceData/random_kb_symptoms/n='+str(i)
        random_symptoms_set = getRandomSymptpms(n=i)
        for random_symptoms in random_symptoms_set:
            ff = open(folder_path+'/'+str(random_symptoms_set.index(random_symptoms)+1),'w+')
            for random_symptom in random_symptoms:
                ff.write(random_symptom)
                ff.write('\n')

syncRandomSymptoms()


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