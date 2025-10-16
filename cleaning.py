import pandas as pd
import re
import swifter

SUBFIELD_KEYWORDS = {
    'Labor Economics': ['labor', 'labour', 'employment', 'unemployment', 'wage', 'worker', 'job', 'human capital',
                        'education', 'skill', 'occupation', 'career', 'workplace', 'hiring', 'firing', 'layoff',
                        'training', 'discrimination', 'gender gap', 'immigration', 'immigrant', 'migration',
                        'union', 'collective bargaining', 'minimum wage', 'labor force', 'workforce'],
   
    'Macroeconomics & Monetary': ['macroeconomic', 'monetary', 'inflation', 'recession', 'business cycle',
                                   'central bank', 'interest rate', 'fiscal policy', 'gdp', 'federal reserve',
                                   'money supply', 'quantitative easing', 'deflation', 'stagflation', 'phillips curve',
                                   'unemployment rate', 'output gap', 'taylor rule', 'monetary transmission',
                                   'aggregate demand', 'aggregate supply', 'economic growth', 'economic expansion'],
   
    'Finance': ['finance', 'financial', 'asset pricing', 'portfolio', 'stock', 'bond', 'banking', 'credit',
                'investment', 'capital markets', 'equity', 'debt', 'derivative', 'option', 'futures', 'swap',
                'risk premium', 'return', 'volatility', 'liquidity', 'leverage', 'dividend', 'ipo', 'merger',
                'acquisition', 'bankruptcy', 'default', 'rating', 'hedge', 'mutual fund', 'pension',
                'insurance', 'reinsurance', 'financial crisis', 'systemic risk', 'contagion', 'bailout',
                'mortgage', 'loan', 'interest', 'yield', 'spread', 'arbitrage', 'market efficiency'],
   
    'International Economics': ['international trade', 'trade', 'export', 'import', 'tariff', 'globalization',
                                'exchange rate', 'currency', 'trade agreement', 'wto', 'nafta', 'fta',
                                'trade deficit', 'trade surplus', 'balance of payments', 'current account',
                                'capital account', 'foreign direct investment', 'fdi', 'multinational',
                                'offshoring', 'outsourcing', 'trade barrier', 'quota', 'dumping',
                                'comparative advantage', 'trade liberalization', 'protectionism'],
   
    'Development & Growth': ['development', 'developing country', 'poverty', 'inequality', 'growth',
                            'productivity', 'innovation', 'r&d', 'technology', 'technological change',
                            'human development', 'economic development', 'emerging market', 'transition',
                            'industrialization', 'structural transformation', 'convergence', 'divergence',
                            'income distribution', 'gini', 'social mobility', 'intergenerational',
                            'institution', 'governance', 'corruption', 'property rights', 'rule of law'],
   
    'Public Economics': ['public', 'tax', 'taxation', 'government spending', 'fiscal', 'subsidy', 'welfare',
                        'social security', 'redistribution', 'public good', 'externality', 'pigovian',
                        'budget', 'deficit', 'surplus', 'debt', 'public debt', 'sovereign debt',
                        'tax evasion', 'tax avoidance', 'tax rate', 'tax base', 'progressive', 'regressive',
                        'transfer', 'benefit', 'pension', 'medicare', 'medicaid', 'unemployment insurance',
                        'disability', 'snap', 'tanf', 'eitc', 'child tax credit', 'universal basic income'],
   
    'Health Economics': ['health', 'healthcare', 'hospital', 'medical', 'insurance', 'mortality', 'disease',
                        'pandemic', 'covid', 'vaccination', 'vaccine', 'pharmaceutical', 'drug', 'medicine',
                        'doctor', 'physician', 'nurse', 'patient', 'treatment', 'diagnosis', 'prevention',
                        'life expectancy', 'infant mortality', 'morbidity', 'disability', 'mental health',
                        'obesity', 'smoking', 'alcohol', 'substance', 'addiction', 'opioid', 'medicare',
                        'medicaid', 'aca', 'obamacare', 'single payer', 'public option', 'hmo', 'ppo'],
   
    'Industrial Organization': ['industrial organization', 'competition', 'monopoly', 'antitrust',
                                'market power', 'firm', 'regulation', 'merger', 'oligopoly', 'duopoly',
                                'market structure', 'concentration', 'herfindahl', 'entry', 'exit',
                                'barrier to entry', 'product differentiation', 'advertising', 'marketing',
                                'price discrimination', 'bundling', 'tying', 'vertical integration',
                                'horizontal integration', 'network effect', 'platform', 'two-sided market',
                                'auction', 'bidding', 'procurement', 'privatization', 'deregulation'],
   
    'Microeconomics': ['microeconomic', 'consumer', 'household', 'demand', 'supply', 'utility',
                       'game theory', 'behavioral economics', 'preference', 'choice', 'decision',
                       'rational', 'irrational', 'bounded rationality', 'heuristic', 'bias',
                       'prospect theory', 'loss aversion', 'risk aversion', 'time preference',
                       'discount', 'present bias', 'hyperbolic', 'altruism', 'fairness',
                       'reciprocity', 'trust', 'cooperation', 'coordination', 'nash equilibrium',
                       'pareto', 'welfare', 'social choice', 'mechanism design', 'matching',
                       'signaling', 'screening', 'moral hazard', 'adverse selection',
                       'principal agent', 'contract', 'incentive', 'information asymmetry'],
   
    'Environmental Economics': ['environment', 'environmental', 'climate', 'pollution', 'energy',
                                'renewable', 'sustainability', 'carbon', 'emission', 'greenhouse',
                                'global warming', 'climate change', 'carbon tax', 'cap and trade',
                                'kyoto', 'paris agreement', 'fossil fuel', 'oil', 'gas', 'coal',
                                'solar', 'wind', 'nuclear', 'hydroelectric', 'biomass', 'biofuel',
                                'deforestation', 'conservation', 'biodiversity', 'ecosystem',
                                'water', 'air quality', 'waste', 'recycling', 'circular economy',
                                'natural resource', 'extraction', 'mining', 'fishing', 'forestry'],
   
    'Urban Economics': ['urban', 'city', 'housing', 'real estate', 'transportation', 'infrastructure',
                        'agglomeration', 'metropolitan', 'suburb', 'sprawl', 'gentrification',
                        'zoning', 'land use', 'rent', 'home price', 'affordability', 'homeless',
                        'commute', 'traffic', 'congestion', 'public transit', 'subway', 'bus',
                        'highway', 'road', 'parking', 'walkability', 'density', 'neighborhood',
                        'segregation', 'redlining', 'nimby', 'yimby', 'property tax', 'mortgage'],
   
    'Econometrics': ['econometric', 'regression', 'estimation', 'causal', 'instrumental variable',
                     'panel data', 'time series', 'identification', 'endogeneity', 'omitted variable',
                     'measurement error', 'difference in differences', 'did', 'regression discontinuity',
                     'rdd', 'propensity score', 'matching', 'synthetic control', 'event study',
                     'fixed effect', 'random effect', 'clustered standard error', 'heteroskedasticity',
                     'autocorrelation', 'cointegration', 'var', 'vector autoregression', 'granger',
                     'forecast', 'prediction', 'machine learning', 'lasso', 'ridge', 'elastic net',
                     'random forest', 'neural network', 'deep learning', 'bootstrap', 'monte carlo'],
   
    'Political Economy': ['political', 'election', 'voting', 'voter', 'democracy', 'autocracy',
                         'dictatorship', 'politician', 'party', 'campaign', 'lobbying', 'interest group',
                         'polarization', 'ideology', 'partisan', 'gerrymandering', 'media', 'propaganda',
                         'revolution', 'conflict', 'war', 'peace', 'military', 'defense', 'security',
                         'nationalism', 'populism', 'brexit', 'referendum', 'constitution', 'federalism'],
   
    'Law and Economics': ['law', 'legal', 'court', 'judge', 'jury', 'litigation', 'lawsuit', 'settlement',
                         'crime', 'criminal', 'police', 'incarceration', 'prison', 'jail', 'bail',
                         'death penalty', 'deterrence', 'recidivism', 'juvenile', 'gun', 'violence',
                         'property right', 'intellectual property', 'patent', 'copyright', 'trademark',
                         'contract law', 'tort', 'liability', 'negligence', 'bankruptcy', 'corporate law'],
   
    'Behavioral Economics': ['behavioral', 'psychology', 'cognitive', 'emotion', 'mood', 'happiness',
                            'wellbeing', 'satisfaction', 'nudge', 'framing', 'anchor', 'availability',
                            'representative', 'confirmation bias', 'overconfidence', 'hindsight bias',
                            'mental accounting', 'sunk cost', 'endowment effect', 'status quo bias',
                            'social preference', 'other regarding', 'inequity aversion', 'reciprocal',
                            'social norm', 'peer effect', 'social influence', 'herd', 'cascade',
                            'self control', 'temptation', 'commitment', 'procrastination', 'addiction'],
   
    'Experimental Economics': ['experiment', 'laboratory', 'field experiment', 'rct', 'randomized',
                              'treatment', 'control group', 'placebo', 'double blind', 'dictator game',
                              'ultimatum game', 'public good game', 'trust game', 'beauty contest',
                              'auction experiment', 'market experiment', 'experimental market',
                              'subject pool', 'incentive compatible', 'deception', 'demand effect'],
   
    'Economic History': ['history', 'historical', 'long run', 'persistence', 'path dependence',
                        'industrial revolution', 'great depression', 'great recession', 'financial crisis',
                        'world war', 'cold war', 'colonialism', 'slavery', 'institution origin',
                        'economic history', 'cliometric', 'archival', 'historical data'],
   
    'Agricultural Economics': ['agriculture', 'agricultural', 'farm', 'farmer', 'crop', 'livestock',
                              'food', 'nutrition', 'hunger', 'famine', 'food security', 'gmo',
                              'organic', 'pesticide', 'fertilizer', 'irrigation', 'drought',
                              'land reform', 'rural', 'peasant', 'cooperative', 'commodity'],
   
    'Education Economics': ['education', 'school', 'student', 'teacher', 'classroom', 'curriculum',
                           'test score', 'achievement', 'attainment', 'dropout', 'graduation',
                           'college', 'university', 'tuition', 'financial aid', 'scholarship',
                           'school choice', 'charter school', 'voucher', 'private school',
                           'human capital', 'skill', 'training', 'stem', 'literacy', 'numeracy']
}

