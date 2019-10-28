import random
import glob


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

#syncRandomSymptoms()


def getMedicalHistoryMaininfo(k=10):
    data_source_path = '/home/maxding/TextMatchExperiment/data/sourceData/100份病历结构化结果与源文件'
    data_dest_path = '/home/maxding/TextMatchExperiment/data/sourceData/medicalhistory_maininfo'
    index = 1
    for filename in glob.glob(data_source_path+'/*txt'):
        print(filename)
        if index > k:
            break
       
        f = open(filename,'r')
        lines = f.readlines()
        maininfo_line = lines[1]
        maininfo_line = maininfo_line.strip('\n')
        main_info_list = maininfo_line.split('\t')
        print(main_info_list)
        main_info_list = [main_info.split('(')[0] for main_info in main_info_list]
        print(main_info_list)
        f = open(data_dest_path+'/'+str(index),'w+')
        for main_info in main_info_list:
            f.write(main_info)
            f.write('\n')
        index += 1

def getMedicalHistoryDiseaseHistory(k=10):
    data_source_path = '/home/maxding/TextMatchExperiment/data/sourceData/100份病历结构化结果与源文件'
    data_dest_path = '/home/maxding/TextMatchExperiment/data/sourceData/medicalhistory_diseasehistory'
    index = 1
    for filename in glob.glob(data_source_path+'/*txt'):
        print(filename)
        if index > k:
            break
       
        f = open(filename,'r')
        lines = f.readlines()
        maininfo_line = lines[1]
        disease_history_line = lines[3]
        maininfo_line = maininfo_line.strip('\n')
        main_info_list = maininfo_line.split('\t')
        disease_history_line = disease_history_line.strip('\n')
        disease_history_list = disease_history_line.split('\t')
        print(main_info_list,disease_history_list)
        main_info_list = [main_info.split('(')[0] for main_info in main_info_list]
        disease_history_ret_list = []
        for disease_history in disease_history_list:
            disease_history_entity = disease_history.split('(')[0]
            disease_history_value = int(disease_history.split('(')[1][0])
            if disease_history_value == 1:
                disease_history_ret_list.append(disease_history_entity)
            print(disease_history_entity,disease_history_value)
        print(main_info_list,disease_history_ret_list)
        f = open(data_dest_path+'/'+str(index),'w+')
        for main_info in main_info_list:
            f.write(main_info)
            f.write('\n')
        for disease_history in disease_history_ret_list:
            f.write(disease_history)
            f.write('\n')
        index += 1

getMedicalHistoryDiseaseHistory()
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