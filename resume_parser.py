#!/usr/bin/env python3
"""
Resume Parser
------------
A simple Python script to extract information from PDF resumes.
Extracts text, email, and skills from PDF resume files.

Required packages:
- pdfminer.six
- spacy
- nltk
"""

import re
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pdfminer.high_level import extract_text

def setup_nlp():
    """
    Initialize NLP requirements.
    Downloads required NLTK data and loads spaCy model.
    """
    try:
        nltk.download('punkt')
        nltk.download('stopwords')
        return spacy.load("en_core_web_sm")
    except Exception as e:
        print(f"Error setting up NLP components: {str(e)}")
        return None

def pdf_to_text(pdf_path):
    """
    Convert PDF file to text.
    Args:
        pdf_path (str): Path to the PDF file    
    Returns:
        str: Extracted text from PDF
    """
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return None

def clean_text(text):
    """
    Clean and preprocess the extracted text.
    Args:
        text (str): Raw text extracted from PDF  
    Returns:
        str: Cleaned text
    """
    if text:
        text = text.replace('\n', '')
        text = text.replace('\uf0b7', '')
        text = text.replace('\x0c', '')
        text = text.replace(',', '')
        return text
    return None

def extract_email(text):
    """
    Extract email address from text.
    Args:
        text (str): Input text
    Returns:
        str: First email address found in text, or None if not found
    """
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None
    return None

def extract_skills(text, noun_chunks):
    """
    Extract skills from text based on predefined skills list.
    Args:
        text (str): Input text
        noun_chunks: spaCy noun chunks (unused in current implementation)
    Returns:
        list: List of identified skills
    """
    tokens = word_tokenize(text)
    skills_list = ['English', 'Leadership', 'Collaboration', 'Content creator']
    skillset = []
    
    # Check for one-gram skills
    for token in tokens:
        if token in skills_list:
            skillset.append(token)
    
    # Remove duplicates and standardize capitalization
    return list(set(skill.capitalize() for skill in skillset))

def analyze_resume(pdf_path):
    """
    Main function to analyze the resume.
    Args:
        pdf_path (str): Path to the PDF resume file  
   Returns:
        dict: Dictionary containing extracted information
    """
    # Initialize NLP components
    nlp = setup_nlp()
    if not nlp:
        return None
    
    # Extract and clean text
    raw_text = pdf_to_text(pdf_path)
    if not raw_text:
        return None
    
    cleaned_text = clean_text(raw_text)
    
    # Process text with spaCy
    doc = nlp(cleaned_text)
    noun_chunks = list(doc.noun_chunks)
    
    # Extract information
    email = extract_email(cleaned_text)
    skills = extract_skills(cleaned_text, noun_chunks)
    
    return {
        'email': email,
        'skills': skills,
        'noun_phrases': [chunk.text for chunk in noun_chunks]
    }

def main():
    """
    Main execution function.
    """
    pdf_path = '/path/to/your/resume.pdf'  # Replace with actual path
    
    results = analyze_resume(pdf_path)
    if results:
        print("\nExtracted Information:")
        print("=====================")
        print(f"Email: {results['email']}")
        print("\nSkills Found:")
        for skill in results['skills']:
            print(f"- {skill}")
        print("\nKey Phrases:")
        for phrase in results['noun_phrases'][:10]:  # Print first 10 phrases
            print(f"- {phrase}")

if __name__ == "__main__":
    main()
