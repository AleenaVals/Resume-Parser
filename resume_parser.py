#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pdfminer')


# In[1]:


def pdf_to_text(text):
        from pdfminer.high_level import extract_text
        text = extract_text(text)
        return text
 


# In[2]:


text =('/home/vals/Downloads/Resume.pdf')
a=pdf_to_text(text)
 


# In[3]:


a


# In[4]:


b=a.replace('\n','')
c=b.replace('\uf0b7','')
d=c.replace('\x0c','')
e=d.replace(',','')



# In[7]:


pip install spacy


# In[8]:


get_ipython().system('python -m spacy download en_core_web_sm')


# In[6]:


import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# In[7]:


tokens = nltk.word_tokenize(e)
tokens


# In[11]:


stops = set(stopwords.words('english'))
print(stops)


# In[12]:


stopslist=list(stops)
stopslist


# In[14]:


for word in tokens: 
    if word not in stopslist:
        print(word)


# In[17]:


import re

def extract_email(e):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", e)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


# In[18]:


extract_email(e)


# In[21]:


nlp = spacy.load("en_core_web_sm")  # load the English model
doc = nlp(e)  # process a text and create a Doc object
n=doc.noun_chunks
for chunk in doc.noun_chunks:       # iterate over the noun chunks in the Doc
   print(chunk.text)


# In[22]:


def extract_skills(nlp_text,n):
    tokens=word_tokenize(nlp_text)
    skills_list_new=['English','Leadership','Collaboration','Content creator']
    skillset=[]
    
    #check for one gram
    for token in tokens:
        if token in skills_list_new:
            skillset.append(token)
    print("")
    
     # check for bi-grams and tri-grams
    for token in tokens:
        token = token.strip()
        if token in skills_list_new:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]
    


# In[23]:


extract_skills(e,n)

