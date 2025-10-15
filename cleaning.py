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