def get_countries(institution_text):
    """Extract countries from institution text - comprehensive version with UK/USA disambiguation"""
    if not institution_text or pd.isna(institution_text):
        return []
    
    countries = []
    text = str(institution_text)
    
    # USA - Check first with most specific patterns
    usa_patterns = [
        # Explicit country mentions
        r'\bUSA\b', r'\bU\.S\.A\.?\b', r'\bUnited States\b', r'\bU\.S\.\b',
        # State abbreviations with zip codes
        r', (AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\s*\d{5}',
        r'\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\s+\d{5}',
        # US-specific Cambridge/Oxford
        r'\bCambridge,?\s+(MA|Mass|Massachusetts)\b',
        r'\bOxford,?\s+(OH|Ohio|MS|Mississippi)\b',
        # Major US cities
        r'\b(New York|Boston|Chicago|Philadelphia|Los Angeles|San Francisco|Washington|Seattle|Atlanta|Dallas|Houston|Miami|Denver|Phoenix|San Diego|Baltimore|Detroit|Minneapolis|Pittsburgh|Cleveland|Milwaukee|Portland|Austin|Nashville|Indianapolis|Charlotte|Columbus|San Antonio|San Jose|Jacksonville|Fort Worth|Sacramento|Las Vegas|Kansas City|Memphis|Richmond|New Orleans|Cincinnati|Madison|Ann Arbor|Berkeley|Palo Alto|Princeton|Ithaca|Durham|Chapel Hill|Evanston|Stanford|Pasadena|Boulder|Providence|Hanover|Charlottesville|Amherst|Williamstown|Claremont|West Point|Annapolis)\b',
        # US institutions
        r'\b(Harvard|Yale|Princeton|Stanford|MIT|Columbia|UCLA|Penn|UPenn|Wharton|Cornell|Brown|Dartmouth|Duke|Chicago|Northwestern|Johns Hopkins|Caltech|Michigan|Virginia|Wisconsin|Illinois|Minnesota|Washington|Texas|North Carolina|Maryland|Purdue|Indiana|Ohio State|Penn State|Rutgers|Georgetown|Vanderbilt|Emory|Carnegie Mellon|Rice|Notre Dame|USC|NYU|Boston University|Boston College|Tufts|Brandeis|Rochester|Case Western|Wake Forest|Georgia Tech|UC San Diego|UC Davis|UC Irvine|UC Santa Barbara|William & Mary|Lehigh|Syracuse|Tulane|George Washington|American University|Fordham|Northeastern|Pepperdine|SMU|TCU|Baylor|Villanova|Drexel|Temple|Arizona State|Florida State|Georgia State|SUNY|CUNY)\b',
        # Federal institutions
        r'\bFederal Reserve\b', r'\bFed\b.*\b(Bank|Board)\b', r'\bNBER\b', r'\bNational Bureau of Economic Research\b',
        r'\bCensus Bureau\b', r'\bBureau of Labor Statistics\b', r'\bBLS\b', r'\bCBO\b', r'\bGAO\b',
        r'\bIMF.*Washington\b', r'\bWorld Bank.*Washington\b',
        r'Brookings', r'RAND Corporation', r'Urban Institute', r'Hoover Institution',
    ]
    
    for pattern in usa_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('USA')
            break
    
    # China - comprehensive
    china_patterns = [
        r'\bChina\b', r'\bP\.?R\.?\s*China\b', r'\bPeople\'?s Republic of China\b',
        r'\b(Beijing|Shanghai|Guangzhou|Shenzhen|Chengdu|Hangzhou|Wuhan|Nanjing|Xi\'?an|Tianjin|Chongqing|Suzhou|Dalian|Qingdao|Changsha|Xiamen|Harbin|Jinan|Fuzhou|Zhengzhou|Kunming|Lanzhou|Hefei|Nanchang|Shijiazhuang|Urumqi|Guiyang|Taiyuan|Hohhot|Nanning|Yinchuan|Xining)\b',
        r'\b(Tsinghua|Peking University|PKU|Renmin|Fudan|Zhejiang University|Shanghai Jiao Tong|SJTU|Nanjing University|USTC|University of Science and Technology of China|Wuhan University|Sun Yat-sen|SYSU|Nankai|Xiamen University|Shandong University|Huazhong|Beihang|Beijing Normal|East China Normal|ECNU|Tongji|Tianjin University|Southeast University|Central University of Finance|CUFE|Shanghai University of Finance|SUFE|CASS|Chinese Academy)\b',
        r'\bHong Kong\b', r'\bHKU\b', r'\bCUHK\b', r'\bHKUST\b', r'\bCity University of Hong Kong\b',
        r"People's Bank of China", r'\bPBOC\b',
    ]
    
    for pattern in china_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('China')
            break
    
    # United Kingdom - only check if USA not already found
    if 'USA' not in countries:
        uk_patterns = [
            r'\bUnited Kingdom\b', r'\bU\.?K\.?\b', r'\bGreat Britain\b', r'\bEngland\b', r'\bScotland\b', r'\bWales\b',
            # UK-specific Cambridge/Oxford
            r'\bCambridge,?\s+(UK|England|United Kingdom)\b',
            r'\bOxford,?\s+(UK|England|United Kingdom)\b',
            # UK cities with university context
            r'\b(London|Manchester|Birmingham|Edinburgh|Glasgow|Liverpool|Bristol|Leeds|Sheffield|Newcastle|Nottingham|Leicester|Southampton|Brighton|York|Warwick|Bath|Durham|St Andrews|Exeter|Cardiff|Aberdeen|Belfast)\b.*\b(University|College|School)\b',
            # UK institutions
            r'\b(LSE|London School of Economics|Imperial College|UCL|University College London|King\'?s College|Queen Mary|Warwick|Edinburgh|Manchester|Bristol|Nottingham|Glasgow|Birmingham|Southampton|Durham|St Andrews|York|Exeter|Lancaster|Bath|Essex|Sussex|Kent|Reading|Sheffield|Leeds|Newcastle|Cardiff|Queen\'?s University Belfast|Strathclyde)\b.*\b(University|College)\b',
            r'\bUniversity of (Oxford|Cambridge)\b',
            r'\bBank of England\b', r'\bOffice for National Statistics\b', r'\bONS\b',
            r'London Business School',
        ]
        
        for pattern in uk_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                countries.append('United Kingdom')
                break
    
    # Germany
    germany_patterns = [
        r'\bGermany\b', r'\bDeutschland\b',
        r'\b(Berlin|Munich|München|Hamburg|Frankfurt|Cologne|Köln|Stuttgart|Düsseldorf|Dortmund|Essen|Leipzig|Bremen|Dresden|Hannover|Nuremberg|Nürnberg|Mannheim|Heidelberg|Bonn|Münster|Karlsruhe|Freiburg|Konstanz|Tübingen|Göttingen|Marburg|Regensburg|Passau)\b',
        r'\b(Ludwig.*Maximilian|LMU|Humboldt|Freie Universität|Free University|TU Munich|Technical University of Munich|Heidelberg University|Mannheim|Frankfurt School|Goethe University|University of Bonn|ZEW|Ifo Institute|DIW|Bundesbank|Max Planck|IZA)\b',
    ]
    
    for pattern in germany_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Germany')
            break
    
    # France
    france_patterns = [
        r'\bFrance\b',
        r'\b(Paris|Lyon|Marseille|Toulouse|Nice|Nantes|Strasbourg|Montpellier|Bordeaux|Lille|Rennes|Grenoble|Aix)\b',
        r'\b(Sorbonne|École|Ecole|Sciences Po|PSE|Paris School of Economics|INSEAD|HEC Paris|Toulouse School of Economics|TSE|EHESS|ENS|Polytechnique|Paris-Dauphine|Panthéon|Pantheon|CREST|CNRS)\b',
        r'\bBanque de France\b', r'INSEE\b',
    ]
    
    for pattern in france_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('France')
            break
    
    # Canada
    canada_patterns = [
        r'\bCanada\b',
        r'\b(Toronto|Montreal|Montréal|Vancouver|Ottawa|Calgary|Edmonton|Winnipeg|Quebec|Québec|Hamilton|Kitchener|Victoria|Halifax|Saskatoon|Kingston|Waterloo)\b',
        r'\b(University of Toronto|UofT|McGill|UBC|University of British Columbia|McMaster|Queen\'?s University|Alberta|Calgary|Western Ontario|Waterloo|Simon Fraser|SFU|York University|Carleton|Dalhousie|Laval|Concordia)\b',
        r'\bBank of Canada\b', r'\bStatistics Canada\b',
    ]
    
    for pattern in canada_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Canada')
            break
    
    # Other major countries
    other_countries = {
        'Japan': [r'\bJapan\b', r'\b(Tokyo|Osaka|Kyoto|Yokohama|Nagoya|Kobe|Fukuoka|Sendai)\b', 
                  r'\b(Tokyo University|Todai|Kyoto University|Waseda|Keio|Hitotsubashi|Osaka University|Bank of Japan)\b'],
        'Australia': [r'\bAustralia\b', r'\b(Sydney|Melbourne|Brisbane|Perth|Adelaide|Canberra)\b',
                      r'\b(Australian National University|ANU|University of Sydney|Melbourne University|UNSW|Monash|Queensland|UQ|Western Australia|Adelaide University)\b',
                      r'\bReserve Bank of Australia\b'],
        'South Korea': [r'\bSouth Korea\b', r'\bKorea\b', r'\bRepublic of Korea\b',
                        r'\b(Seoul|Busan|Incheon|Daegu|Daejeon|Gwangju)\b',
                        r'\b(Seoul National|SNU|Korea University|Yonsei|KAIST|Sungkyunkwan|SKKU|Sogang|Hanyang|Ewha)\b',
                        r'\bBank of Korea\b', r'\bKDI\b'],
        'Netherlands': [r'\bNetherlands\b', r'\bHolland\b', r'\bDutch\b',
                        r'\b(Amsterdam|Rotterdam|Utrecht|Eindhoven|Groningen|Maastricht|Tilburg|Leiden|Delft)\b',
                        r'\b(University of Amsterdam|UvA|Erasmus|Tilburg University|VU Amsterdam|Maastricht University|Utrecht University|Groningen|Leiden|Tinbergen Institute)\b'],
        'Switzerland': [r'\bSwitzerland\b', r'\b(Zurich|Zürich|Geneva|Genève|Basel|Bern|Lausanne|St\.? Gallen)\b',
                        r'\b(ETH|University of Zurich|Geneva|Lausanne|EPFL|Basel|Bern|St\.? Gallen|Swiss National Bank|SNB)\b'],
        'Italy': [r'\bItaly\b', r'\b(Rome|Roma|Milan|Milano|Turin|Torino|Florence|Firenze|Bologna|Naples|Napoli|Padua|Padova|Venice|Venezia|Pisa)\b',
                  r'\b(Bocconi|Bologna|Padua|Sapienza|Tor Vergata|Ca\' Foscari|Bank of Italy|Banca d\'Italia)\b'],
        'Spain': [r'\bSpain\b', r'\b(Madrid|Barcelona|Valencia|Seville|Sevilla|Zaragoza|Málaga|Bilbao|Alicante)\b',
                  r'\b(Pompeu Fabra|UPF|Complutense|Autonomous University|UAB|UAM|Carlos III|UC3M|CEMFI|Barcelona GSE|Bank of Spain|IESE)\b'],
        'Sweden': [r'\bSweden\b', r'\b(Stockholm|Gothenburg|Göteborg|Malmö|Uppsala|Lund)\b',
                   r'\b(Stockholm School of Economics|SSE|Stockholm University|Uppsala University|Lund University|Karolinska|KTH|Sveriges Riksbank)\b'],
        'Norway': [r'\bNorway\b', r'\b(Oslo|Bergen|Trondheim|Stavanger)\b', r'\b(University of Oslo|UiO|Norwegian School of Economics|NHH|BI Norwegian)\b'],
        'Denmark': [r'\bDenmark\b', r'\b(Copenhagen|København|Aarhus|Aalborg|Odense)\b', r'\b(University of Copenhagen|Copenhagen Business School|CBS|Aarhus University)\b'],
        'Belgium': [r'\bBelgium\b', r'\b(Brussels|Bruxelles|Antwerp|Ghent|Leuven|Liège)\b', r'\b(KU Leuven|Université Libre de Bruxelles|ULB|Ghent University)\b'],
        'Austria': [r'\bAustria\b', r'\b(Vienna|Wien|Graz|Linz|Salzburg|Innsbruck)\b', r'\b(University of Vienna|Vienna University of Economics|WU Wien)\b'],
        'Singapore': [r'\bSingapore\b', r'\b(National University of Singapore|NUS|Nanyang|NTU|Singapore Management University|SMU)\b'],
        'India': [r'\bIndia\b', r'\b(Delhi|Mumbai|Bangalore|Bengaluru|Chennai|Kolkata|Hyderabad|Pune|Ahmedabad)\b',
                  r'\b(IIT|Indian Institute of Technology|IIM|Indian Institute of Management|Delhi School of Economics|ISI|Indian Statistical Institute|JNU|Reserve Bank of India|RBI)\b'],
        'Israel': [r'\bIsrael\b', r'\b(Jerusalem|Tel Aviv|Haifa|Be\'?er Sheva)\b', r'\b(Hebrew University|Tel Aviv University|Technion|Ben-Gurion|Bar-Ilan)\b'],
        'Brazil': [r'\bBrazil\b', r'\bBrasil\b', r'\b(São Paulo|Sao Paulo|Rio de Janeiro|Brasília|Brasilia|Belo Horizonte)\b',
                   r'\b(USP|University of São Paulo|FGV|Fundação Getulio Vargas|PUC|Central Bank of Brazil)\b'],
        'Mexico': [r'\bMexico\b', r'\bMéxico\b', r'\b(Mexico City|Ciudad de México|Guadalajara|Monterrey)\b',
                   r'\b(UNAM|ITAM|CIDE|Tec de Monterrey|Banco de México)\b'],
        'Chile': [r'\bChile\b', r'\b(Santiago|Valparaíso|Concepción)\b', r'\b(Universidad de Chile|Pontificia Universidad Católica|PUC)\b'],
        'Argentina': [r'\bArgentina\b', r'\b(Buenos Aires|Córdoba|Rosario|Mendoza)\b', r'\b(UBA|Universidad de Buenos Aires|UTDT|Torcuato Di Tella)\b'],
        'South Africa': [r'\bSouth Africa\b', r'\b(Cape Town|Johannesburg|Pretoria|Durban)\b',
                         r'\b(University of Cape Town|UCT|Stellenbosch|Witwatersrand|Wits|SARB)\b'],
        'New Zealand': [r'\bNew Zealand\b', r'\b(Auckland|Wellington|Christchurch)\b', r'\b(University of Auckland|Victoria University of Wellington|Otago)\b'],
        'Turkey': [r'\bTurkey\b', r'\bTürkiye\b', r'\b(Istanbul|Ankara|Izmir)\b', r'\b(Koç University|Bilkent|Boğaziçi|Bogazici)\b'],
    }
    
    for country, patterns in other_countries.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                countries.append(country)
                break
    
    # International Organizations
    international_patterns = [
        r'World Bank', r'IMF\b', r'International Monetary Fund',
        r'United Nations', r'OECD\b', r'ECB\b', r'European Central Bank',
        r'BIS\b', r'Bank for International Settlements'
    ]
    
    for pattern in international_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('International')
            break
    
    return countries

