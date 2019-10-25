# -*- coding: utf-8 -*-  
import re
from lxml import etree

data_file_path_nkx = "/home/maxding/TextMatchExperiment/data/内科学.html"
data_file_path_zdx = "/home/maxding/TextMatchExperiment/data/诊断学.html"

def parse_nkx():
    with open(data_file_path_nkx,'r+',encoding='utf-8') as f:
        text = f.read()
        article_pattern = r'<h1.*id="CHP[2-9]">第.篇.*</h1>'
        chapter_pattern = r'<h2.*id="CHP.*">.*</h2>'
        section_pattern = r'<h4.*id="CHP.*">.*</h4>'
        paragraph_pattern = r'<h7.*id="CHP.*">.*</h7>'
        #chapters = re.split(chapter_pattern,text)
        article_titles = re.findall(article_pattern,text)
        articles = re.split(article_pattern,text)
        articles = articles[1:]
        for i in range(len(article_titles)):
            article_title = article_titles[i]
            article = articles[i]
            #print(article_title)
            chapter_titles = re.findall(chapter_pattern,article)
            chapters = re.split(chapter_pattern,article)
            chapters = chapters[1:]
            article_element = etree.HTML(article_title,parser=etree.HTMLParser(encoding='utf-8'))
            article_h = article_element.xpath('//h1')
            article_title_str =  etree.tostring(article_h[0], encoding = "utf-8", pretty_print = True,method='text').decode('utf-8')
            print(article_title_str)
            for j in range(len(chapter_titles)):
                chapter_title = chapter_titles[j]
                chapter = chapters[j]
                #print(chapter_title)
                chapter_element = etree.HTML(chapter_title)
                chapter_h = chapter_element.xpath('//h2')
                chapter_title_str =  etree.tostring(chapter_h[0], encoding = "utf-8", pretty_print = True,method='text').decode('utf-8')
                print(chapter_title_str)
                section_titles = re.findall(section_pattern,chapter)
                section_titles.insert(0,"<h4>Section_Default</h4>")
                sections = re.split(section_pattern,chapter)
                for k in range(len(section_titles)):               
                    section_title = section_titles[k]
                    section_element = etree.HTML(section_title)
                    section_h = section_element.xpath('//h4')
                    section_title_str = etree.tostring(section_h[0], encoding = "utf-8", pretty_print = True,method='text').decode('utf-8')
                    print(section_title_str)
                    section = sections[k]
                    if section == '' or section == " " or section == "\n":
                        continue
                    
                    paragraph_titles = re.findall(paragraph_pattern,section)
                    paragraphs = re.split(paragraph_pattern,section)
                    paragraph_titles.insert(0,"<h7>Paragraph_Default</h7>")
                    for t in range(len(paragraph_titles)):
                        paragraph_title = paragraph_titles[t]
                        paragraph = paragraphs[t]
                        if paragraph == '' or paragraph == " " or paragraph == "\n":
                            continue
                        paragraph_element = etree.HTML(paragraph_title)
                        paragraph_h = paragraph_element.xpath('//h7')
                        paragraph_title_str = etree.tostring(paragraph_h[0], encoding = "utf-8", pretty_print = True,method='text').decode('utf-8')
                        print(paragraph_title_str)
                        paragraph_context = "<div>"+paragraph+"</div>"
                        paragraph_context_element = etree.HTML(paragraph_context)
                        paragraph_context_h = paragraph_context_element.xpath('//div')
                        paragraph_context_str = etree.tostring(paragraph_context_h[0], encoding = "utf-8", pretty_print = True,method='text').decode('utf-8')       
                        paragraph_context_str = paragraph_context_str.strip('\n')
                        paragraph_context_str = paragraph_title_str+'\n'+paragraph_context_str
                        ff = open('/home/maxding/TextMatchExperiment/data/splitText/nkx/'+article_title_str+'|'+chapter_title_str+'|'+section_title_str+'|'+paragraph_title_str,'w+')
                        ff.write(paragraph_context_str)

def parse_zdx():
    with open(data_file_path_zdx,'r+',encoding='utf-8') as f:
        text = f.read()
        article_title_str = '常见症状'
        chapter_title_str = 'NULL'
        section_pattern = r'<h4.*id="CHP.*">.*</h4>'
        paragraph_pattern = r'<h7.*id="CHP.*">.*</h7>'
        section_titles = re.findall(section_pattern,text)
        sections = re.split(section_pattern,text)
        sections = sections[1:]
        for  k in range(len(section_titles)):
            section_title = section_titles[k]
            section = sections[k]
            section_element = etree.HTML(section_title)
            section_h = section_element.xpath('//h4')
            section_title_str = etree.tostring(section_h[0], encoding = "utf-8", pretty_print = True,method='text').decode('utf-8')
            print(section_title_str)
            if section == '' or section == " " or section == "\n":
                continue
            paragraph_titles = re.findall(paragraph_pattern,section)
            paragraphs = re.split(paragraph_pattern,section)
            paragraph_titles.insert(0,"<h7>Paragraph_Default</h7>")
            for t in range(len(paragraph_titles)):
                paragraph_title = paragraph_titles[t]
                paragraph = paragraphs[t]
                if paragraph == '' or paragraph == " " or paragraph == "\n":
                    continue
                paragraph_element = etree.HTML(paragraph_title)
                paragraph_h = paragraph_element.xpath('//h7')
                paragraph_title_str = etree.tostring(paragraph_h[0], encoding = "utf-8", pretty_print = True,method='text').decode('utf-8')
                print(paragraph_title_str)
                paragraph_context = "<div>"+paragraph+"</div>"
                paragraph_context_element = etree.HTML(paragraph_context)
                paragraph_context_h = paragraph_context_element.xpath('//div')
                paragraph_context_str = etree.tostring(paragraph_context_h[0], encoding = "utf-8", pretty_print = True,method='text').decode('utf-8')       
                paragraph_context_str = paragraph_context_str.strip('\n')
                paragraph_context_str = paragraph_title_str+'\n'+paragraph_context_str
                ff = open('/home/maxding/TextMatchExperiment/data/splitText/zdx/'+article_title_str+'|'+chapter_title_str+'|'+section_title_str+'|'+paragraph_title_str,'w+')
                ff.write(paragraph_context_str)


parse_nkx()  
