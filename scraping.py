import requests
import pandas as pd
import re
import time
from datetime import datetime
"""
Download articles from Top 5 Economics Journals: 1990-2025
Removes incomplete rows automatically
"""
def extract_country_from_text(text):
    if not text:
        return ""
    
    country_patterns = {
        'USA': [r'\bUSA\b', r'\bU\.S\.A\b', r'\bUnited States\b', r'\bU\.S\.\b', 
                r', (AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY) \d{5}'],
        'United Kingdom': [r'\bUnited Kingdom\b', r'\bU\.K\.\b', r'\bUK\b', r'\bEngland\b', r'\bScotland\b', r'\bWales\b'],
        'Canada': [r'\bCanada\b'],
        'Germany': [r'\bGermany\b'],
        'France': [r'\bFrance\b'],
        'Italy': [r'\bItaly\b'],
        'Spain': [r'\bSpain\b'],
        'Netherlands': [r'\bNetherlands\b'],
        'Switzerland': [r'\bSwitzerland\b'],
        'China': [r'\bChina\b'],
        'Japan': [r'\bJapan\b'],
        'Australia': [r'\bAustralia\b'],
    }
    
    countries = []
    for country, patterns in country_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                countries.append(country)
                break
    
    return '; '.join(countries)