def get_subfield(title, abstract):
    """Classify article into subfield with improved matching"""
    # Combine title and abstract, handle NaN values
    title_text = str(title) if not pd.isna(title) else ''
    abstract_text = str(abstract) if not pd.isna(abstract) else ''
    text = f"{title_text} {abstract_text}".lower()
   
    # If both title and abstract are empty or very short, return Unclassified
    if len(text.strip()) < 10:
        return 'Unclassified'
   
    # Count keyword matches for each subfield with weighted scoring
    scores = {}
    for subfield, keywords in SUBFIELD_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Give more weight to multi-word phrases and specific terms
            if ' ' in keyword:  # Multi-word phrases get higher weight
                matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
                score += matches * 3
            else:
                matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text))
                score += matches
        scores[subfield] = score
   
    # Get top two scoring subfields
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    max_score = sorted_scores[0][1]
    second_score = sorted_scores[1][1] if len(sorted_scores) > 1 else 0
   
    # Return subfield with highest score if it's clearly ahead
    if max_score > 0:
        # If there's a clear winner (50% more than second place), use it
        if second_score == 0 or max_score >= second_score * 1.5:
            return sorted_scores[0][0]
        # If top two are close, check for specific high-priority matches
        else:
            # Check for very specific field indicators
            high_priority_terms = {
                'Econometrics': ['instrumental variable', 'regression discontinuity', 'difference in differences'],
                'Experimental Economics': ['randomized controlled trial', 'field experiment', 'laboratory experiment'],
                'Political Economy': ['election', 'voting', 'political'],
                'Law and Economics': ['crime', 'court', 'legal'],
                'Health Economics': ['health', 'medical', 'hospital', 'disease'],
                'Education Economics': ['school', 'student', 'teacher', 'education'],
                'Environmental Economics': ['climate change', 'carbon', 'pollution'],
                'Agricultural Economics': ['farm', 'agriculture', 'crop'],
            }
           
            for subfield, priority_terms in high_priority_terms.items():
                for term in priority_terms:
                    if term in text and scores.get(subfield, 0) > 0:
                        return subfield
           
            # Otherwise return the highest scoring one
            return sorted_scores[0][0]
   
    # Special checks for papers that might not use standard keywords
    # Check for methodology papers
    if any(word in text for word in ['methodology', 'estimation', 'identification', 'empirical', 'theoretical model']):
        if 'data' in text or 'evidence' in text:
            return 'Econometrics'
   
    # Check for review/survey papers
    if any(word in text for word in ['review', 'survey', 'literature', 'perspective']):
        # Try to classify based on the topic being reviewed
        if 'macro' in text:
            return 'Macroeconomics & Monetary'
        elif 'micro' in text:
            return 'Microeconomics'
        elif 'development' in text or 'growth' in text:
            return 'Development & Growth'
   
    # Check for theoretical papers
    if 'theory' in text or 'model' in text:
        if 'equilibrium' in text or 'optimization' in text:
            return 'Microeconomics'
        elif 'dynamic' in text and 'macro' in text:
            return 'Macroeconomics & Monetary'
   
    # If we have a Nobel lecture or similar special content
    if 'nobel' in text.lower():
        # Try to classify based on the content
        if 'finance' in text or 'asset' in text:
            return 'Finance'
        elif 'growth' in text or 'development' in text:
            return 'Development & Growth'
        elif 'behavior' in text or 'psychology' in text:
            return 'Behavioral Economics'
   
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
    df = pd.read_csv(input_file, low_memory=False)
   
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