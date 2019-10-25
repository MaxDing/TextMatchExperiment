
import glob
from elasticsearch import Elasticsearch
data_folder_path_nkx = '/home/maxding/TextMatchExperiment/data/splitText/nkx'
data_folder_path_zdx = '/home/maxding/TextMatchExperiment/data/splitText/zdx'
def readText():
    es = Elasticsearch([{'host':'192.168.3.156','port':9200}], timeout=3600)
    # for filename in glob.glob(data_folder_path_nkx+'/*'):
    #     names = filename.split('/')
    #     names = names[-1]
    #     titles = names.split('|')
    #     article_title = titles[0]
    #     chapter_title = titles[1]
    #     section_title = titles[2]
    #     paragraph_title = titles[3]
    #     print(article_title,chapter_title,section_title,paragraph_title)
    #     f = open(filename,'r')
    #     context = f.read()
    #     context = context.strip(' ')
    #     context = context.strip('\t')
    #     context = context.strip('\n')
    #     json_data = {
    #         'sourcebook':'内科学',
    #         'article_title':article_title,
    #         'chapter_title':chapter_title,
    #         'section_title':section_title,
    #         'paragraph_title':paragraph_title,
    #         'context':context
    #     }
    #     res = es.index(index="textmatch_paragraph", doc_type="docs", body=json_data)
    #     print(res)

    for filename in glob.glob(data_folder_path_zdx+'/*'):
        names = filename.split('/')
        names = names[-1]
        titles = names.split('|')
        article_title = titles[0]
        chapter_title = titles[1]
        section_title = titles[2]
        paragraph_title = titles[3]
        print(article_title,chapter_title,section_title)
        f = open(filename,'r')
        context = f.read()
        context = context.strip(' ')
        context = context.strip('\t')
        context = context.strip('\n')
        
        json_data = {
            'sourcebook':'诊断学',
            'article_title':article_title,
            'chapter_title':chapter_title,
            'section_title':section_title,
            'paragraph_title':paragraph_title,
            'context':context
        }
        res = es.index(index="textmatch_paragraph", doc_type="docs", body=json_data)
        print(res)


readText()
