from elasticsearch import Elasticsearch
from LogicServer.DiagnoseCore.KBConverter.LogicDataPreProcess import LogicDataPreProcess
from LogicServer.DiagnoseCore.KBConverter.Literal import Literal
from LogicServer.DiagnoseCore.diagnose import TriageDiagnose
from LogicServer.DiagnoseCore.Utils.patient import Patient
import glob
import requests,json


class TextMatchExperiment:
    es_url = '192.168.3.156'
    es_port = 9200
    random_kb_symptoms_folder_path = "/home/maxding/TextMatchExperiment/data/sourceData/random_kb_symptoms"
    maininfo_folder_path = '/home/maxding/TextMatchExperiment/data/sourceData/medicalhistory_maininfo'
    maininfo_and_diseasehistory_folder_path = '/home/maxding/TextMatchExperiment/data/sourceData/medicalhistory_diseasehistory'
    maininfo_and_diseasehistory_withnegative_folder_path = '/home/maxding/TextMatchExperiment/data/sourceData/medicalhistory_diseasehistory(with negative)'
    ner_url = 'http://192.168.3.156:32031/ner'
    experiment1_randomkbsymptoms_result_folder = '/home/maxding/TextMatchExperiment/result/experiment1/randomKBSymptoms'
    experiment1_maininfo_result_folder = '/home/maxding/TextMatchExperiment/result/experiment1/MedicalHIstoryMainInfos'
    experiment1_maininfoanddiseasehistory_result_folder = '/home/maxding/TextMatchExperiment/result/experiment1/MedicalHIstoryDiseaseHistory'
    experiment2_result_folder = '/home/maxding/TextMatchExperiment/result/experiment2'
    def __init__(self):
        self.es = Elasticsearch([{'host':TextMatchExperiment.es_url,'port':TextMatchExperiment.es_port}])

    def readRandomKBSymptoms(self):
        folder_path = TextMatchExperiment.random_kb_symptoms_folder_path
        random_symptom_set_dict = {}
        for n in range(2,11,2):
            random_symptom_set_dict[n] = {}
            for filename in glob.glob(folder_path+'/n='+str(n)+'/*'):
                f = open(filename,'r')
                index = int(filename.split('/')[-1])
                symptoms = f.read()
                random_symptom_set_dict[n][index] = symptoms.split('\n')[0:-1]
        return random_symptom_set_dict
    
    def readMainInfo(self):
        folder_path = TextMatchExperiment.maininfo_folder_path
        main_info_set_dict = {1:{}}
        for filename in glob.glob(folder_path+'/*'):
            f = open(filename,'r')
            print(filename)
            index = int(filename.split('/')[-1])
            symptoms = f.read()
            symptoms = symptoms.strip('\n')
            symptom_list =  symptoms.split('\n')
            symptom_list = list(set(symptom_list))
            main_info_set_dict[1][index] = symptom_list
        return main_info_set_dict
    def readMainInfoAndDiseaseHistory(self):
        folder_path = TextMatchExperiment.maininfo_and_diseasehistory_folder_path
        main_info_set_dict = {1:{}}
        for filename in glob.glob(folder_path+'/*'):
            f = open(filename,'r')
            print(filename)
            index = int(filename.split('/')[-1])
            symptoms = f.read()
            symptoms = symptoms.strip('\n')
            symptom_list =  symptoms.split('\n')
            symptom_list = list(set(symptom_list))
            main_info_set_dict[1][index] = symptom_list
        return main_info_set_dict

    def readMainInfoAndDiseaseHistoryWithNegative(self):
        folder_path = TextMatchExperiment.maininfo_and_diseasehistory_withnegative_folder_path
        symptom_set_dict = {}
        for filename in glob.glob(folder_path+'/*'):
            f = open(filename,'r')
            print(filename)
            index = int(filename.split('/')[-1])
            lines = f.readlines()
            main_info_line = lines[0]
            symptom_postive_line = lines[1]
            symptom_negative_line = lines[2]
            main_info_line = main_info_line.strip('\n')
            main_info_line = main_info_line.strip('\t')
            symptom_postive_line = symptom_postive_line.strip('\n')
            symptom_postive_line = symptom_postive_line.strip('\t')
            symptom_negative_line = symptom_negative_line.strip('\n')
            symptom_negative_line = symptom_negative_line.strip('\t')
            main_info_list = list(set(main_info_line.split('\t')))
            symptom_postive_list = list(set(symptom_postive_line.split('\t')))
            symptom_negative_list = list(set(symptom_negative_line.split('\t')))
            symptom_set_dict[index] = {'main_info_list':main_info_list,'symptom_postive_list':symptom_postive_list,'symptom_negative_list':symptom_negative_list}
        return symptom_set_dict

    def retriveTopKParagraphsFromEs(self,symptoms,k=10):
        ###read the random symptoms
        print(symptoms)
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
                "minimum_should_match": 2
                }
            }
        }
        #print(query_sql)
        query_sql['query']['bool']['should'] = should_query_list
        data = self.es.search(index="textmatch_paragraph", body=query_sql)
        #print(data)
        context_data = data['hits']['hits']
        top_k_context_dict_data = context_data[:k]
        top_k_context = [t['_source']['context'] for t in top_k_context_dict_data]
        return top_k_context



    def splitContextandGetCategory(self,context):
        data = json.dumps({"text":context})
        r = requests.post(TextMatchExperiment.ner_url,data=data)
        ret_data = {'disease':set(),'symptom':set()}
        #print(r.json)
        ret =  r.json()
        for ret_conext in ret['contents']:
            if isinstance(ret_conext,dict):
                category = ret_conext['category']
                entity = ""
                for item in ret_conext['subItems']:
                    entity += item
                if category == '疾病':
                    ret_data['disease'].add(entity)
                elif category == '症状':
                    ret_data['symptom'].add(entity)
                else:
                    pass
        #print(ret_data)
        return ret_data

    def getDiseaseandSymptomsByKBConventer(self,symptom_list):
        print('in the getDiseaseandSymptomsByKBConventer')
        print(symptom_list)
        ret_data = {'disease':set(),'symptom':set()}
        logicDataPreProcessInstance = LogicDataPreProcess(symptom_list,hop=4)   ###创建数据预处理实例
        logic_rules = logicDataPreProcessInstance.get_rules()
        print('rule_num:%d'%(len(logic_rules)))
        for logic_rule in logic_rules:
            left_literal_list = logic_rule[0]
            right_literal_list = logic_rule[1]
            for literal in left_literal_list:                
                name = literal.get_name()
                entity_name = logicDataPreProcessInstance.variable_2_entity(name)
                flag = literal.get_flag()
                entity_type = literal.get_entity_type()
                #print('%s %d'%(self.__logicDataPreProcessInstance.get_variable_map()[name],entity_type))
                if entity_type == Literal.TYPE_DISEASE:  ###疾病
                    
                    ret_data['disease'].add(entity_name)
                elif entity_type == Literal.TYPE_SYMPTOM: ###症状
                    
                    ret_data['symptom'].add(entity_name)
                else:
                    pass
            for literal in right_literal_list:                
                name = literal.get_name()
                entity_name = logicDataPreProcessInstance.variable_2_entity(name)
                flag = literal.get_flag()
                entity_type = literal.get_entity_type()
                #print('%s %d'%(self.__logicDataPreProcessInstance.get_variable_map()[name],entity_type))
                if entity_type == Literal.TYPE_DISEASE:  ###疾病
                    
                    ret_data['disease'].add(entity_name)
                elif entity_type == Literal.TYPE_SYMPTOM: ###症状
                    
                    ret_data['symptom'].add(entity_name)
                else:
                    pass
       
        return ret_data

    def experiment1RandomKBSymptomsTextMatch(self,random_symptom_set_dict):
        return_data = {}
        for n in random_symptom_set_dict:
            return_data[n] = {}
            for index in random_symptom_set_dict[n]:
                return_data[n][index] = {}
        for n in random_symptom_set_dict:
            random_symptom_set = random_symptom_set_dict[n]
            for index in random_symptom_set:
                random_symptom_list = random_symptom_set[index]
                #print('--------------------')
                #print(n,index,random_symptom_list)
                top_k_context = self.retriveTopKParagraphsFromEs(random_symptom_list)
                print(n,index,random_symptom_list)
                ret = {'disease':set(),'symptom':set()}
                if len(top_k_context) == 0:
                    print('-----------No Context------------')
                    return_data[n][index] = ret
                else:                               
                    for conext in top_k_context:
                        data = self.splitContextandGetCategory(conext)
                        ret['disease'] |= data['disease']
                        ret['symptom'] |= data['symptom']    
                        print('---in the loop-------')
                        print(ret) 
                        return_data[n][index] = ret          
                
                #print(ret)
        return return_data
        
    def experiment1RandomKBSymptomsKBConventer(self,random_symptom_set_dict):
        return_data = {}
        for n in random_symptom_set_dict:
            return_data[n] = {}
            for index in random_symptom_set_dict[n]:
                return_data[n][index] = {}
        for n in random_symptom_set_dict:
            random_symptom_set = random_symptom_set_dict[n]
            for index in random_symptom_set:
                random_symptom_list = random_symptom_set[index]   
                print(n,index,random_symptom_list)             
                ret_data = self.getDiseaseandSymptomsByKBConventer(random_symptom_list)
                return_data[n][index] = ret_data
        return return_data
    def experiment1(self,flag):
        random_symptom_set_dict = {}
        dest_data_folder = ""
        if flag == 1:
            random_symptom_set_dict = self.readRandomKBSymptoms()
            dest_data_folder = TextMatchExperiment.experiment1_randomkbsymptoms_result_folder
        elif flag == 2:
            random_symptom_set_dict = self.readMainInfo()
            dest_data_folder = TextMatchExperiment.experiment1_maininfo_result_folder
        elif flag == 3:
            random_symptom_set_dict = self.readMainInfoAndDiseaseHistory()
            dest_data_folder = TextMatchExperiment.experiment1_maininfoanddiseasehistory_result_folder
        else:
            pass
        return_data1 = self.experiment1RandomKBSymptomsTextMatch(random_symptom_set_dict)
        return_data2 = self.experiment1RandomKBSymptomsKBConventer(random_symptom_set_dict)
        print(return_data1)
        for n in return_data1:
            for index in return_data1[n]:
                symptom_list = random_symptom_set_dict[n][index]
                
                disease_set1,symptom_set1,disease_set2,symptom_set2 = return_data1[n][index]['disease'],return_data1[n][index]['symptom'],return_data2[n][index]['disease'],return_data2[n][index]['symptom']
                
                D = disease_set1 | symptom_set1
                G = disease_set2 | symptom_set2

                J = len(D&G)/len(D|G) if len(D|G) != 0 else -1
                Fg = len(G&D)/len(G) if len(G) != 0 else -1
                Fd = len(G&D)/len(D) if len(D) != 0 else -1
                
                f = open(dest_data_folder+'/n='+str(n)+',index='+str(index),'w+')
                f.write(str(symptom_list)+'\n')
                f.write('--------------------------------\n')
                f.write('TextMatch  :\tdisease_len:%d,\tsymptom_len:%d\n'%(len(disease_set1),len(symptom_set1)))
                f.write('KBConventer:\tdisease_len:%d,\tsymptom_len:%d\n'%(len(disease_set2),len(symptom_set2)))
                f.write('--------------------------------\n')
                f.write('G:%d\tD:%d\n'%(len(G),len(D)))
                f.write('J:%f\n'%(J))
                f.write('Fg:%f\tFd:%f\n'%(Fg,Fd))
    

    def experiment2TextMatch(self,symptom_list):
        #print('--------------------')
        #print(n,index,random_symptom_list)
        top_k_context = self.retriveTopKParagraphsFromEs(symptom_list)
        ret = set()
        if len(top_k_context) == 0:
            print('-----------No Context------------')
        else:                               
            for conext in top_k_context:
                data = self.splitContextandGetCategory(conext)
                ret |= data['disease']     
        return ret       

    def experiment2KBConventer(self,main_info_list,symptom_postive_list,symptom_negative_list):
        
        try:
            print('------in the experiment2KBConventer----------')
            diagnose = TriageDiagnose(patient=Patient('1',True,20),main_info_list=main_info_list)
            diagnose.start_reasoning()
            print('------after main info----------')
            new_main_info_list = []
            for symptom in symptom_postive_list:
                new_main_info_list.append((symptom,True))
            for symptom in symptom_negative_list:
                new_main_info_list.append((symptom,False))
            diagnose.add_main_info(new_main_info_list)
            print('------after disease history----------')
            disease_list = diagnose.get_candidate_disease_list()
            print(len(disease_list))
            return set(disease_list)
        except Exception as e:
            print(e)
            return set()
    def experiment2(self):
        symptom_set_dict = self.readMainInfoAndDiseaseHistoryWithNegative()
        for index in symptom_set_dict:
            symptom_dict = symptom_set_dict[index]
            main_info_list = symptom_dict['main_info_list']
            symptom_postive_list = symptom_dict['symptom_postive_list']
            symptom_negative_list = symptom_dict['symptom_negative_list']
            textmatch_symptom_list = list(set(main_info_list+symptom_postive_list))
            disease_set1 = self.experiment2TextMatch(textmatch_symptom_list)
            disease_set2 = self.experiment2KBConventer(main_info_list,symptom_postive_list,symptom_negative_list)
            D = disease_set1
            G = disease_set2

            J = len(D&G)/len(D|G) if len(D|G) != 0 else -1
            Fg = len(G&D)/len(G) if len(G) != 0 else -1
            Fd = len(G&D)/len(D) if len(D) != 0 else -1
            f = open(TextMatchExperiment.experiment2_result_folder+'/'+str(index),'w+')
            f.write(str(main_info_list)+'\n')
            f.write(str(symptom_postive_list)+'\n')
            f.write(str(symptom_negative_list)+'\n')
            f.write('--------------------------------\n')
            f.write('G:%d\tD:%d\n'%(len(G),len(D)))
            f.write('J:%f\n'%(J))
            f.write('Fg:%f\tFd:%f\n'%(Fg,Fd))
#retriveTopKDocumentsFromEs(10,symptoms=['发热','咳嗽','头痛','癌症'])
# x = readRandomKBSymptoms(random_kb_symptoms_folder_path)
# print(x)
te = TextMatchExperiment()
#te.experiment1()
te.experiment1(flag=1)
# te.experiment1(flag=2)
# te.experiment1(flag=3)
# te.experiment2()