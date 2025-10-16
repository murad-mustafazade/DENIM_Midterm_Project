import pandas as pd
import re

SUBFIELD_KEYWORDS = {
    'Labor Economics': ['labor', 'labour', 'employment', 'unemployment', 'wage', 'worker', 'job', 'human capital', 'education', 'skill'],
    'Macroeconomics & Monetary': ['macroeconomic', 'monetary', 'inflation', 'recession', 'business cycle', 'central bank', 'interest rate', 'fiscal policy', 'gdp'],
    'Finance': ['finance', 'financial', 'asset pricing', 'portfolio', 'stock', 'bond', 'banking', 'credit', 'investment', 'capital markets'],
    'International Economics': ['international trade', 'trade', 'export', 'import', 'tariff', 'globalization', 'exchange rate', 'currency'],
    'Development & Growth': ['development', 'developing country', 'poverty', 'inequality', 'growth', 'productivity', 'innovation', 'r&d'],
    'Public Economics': ['public', 'tax', 'taxation', 'government spending', 'fiscal', 'subsidy', 'welfare', 'social security'],
    'Health Economics': ['health', 'healthcare', 'hospital', 'medical', 'insurance', 'mortality', 'disease', 'pandemic'],
    'Industrial Organization': ['industrial organization', 'competition', 'monopoly', 'antitrust', 'market power', 'firm', 'regulation', 'merger'],
    'Microeconomics': ['microeconomic', 'consumer', 'household', 'demand', 'supply', 'utility', 'game theory', 'behavioral economics'],
    'Environmental Economics': ['environment', 'environmental', 'climate', 'pollution', 'energy', 'renewable', 'sustainability', 'carbon'],
    'Urban Economics': ['urban', 'city', 'housing', 'real estate', 'transportation', 'infrastructure', 'agglomeration'],
    'Econometrics': ['econometric', 'regression', 'estimation', 'causal', 'instrumental variable', 'panel data', 'time series'],
}

def get_countries(institution_text):
    """Extract countries from institution text"""
    if not institution_text or pd.isna(institution_text):
        return []
    
    countries = []
    text = str(institution_text)
    
    # Check for China
    china_keywords = ['China', 'P.R. China', 'Beijing', 'Shanghai', 'Guangzhou', 
                      'Shenzhen', 'Hong Kong', 'Tsinghua', 'Peking University']
    for keyword in china_keywords:
        if keyword.lower() in text.lower():
            countries.append('China')
            break
    
    # Check for USA
    usa_keywords = ['USA', 'U.S.A', 'United States', 'U.S.']
    for keyword in usa_keywords:
        if keyword in text:
            countries.append('USA')
            break
    
    # Check for other countries
    other_countries = {
        'United Kingdom': ['United Kingdom', 'U.K.', 'UK', 'England'],
        'Germany': ['Germany'],
        'France': ['France'],
        'Canada': ['Canada'],
        'Japan': ['Japan'],
        'Australia': ['Australia'],
        'South Korea': ['South Korea', 'Korea'],
        'India': ['India'],
    }
    
    for country, keywords in other_countries.items():
        for keyword in keywords:
            if keyword in text:
                countries.append(country)
                break
    
    return countries

def get_subfield(title, abstract):
    """Classify article into subfield"""
    text = f"{title} {abstract}".lower()
    
    if not text.strip():
        return 'Unclassified'
    
    # Count keyword matches for each subfield
    scores = {}
    for subfield, keywords in SUBFIELD_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            score += len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
        scores[subfield] = score
    
    # Return subfield with highest score
    max_score = max(scores.values())
    if max_score > 0:
        return max(scores, key=scores.get)
    
    return 'Unclassified'

def clean_abstract(text):
    """Clean abstract text"""
    if pd.isna(text) or not text:
        return ''
    
    text = str(text)
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def main():
    # Read raw data
    input_file = 'raw_data.csv'
    
    print(f"Loading {input_file}...")
    df = pd.read_csv(input_file)
    
    # Clean abstracts
    print("Cleaning abstracts...")
    df['abstract'] = df['abstract'].apply(clean_abstract)
    
    # Extract countries
    print("Extracting countries...")
    df['countries_list'] = df['institutions'].apply(get_countries)
    df['countries'] = df['countries_list'].apply(lambda x: '; '.join(x))
    df['has_china_author'] = df['countries_list'].apply(lambda x: 'China' in x)
    
    # Classify subfields
    print("Classifying subfields...")
    df['subfield'] = df.swifter.apply(lambda row: get_subfield(row['title'], row['abstract']), axis=1)
    
    # Drop temporary column
    df = df.drop('countries_list', axis=1)
    
    # Save cleaned data
    output_file = 'cleaned_data.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig', quoting=1)
    
    print(f"\nSaved cleaned data to {output_file}")
    print(f"Total articles: {len(df)}")
    print(f"Articles with China: {df['has_china_author'].sum()}")

if __name__ == "__main__":
    main()
