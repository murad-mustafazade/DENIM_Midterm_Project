mport pandas as pd
import re
import swifter
from datetime import datetime
from collections import Counter

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
                     'measurement error', 'difference in differences', 'regression discontinuity',
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
    """Extract countries from institution text - comprehensive version"""
    if not institution_text or pd.isna(institution_text):
        return []
   
    countries = []
    text = str(institution_text)
   
    # USA - most comprehensive (check first for US-specific patterns)
    usa_patterns = [
        # Explicit country mentions
        r'\bUSA\b', r'\bU\.S\.A\.?\b', r'\bUnited States\b', r'\bU\.S\.\b',
        # State abbreviations with zip codes
        r', (AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\s*\d{5}',
        # State abbreviations before zip
        r'\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\s+\d{5}',
        # US-specific city mentions (Cambridge MA, not Cambridge UK)
        r'\bCambridge,?\s+(MA|Mass|Massachusetts)\b',
        r'\bOxford,?\s+(OH|Ohio|MS|Mississippi)\b',
        # Major US cities (excluding ambiguous ones)
        r'\b(New York|Boston|Chicago|Philadelphia|Los Angeles|San Francisco|Washington|Seattle|Atlanta|Dallas|Houston|Miami|Denver|Phoenix|San Diego|Baltimore|Detroit|Minneapolis|Pittsburgh|Cleveland|Milwaukee|Portland|Austin|Nashville|Indianapolis|Charlotte|Columbus|San Antonio|San Jose|Jacksonville|Fort Worth|Sacramento|Las Vegas|Kansas City|Memphis|Richmond|New Orleans|Cincinnati|Madison|Ann Arbor|Berkeley|Palo Alto|Princeton|Ithaca|Durham|Chapel Hill|Evanston|Stanford|Pasadena|Boulder|Providence|Hanover|Charlottesville|Amherst|Williamstown|Claremont|West Point|Annapolis|Tucson|Gainesville|Tallahassee|Tempe|Bloomington|Urbana|Champaign|Lafayette|College Station|Norman|Stillwater|Fayetteville|Little Rock|Baton Rouge|Lubbock|Raleigh|Greensboro|Winston-Salem|Columbia|Athens|Auburn|Tuscaloosa|Clemson|Knoxville|Lexington|Louisville|Eugene|Corvallis|Iowa City|Lincoln|Lawrence|Manhattan|Storrs|Newark|New Brunswick|Buffalo|Rochester|Albany|Syracuse|Binghamton|Stony Brook|Riverside|Irvine|Santa Barbara|Santa Cruz|Davis|Merced)\b',
        # US institutions (very specific names)
        r'\b(Harvard|Yale|Princeton|Stanford|MIT|Columbia|UCLA|UPenn|Penn|Cornell|Brown|Dartmouth|Duke|University of Chicago|Northwestern|Johns Hopkins|Caltech|University of Michigan|University of Virginia|University of Wisconsin|University of Illinois|University of Minnesota|University of Washington|University of Texas|University of North Carolina|University of Maryland|Purdue|Indiana University|Ohio State|Penn State|Rutgers|Georgetown|Vanderbilt|Emory|Carnegie Mellon|Rice|Notre Dame|USC|NYU|Boston University|Boston College|Tufts|Brandeis|University of Rochester|Case Western|Wake Forest|Georgia Tech|UC San Diego|UC Davis|UC Irvine|UC Santa Barbara|UC Riverside|William & Mary|Lehigh|Syracuse University|Tulane|George Washington|American University|Fordham|Northeastern|Pepperdine|SMU|TCU|Baylor|Villanova|Drexel|Temple|Arizona State|Florida State|Georgia State|SUNY|CUNY|NBER|Brookings|Hoover|RAND|Urban Institute)\b',
        # Federal institutions
        r'\bFederal Reserve\b', r'\bFed\b.*\b(Bank|Board)\b', r'\bNBER\b', r'\bNational Bureau of Economic Research\b',
        r'\bCensus Bureau\b', r'\bBureau of Labor Statistics\b', r'\bBLS\b', r'\bCBO\b', r'\bGAO\b',
        r'\bIMF.*Washington\b', r'\bWorld Bank.*Washington\b',
        # Business schools
        r'\b(Wharton|Booth|Sloan|Kellogg|Haas|Stern|Fuqua|Ross|Anderson|Tepper|McDonough|Kenan-Flagler|McCombs|Fisher|Kelley|Olin|Goizueta|Carey|Marshall|Foster)\b.*\b(School|Business)\b',
    ]
   
    for pattern in usa_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('USA')
            break
   
    # China - comprehensive
    china_patterns = [
        r'\bChina\b', r'\bP\.?R\.?\s*China\b', r'\bPeople\'?s Republic of China\b', r'\bMainland China\b',
        # Major cities
        r'\b(Beijing|Shanghai|Guangzhou|Shenzhen|Chengdu|Hangzhou|Wuhan|Nanjing|Xi\'?an|Tianjin|Chongqing|Suzhou|Dalian|Qingdao|Changsha|Xiamen|Harbin|Jinan|Fuzhou|Zhengzhou|Kunming|Lanzhou|Hefei|Nanchang|Shijiazhuang|Urumqi|Guiyang|Taiyuan|Hohhot|Nanning|Yinchuan|Xining|Shantou|Shenyang|Changchun|Ningbo|Wenzhou|Zhuhai|Dongguan|Foshan|Huizhou|Zhongshan|Jiangmen|Zhanjiang|Shaoguan|Qingyuan)\b',
        # Universities and institutions
        r'\b(Tsinghua|Peking University|PKU|Renmin|Fudan|Zhejiang University|Shanghai Jiao Tong|SJTU|Nanjing University|USTC|University of Science and Technology of China|Wuhan University|Sun Yat-sen|SYSU|Nankai|Xiamen University|Shandong University|Huazhong|Beihang|Beijing Normal|East China Normal|ECNU|Tongji|Tianjin University|Southeast University|Central University of Finance|CUFE|Shanghai University of Finance|SUFE|CASS|Chinese Academy|Nankai University|Zhongnan|Jiaotong|Southwestern|Sichuan University|Central South|Hunan University|Dongbei|Harbin Institute|Dalian University|Ocean University|China Agricultural|Beijing Institute of Technology|South China|Guangdong|Soochow|Jiangsu|Anhui|Hebei|Henan|Hubei|Hunan|Shaanxi|Shanxi|Jilin|Liaoning|Heilongjiang|Fujian|Jiangxi|Shandong|Guangxi|Guizhou|Yunnan|Gansu|Qinghai|Ningxia|Xinjiang|Inner Mongolia)\b.*\b(University|Institute|Academy)\b',
        # Hong Kong (separate but often grouped with China in data)
        r'\bHong Kong\b', r'\bHKU\b', r'\bCUHK\b', r'\bHKUST\b', r'\bCity University of Hong Kong\b', r'\bPolyU\b', r'\bLingnan\b.*\bHong Kong\b',
        # Macau
        r'\bMacau\b', r'\bMacao\b',
        # Chinese provinces when mentioned
        r'\b(Guangdong|Zhejiang|Jiangsu|Shandong|Henan|Sichuan|Hebei|Hunan|Anhui|Hubei|Fujian|Shaanxi|Jiangxi|Yunnan|Guangxi|Guizhou|Shanxi|Jilin|Gansu|Liaoning|Heilongjiang|Hainan|Qinghai|Ningxia|Tibet|Xinjiang|Inner Mongolia)\b.*\b(Province|China)\b',
    ]
   
    for pattern in china_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('China')
            break
   
    # Taiwan - separate from China
    taiwan_patterns = [
        r'\bTaiwan\b', r'\bR\.?O\.?C\.?\b', r'\bRepublic of China\b',
        r'\b(Taipei|Kaohsiung|Taichung|Tainan|Hsinchu)\b',
        r'\b(National Taiwan University|NTU|National Chengchi|NCCU|National Tsing Hua|NTHU|National Chiao Tung|NCTU|Academia Sinica)\b',
    ]
   
    for pattern in taiwan_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Taiwan')
            break
   
    # United Kingdom - only check if USA not already found
    if 'USA' not in countries:
        uk_patterns = [
            r'\bUnited Kingdom\b', r'\bU\.?K\.?\b', r'\bGreat Britain\b', r'\bEngland\b', r'\bScotland\b', r'\bWales\b', r'\bNorthern Ireland\b',
            # UK-specific mentions
            r'\bCambridge,?\s+(UK|England|United Kingdom)\b',
            r'\bOxford,?\s+(UK|England|United Kingdom)\b',
            # UK cities
            r'\b(London|Manchester|Birmingham|Edinburgh|Glasgow|Liverpool|Bristol|Leeds|Sheffield|Newcastle|Nottingham|Leicester|Southampton|Brighton|York|Warwick|Bath|Durham|St Andrews|Exeter|Cardiff|Aberdeen|Belfast|Coventry|Leicester|Reading|Canterbury|Norwich|Lancaster|Loughborough|Surrey|Sussex|Kent|Essex)\b.*\b(University|College|School)\b',
            # UK institutions
            r'\b(LSE|London School of Economics|Imperial College|UCL|University College London|King\'?s College|Queen Mary|Oxford|Cambridge|Edinburgh|Manchester|Bristol|Nottingham|Glasgow|Birmingham|Southampton|Durham|St Andrews|York|Exeter|Lancaster|Bath|Essex|Sussex|Kent|Reading|Sheffield|Leeds|Newcastle|Cardiff|Queen\'?s University Belfast|Strathclyde|Warwick|Leicester|Loughborough|Surrey|City University|Brunel|Goldsmiths)\b',
            r'\bUniversity of (Oxford|Cambridge|Edinburgh|Manchester|Bristol|Glasgow|Birmingham|Leeds|Sheffield|Southampton|Warwick|Durham|York|Exeter|Lancaster|Bath|St Andrews|Aberdeen|Dundee|Stirling)\b',
            r'\bBank of England\b', r'\bOffice for National Statistics\b', r'\bONS\b', r'\bIFS\b', r'\bInstitute for Fiscal Studies\b',
        ]
       
        for pattern in uk_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                countries.append('United Kingdom')
                break
   
    # Germany - comprehensive
    germany_patterns = [
        r'\bGermany\b', r'\bDeutschland\b',
        r'\b(Berlin|Munich|München|Hamburg|Frankfurt|Cologne|Köln|Stuttgart|Düsseldorf|Dortmund|Essen|Leipzig|Bremen|Dresden|Hannover|Nuremberg|Nürnberg|Mannheim|Heidelberg|Bonn|Münster|Karlsruhe|Freiburg|Konstanz|Tübingen|Göttingen|Marburg|Regensburg|Passau|Augsburg|Aachen|Bielefeld|Bochum|Wuppertal|Kiel|Mainz|Saarbrücken|Halle|Jena|Magdeburg|Rostock|Potsdam)\b',
        r'\b(Ludwig.*Maximilian|LMU|Humboldt|Freie Universität|Free University|TU Munich|Technical University of Munich|Heidelberg University|Mannheim|Frankfurt School|Goethe University|University of Bonn|ZEW|Ifo Institute|DIW|Bundesbank|Max Planck|IZA|WHU|EBS|ESMT|Konstanz|Tübingen|Göttingen|Regensburg|Passau|Bayreuth|Hohenheim|Duisburg-Essen)\b',
    ]
   
    for pattern in germany_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Germany')
            break
   
    # France - comprehensive
    france_patterns = [
        r'\bFrance\b',
        r'\b(Paris|Lyon|Marseille|Toulouse|Nice|Nantes|Strasbourg|Montpellier|Bordeaux|Lille|Rennes|Grenoble|Aix|Aix-Marseille|Dijon|Clermont|Orléans|Tours|Angers|Cergy|Saclay)\b',
        r'\b(Sorbonne|École|Ecole|Sciences Po|PSE|Paris School of Economics|INSEAD|HEC Paris|Toulouse School of Economics|TSE|EHESS|ENS|Polytechnique|Paris-Dauphine|Panthéon|Pantheon|CREST|CNRS|INRA|INRAE|Aix-Marseille|Université Paris|PSL|AMSE|GATE|CREST|TSM|Montpellier Business School|EDHEC|ESSEC|ESCP|Grenoble École|Audencia|SKEMA|IESEG)\b',
        r'\bBanque de France\b',
    ]
   
    for pattern in france_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('France')
            break
   
    # Canada - comprehensive
    canada_patterns = [
        r'\bCanada\b',
        r'\b(Toronto|Montreal|Montréal|Vancouver|Ottawa|Calgary|Edmonton|Winnipeg|Quebec|Québec|Hamilton|Kitchener|Victoria|Halifax|Saskatoon|Kingston|Waterloo|London|Windsor|Oshawa|Burnaby|Surrey)\b',
        r'\b(University of Toronto|UofT|U of T|McGill|UBC|University of British Columbia|McMaster|Queen\'?s University|Alberta|Calgary|Western Ontario|Waterloo|Simon Fraser|SFU|York University|Carleton|Dalhousie|Laval|Concordia|Ottawa|Manitoba|Saskatchewan|Memorial|Ryerson|Wilfrid Laurier|Guelph|Rotman|Sauder|Desautels|Ivey|Schulich)\b',
        r'\bBank of Canada\b', r'\bStatistics Canada\b', r'\bCIFAR\b',
    ]
   
    for pattern in canada_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Canada')
            break
   
    # Japan - comprehensive
    japan_patterns = [
        r'\bJapan\b',
        r'\b(Tokyo|Osaka|Kyoto|Yokohama|Nagoya|Kobe|Fukuoka|Sapporo|Sendai|Hiroshima|Kawasaki|Saitama|Kitakyushu|Chiba|Niigata|Hamamatsu|Kumamoto|Okayama|Shizuoka|Kagoshima)\b',
        r'\b(Tokyo University|University of Tokyo|Kyoto University|Waseda|Keio|Hitotsubashi|Osaka University|Tohoku University|Nagoya University|Kyushu University|Hokkaido University|Tsukuba|Kobe University|Sophia|Meiji|Doshisha|Ritsumeikan|Chuo|Hosei|Aoyama Gakuin|Kwansei Gakuin|Gakuin University|Bank of Japan|RIETI)\b',
    ]
   
    for pattern in japan_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Japan')
            break
   
    # South Korea - comprehensive
    korea_patterns = [
        r'\bSouth Korea\b', r'\bKorea\b', r'\bRepublic of Korea\b', r'\bR\.?O\.?K\.?\b',
        r'\b(Seoul|Busan|Incheon|Daegu|Daejeon|Gwangju|Ulsan|Suwon|Goyang|Seongnam|Bucheon|Ansan)\b',
        r'\b(Seoul National|SNU|Korea University|Yonsei|KAIST|Sungkyunkwan|SKKU|Sogang|Hanyang|Ewha|Kyung Hee|Chung-Ang|Korea Advanced Institute|Pohang|POSTECH|Ajou|Inha|Pusan National|Konkuk|Dongguk|Hankuk|KDI|Bank of Korea)\b',
    ]
   
    for pattern in korea_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('South Korea')
            break
   
    # India - comprehensive
    india_patterns = [
        r'\bIndia\b',
        r'\b(Delhi|New Delhi|Mumbai|Bombay|Bangalore|Bengaluru|Chennai|Madras|Kolkata|Calcutta|Hyderabad|Pune|Ahmedabad|Jaipur|Lucknow|Kanpur|Nagpur|Indore|Bhopal|Patna|Vadodara|Ludhiana|Agra|Nashik|Rajkot|Varanasi|Surat|Visakhapatnam|Kochi|Thiruvananthapuram|Coimbatore|Chandigarh|Gurgaon|Noida|Ghaziabad|Bodh Gaya)\b',
        r'\b(IIT|Indian Institute of Technology|IIM|Indian Institute of Management|Delhi School of Economics|ISI|Indian Statistical Institute|JNU|Jawaharlal Nehru|ISB|Indian School of Business|IGIDR|Indira Gandhi Institute|TISS|Tata Institute|XLRI|FMS|MDI|NIBM|NIFM|NIPFP|NCAER|Reserve Bank of India|RBI|IIFT|ICRIER|Ashoka University|Azim Premji|O\.?P\.? Jindal)\b',
    ]
   
    for pattern in india_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('India')
            break
   
    # Australia - comprehensive
    australia_patterns = [
        r'\bAustralia\b',
        r'\b(Sydney|Melbourne|Brisbane|Perth|Adelaide|Canberra|Gold Coast|Newcastle|Wollongong|Geelong|Hobart|Townsville|Cairns|Toowoomba|Darwin|Launceston)\b',
        r'\b(Australian National University|ANU|University of Sydney|Melbourne University|University of Melbourne|UNSW|University of New South Wales|Monash|University of Queensland|UQ|Western Australia|UWA|Adelaide University|Macquarie|Queensland University of Technology|QUT|RMIT|Deakin|Curtin|Griffith|La Trobe|Swinburne|Reserve Bank of Australia|RBA)\b',
    ]
   
    for pattern in australia_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Australia')
            break
   
    # Netherlands - comprehensive
    netherlands_patterns = [
        r'\bNetherlands\b', r'\bHolland\b', r'\bDutch\b',
        r'\b(Amsterdam|Rotterdam|The Hague|Utrecht|Eindhoven|Groningen|Maastricht|Tilburg|Leiden|Delft|Nijmegen|Enschede|Wageningen)\b',
        r'\b(University of Amsterdam|UvA|Erasmus|Tilburg University|VU Amsterdam|Vrije Universiteit|Maastricht University|Utrecht University|Groningen|Leiden|Tinbergen Institute|Wageningen|Radboud|Eindhoven University of Technology|TU Delft|De Nederlandsche Bank|DNB)\b',
    ]
   
    for pattern in netherlands_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Netherlands')
            break
   
    # Switzerland - comprehensive
    switzerland_patterns = [
        r'\bSwitzerland\b',
        r'\b(Zurich|Zürich|Geneva|Genève|Basel|Bern|Lausanne|St\.? Gallen|Lugano|Lucerne|Neuchâtel|Fribourg)\b',
        r'\b(ETH|University of Zurich|Geneva|Université de Genève|Lausanne|EPFL|Basel|Bern|St\.? Gallen|Lugano|Swiss National Bank|SNB|KOF|Zurich University|UZH)\b',
    ]
   
    for pattern in switzerland_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Switzerland')
            break
   
    # Italy - comprehensive
    italy_patterns = [
        r'\bItaly\b', r'\bItalia\b',
        r'\b(Rome|Roma|Milan|Milano|Turin|Torino|Florence|Firenze|Bologna|Naples|Napoli|Padua|Padova|Venice|Venezia|Pisa|Genoa|Genova|Palermo|Verona|Trieste|Trento|Perugia|Modena|Parma|Ancona|Siena|Bergamo|Brescia|Udine|Cagliari|Sassari|Catania|Bari|Salerno|Macerata)\b',
        r'\b(Bocconi|University of Bologna|Padua|Sapienza|Tor Vergata|Ca\' Foscari|Bank of Italy|Banca d\'Italia|Università|Milan|Bologna|Padova|Roma|Torino|Firenze|Pisa|Cattolica|LUISS|Politecnico|Sant\'Anna|IMT Lucca|European University Institute|EUI)\b',
    ]
   
    for pattern in italy_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Italy')
            break
   
    # Spain - comprehensive
    spain_patterns = [
        r'\bSpain\b', r'\bEspaña\b',
        r'\b(Madrid|Barcelona|Valencia|Seville|Sevilla|Zaragoza|Málaga|Malaga|Bilbao|Alicante|Córdoba|Cordoba|Valladolid|Vigo|Gijón|Granada|Pamplona|Oviedo|Santander|San Sebastián|Murcia|Salamanca|Coruña|Corunna)\b',
        r'\b(Pompeu Fabra|UPF|Complutense|Autonomous University|Autónoma|Autònoma|UAB|UAM|Carlos III|UC3M|CEMFI|Barcelona GSE|Bank of Spain|Banco de España|Universidad|Politécnica|Politecnica|IESE|ESADE|IE Business School|Ramon Llull|Navarra|Deusto|Comillas)\b',
    ]
   
    for pattern in spain_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Spain')
            break
   
    # Scandinavian countries - comprehensive
    sweden_patterns = [
        r'\bSweden\b',
        r'\b(Stockholm|Gothenburg|Göteborg|Malmö|Uppsala|Lund|Linköping|Örebro|Västerås|Umeå)\b',
        r'\b(Stockholm School of Economics|SSE|Stockholm University|Uppsala University|Lund University|Karolinska|KTH|Gothenburg University|Linköping University|Sveriges Riksbank|IFN)\b',
    ]
   
    norway_patterns = [
        r'\bNorway\b',
        r'\b(Oslo|Bergen|Trondheim|Stavanger|Drammen|Kristiansand|Tromsø)\b',
        r'\b(University of Oslo|UiO|Norwegian School of Economics|NHH|BI Norwegian|NTNU|Norwegian University of Science|University of Bergen|Norges Bank)\b',
    ]
   
    denmark_patterns = [
        r'\bDenmark\b',
        r'\b(Copenhagen|København|Aarhus|Aalborg|Odense|Esbjerg|Roskilde)\b',
        r'\b(University of Copenhagen|Copenhagen Business School|CBS|Aarhus University|Aalborg University|Danmarks Nationalbank)\b',
    ]
   
    finland_patterns = [
        r'\bFinland\b',
        r'\b(Helsinki|Espoo|Tampere|Turku|Oulu|Jyväskylä|Lahti|Kuopio|Vaasa)\b',
        r'\b(University of Helsinki|Aalto University|Hanken|Turku School of Economics|Bank of Finland|Suomen Pankki)\b',
    ]
   
    for pattern in sweden_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Sweden')
            break
   
    for pattern in norway_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Norway')
            break
   
    for pattern in denmark_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Denmark')
            break
   
    for pattern in finland_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Finland')
            break
   
    # Other European countries
    belgium_patterns = [
        r'\bBelgium\b', r'\bBelgique\b', r'\bBelgië\b',
        r'\b(Brussels|Bruxelles|Antwerp|Antwerpen|Ghent|Gent|Leuven|Louvain|Liège|Bruges|Namur|Mons)\b',
        r'\b(KU Leuven|Katholieke Universiteit Leuven|Université Libre de Bruxelles|ULB|Ghent University|Université Catholique de Louvain|UCLouvain|Antwerp University|VUB|ECARES)\b',
    ]
   
    austria_patterns = [
        r'\bAustria\b', r'\bÖsterreich\b',
        r'\b(Vienna|Wien|Graz|Linz|Salzburg|Innsbruck|Klagenfurt)\b',
        r'\b(University of Vienna|Vienna University of Economics|WU Wien|Wirtschaftsuniversität|Graz University|Johannes Kepler|Innsbruck University)\b',
    ]
   
    portugal_patterns = [
        r'\bPortugal\b',
        r'\b(Lisbon|Lisboa|Porto|Oporto|Braga|Coimbra|Aveiro|Évora|Faro|Guimarães)\b',
        r'\b(Nova|Universidade Nova|Católica|Catholic University|ISEG|Lisbon School of Economics|Porto Business School|University of Porto|Coimbra University|Banco de Portugal)\b',
    ]
   
    greece_patterns = [
        r'\bGreece\b',
        r'\b(Athens|Athina|Thessaloniki|Patras|Heraklion|Larissa|Piraeus)\b',
        r'\b(Athens University of Economics|AUEB|National.*Technical University of Athens|Aristotle University|University of Crete|Bank of Greece)\b',
    ]
   
    ireland_patterns = [
        r'\bIreland\b',
        r'\b(Dublin|Cork|Galway|Limerick|Waterford)\b',
        r'\b(Trinity College Dublin|TCD|University College Dublin|UCD|Dublin City University|DCU|National University of Ireland|NUIG|Central Bank of Ireland)\b',
    ]
   
    for pattern in belgium_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Belgium')
            break
   
    for pattern in austria_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Austria')
            break
   
    for pattern in portugal_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Portugal')
            break
   
    for pattern in greece_patterns:
        if re.search(pattern, text, re.
                     
IGNORECASE):
            countries.append('Greece')
            break
   
    for pattern in ireland_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Ireland')
            break
   
    # Eastern European countries
    poland_patterns = [
        r'\bPoland\b', r'\bPolska\b',
        r'\b(Warsaw|Warszawa|Kraków|Krakow|Łódź|Lodz|Wrocław|Wroclaw|Poznań|Poznan|Gdańsk|Gdansk|Szczecin|Lublin)\b',
        r'\b(Warsaw School of Economics|SGH|University of Warsaw|Jagiellonian|Kozminski|Warsaw University)\b',
    ]
   
    czech_patterns = [
        r'\bCzech Republic\b', r'\bCzechia\b',
        r'\b(Prague|Praha|Brno|Ostrava|Pilsen|Plzeň|Hradec|Králové)\b',
        r'\b(Charles University|CERGE-EI|Czech National Bank|ČNB)\b',
    ]
   
    hungary_patterns = [
        r'\bHungary\b',
        r'\b(Budapest|Debrecen|Szeged|Miskolc|Pécs|Győr)\b',
        r'\b(Central European University|CEU|Corvinus|Budapest University|Eötvös Loránd|Magyar Nemzeti Bank)\b',
    ]
   
    romania_patterns = [
        r'\bRomania\b', r'\bRomânia\b',
        r'\b(Bucharest|București|Cluj|Timișoara|Timisoara|Iași|Iasi|Constanța|Constanta|Craiova|Brașov|Brasov|Galați|Galati)\b',
        r'\b(Bucharest University|Babeș-Bolyai|Babes-Bolyai|Alexandru Ioan Cuza|Academy of Economic Studies)\b',
    ]
   
    for pattern in poland_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Poland')
            break
   
    for pattern in czech_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Czech Republic')
            break
   
    for pattern in hungary_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Hungary')
            break
   
    for pattern in romania_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Romania')
            break
   
    # Other European countries
    russia_patterns = [
        r'\bRussia\b', r'\bRussian Federation\b',
        r'\b(Moscow|Moskva|St\.? Petersburg|Novosibirsk|Yekaterinburg|Kazan|Nizhny Novgorod)\b',
        r'\b(Moscow State University|MSU|Higher School of Economics|HSE|St\.? Petersburg State|RANEPA|Central Bank of Russia)\b',
    ]
   
    turkey_patterns = [
        r'\bTurkey\b', r'\bTürkiye\b',
        r'\b(Istanbul|Ankara|Izmir|Bursa|Antalya|Adana)\b',
        r'\b(Koç University|Bilkent|Boğaziçi|Bogazici|Middle East Technical|METU|Sabancı|Sabanci|Central Bank.*Turkey)\b',
    ]
   
    ukraine_patterns = [
        r'\bUkraine\b',
        r'\b(Kyiv|Kiev|Kharkiv|Odesa|Odessa|Dnipro|Lviv)\b',
        r'\b(Kyiv School of Economics|KSE|National University.*Kyiv|Taras Shevchenko)\b',
    ]
   
    for pattern in russia_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Russia')
            break
   
    for pattern in turkey_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Turkey')
            break
   
    for pattern in ukraine_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Ukraine')
            break
   
    # Singapore
    singapore_patterns = [
        r'\bSingapore\b',
        r'\b(National University of Singapore|NUS|Nanyang|NTU|Singapore Management University|SMU|INSEAD.*Singapore|Monetary Authority of Singapore|MAS)\b',
    ]
   
    for pattern in singapore_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Singapore')
            break
   
    # Israel
    israel_patterns = [
        r'\bIsrael\b',
        r'\b(Jerusalem|Tel Aviv|Haifa|Be\'?er Sheva|Beersheba|Ramat Gan|Herzliya)\b',
        r'\b(Hebrew University|Tel Aviv University|Technion|Ben-Gurion|Bar-Ilan|Reichman|IDC Herzliya|Weizmann Institute|Bank of Israel)\b',
    ]
   
    for pattern in israel_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Israel')
            break
   
    # New Zealand
    new_zealand_patterns = [
        r'\bNew Zealand\b',
        r'\b(Auckland|Wellington|Christchurch|Hamilton|Tauranga|Dunedin|Palmerston North|Napier|Waikato)\b',
        r'\b(University of Auckland|Victoria University of Wellington|Canterbury University|Otago|Waikato University|Massey|Auckland University of Technology|AUT|Reserve Bank of New Zealand|RBNZ)\b',
    ]
   
    for pattern in new_zealand_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('New Zealand')
            break
   
    # Latin American countries - comprehensive
    brazil_patterns = [
        r'\bBrazil\b', r'\bBrasil\b',
        r'\b(São Paulo|Sao Paulo|Rio de Janeiro|Brasília|Brasilia|Belo Horizonte|Salvador|Fortaleza|Curitiba|Recife|Porto Alegre|Manaus|Campinas|Goiânia|Goiania)\b',
        r'\b(USP|University of São Paulo|Universidade de São Paulo|FGV|Fundação Getulio Vargas|Getulio Vargas|PUC|Pontifícia|Universidade Federal|UFRJ|Unicamp|INSPER|Central Bank of Brazil|Banco Central do Brasil)\b',
    ]
   
    mexico_patterns = [
        r'\bMexico\b', r'\bMéxico\b',
        r'\b(Mexico City|Ciudad de México|CDMX|Guadalajara|Monterrey|Puebla|Tijuana|León|Juárez|Querétaro|Queretaro)\b',
        r'\b(UNAM|Universidad Nacional Autónoma|ITAM|Instituto Tecnológico Autónomo|CIDE|Centro de Investigación|Tec de Monterrey|Tecnológico de Monterrey|Colegio de México|Colmex|Banco de México|Banxico)\b',
    ]
   
    chile_patterns = [
        r'\bChile\b',
        r'\b(Santiago|Valparaíso|Valparaiso|Concepción|Concepcion|La Serena|Antofagasta|Temuco|Viña del Mar)\b',
        r'\b(Universidad de Chile|Pontificia Universidad Católica|PUC Chile|Universidad de Santiago|Universidad Adolfo Ibáñez|UAI|Universidad del Desarrollo|UDD|Central Bank of Chile)\b',
    ]
   
    argentina_patterns = [
        r'\bArgentina\b',
        r'\b(Buenos Aires|Córdoba|Cordoba|Rosario|Mendoza|La Plata|San Miguel de Tucumán|Mar del Plata)\b',
        r'\b(UBA|Universidad de Buenos Aires|UTDT|Torcuato Di Tella|Universidad de San Andrés|UCEMA|Universidad Nacional de La Plata|UNLP|Universidad Nacional de Córdoba|UNC|BCRA)\b',
    ]
   
    colombia_patterns = [
        r'\bColombia\b',
        r'\b(Bogotá|Bogota|Medellín|Medellin|Cali|Barranquilla|Cartagena|Bucaramanga)\b',
        r'\b(Universidad de los Andes|Uniandes|Universidad Nacional de Colombia|Javeriana|Universidad del Rosario|EAFIT|Universidad del Valle|Banco de la República)\b',
    ]
   
    peru_patterns = [
        r'\bPeru\b', r'\bPerú\b',
        r'\b(Lima|Arequipa|Trujillo|Chiclayo|Cusco|Cuzco)\b',
        r'\b(Universidad del Pacífico|Universidad del Pacifico|Pontificia Universidad Católica del Perú|PUCP|Universidad de Lima|ESAN)\b',
    ]
   
    for pattern in brazil_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Brazil')
            break
   
    for pattern in mexico_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Mexico')
            break
   
    for pattern in chile_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Chile')
            break
   
    for pattern in argentina_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Argentina')
            break
   
    for pattern in colombia_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Colombia')
            break
   
    for pattern in peru_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Peru')
            break
   
    # Other Latin American countries
    other_latin_america = {
        'Ecuador': [r'\bEcuador\b', r'\b(Quito|Guayaquil)\b'],
        'Venezuela': [r'\bVenezuela\b', r'\b(Caracas|Maracaibo|Valencia)\b'],
        'Uruguay': [r'\bUruguay\b', r'\b(Montevideo)\b', r'\bUniversidad de la República\b'],
        'Costa Rica': [r'\bCosta Rica\b', r'\b(San José|San Jose)\b'],
        'Panama': [r'\bPanama\b', r'\bPanamá\b'],
        'Guatemala': [r'\bGuatemala\b'],
    }
   
    for country, patterns in other_latin_america.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                countries.append(country)
                break
   
    # Middle Eastern countries
    saudi_arabia_patterns = [
        r'\bSaudi Arabia\b',
        r'\b(Riyadh|Jeddah|Mecca|Medina|Dammam|Khobar|Dhahran)\b',
        r'\b(King Saud University|King Fahd University|KFUPM|King Abdullah University|KAUST|King Abdulaziz University)\b',
    ]
   
    uae_patterns = [
        r'\bUnited Arab Emirates\b', r'\bU\.?A\.?E\.?\b', r'\bEmirates\b',
        r'\b(Dubai|Abu Dhabi|Sharjah|Ajman|Al Ain)\b',
        r'\b(American University.*Dubai|AUD|Zayed University|UAE University|New York University.*Abu Dhabi|NYUAD|Khalifa University)\b',
    ]
   
    qatar_patterns = [
        r'\bQatar\b',
        r'\b(Doha|Al Rayyan)\b',
        r'\b(Qatar University|Georgetown.*Qatar|Northwestern.*Qatar|Carnegie Mellon.*Qatar|Qatar Foundation)\b',
    ]
   
    iran_patterns = [
        r'\bIran\b',
        r'\b(Tehran|Isfahan|Mashhad|Tabriz|Shiraz|Karaj)\b',
        r'\b(University of Tehran|Sharif University|Amirkabir University)\b',
    ]
   
    lebanon_patterns = [
        r'\bLebanon\b',
        r'\b(Beirut|Tripoli|Sidon)\b',
        r'\b(American University of Beirut|AUB|Lebanese American University|LAU)\b',
    ]
   
    jordan_patterns = [
        r'\bJordan\b',
        r'\b(Amman|Zarqa|Irbid)\b',
        r'\b(University of Jordan|Jordan University)\b',
    ]
   
    for pattern in saudi_arabia_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Saudi Arabia')
            break
   
    for pattern in uae_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('United Arab Emirates')
            break
   
    for pattern in qatar_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Qatar')
            break
   
    for pattern in iran_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Iran')
            break
   
    for pattern in lebanon_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Lebanon')
            break
   
    for pattern in jordan_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Jordan')
            break
   
    # African countries
    south_africa_patterns = [
        r'\bSouth Africa\b',
        r'\b(Cape Town|Johannesburg|Durban|Pretoria|Port Elizabeth|Bloemfontein|Pietermaritzburg|East London|Soweto|Stellenbosch)\b',
        r'\b(University of Cape Town|UCT|Stellenbosch University|Witwatersrand|Wits|University of Pretoria|Johannesburg|UJ|KwaZulu-Natal|UKZN|Rhodes|Walter Sisulu|South African Reserve Bank|SARB)\b',
    ]
   
    egypt_patterns = [
        r'\bEgypt\b',
        r'\b(Cairo|Alexandria|Giza|Shubra El-Kheima)\b',
        r'\b(Cairo University|American University in Cairo|AUC|Ain Shams University|Alexandria University)\b',
    ]
   
    kenya_patterns = [
        r'\bKenya\b',
        r'\b(Nairobi|Mombasa|Kisumu|Nakuru)\b',
        r'\b(University of Nairobi|Kenyatta University|Strathmore University)\b',
    ]
   
    nigeria_patterns = [
        r'\bNigeria\b',
        r'\b(Lagos|Abuja|Kano|Ibadan|Port Harcourt|Benin City)\b',
        r'\b(University of Lagos|UNILAG|University of Ibadan|Obafemi Awolowo|Ahmadu Bello)\b',
    ]
   
    ethiopia_patterns = [
        r'\bEthiopia\b',
        r'\b(Addis Ababa|Dire Dawa|Mekelle|Gondar)\b',
        r'\b(Addis Ababa University|Mekelle University)\b',
    ]
   
    morocco_patterns = [
        r'\bMorocco\b', r'\bMaroc\b',
        r'\b(Casablanca|Rabat|Fès|Fez|Marrakech|Tangier|Agadir)\b',
    ]
   
    tunisia_patterns = [
        r'\bTunisia\b', r'\bTunisie\b',
        r'\b(Tunis|Sfax|Sousse|Jendouba)\b',
        r'\b(University of Tunis|Université de Tunis)\b',
    ]
   
    ghana_patterns = [
        r'\bGhana\b',
        r'\b(Accra|Kumasi|Tamale|Sekondi-Takoradi)\b',
        r'\b(University of Ghana|Kwame Nkrumah University)\b',
    ]
   
    for pattern in south_africa_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('South Africa')
            break
   
    for pattern in egypt_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Egypt')
            break
   
    for pattern in kenya_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Kenya')
            break
   
    for pattern in nigeria_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Nigeria')
            break
   
    for pattern in ethiopia_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Ethiopia')
            break
   
    for pattern in morocco_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Morocco')
            break
   
    for pattern in tunisia_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Tunisia')
            break
   
    for pattern in ghana_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Ghana')
            break
   
    # Southeast Asian countries
    thailand_patterns = [
        r'\bThailand\b',
        r'\b(Bangkok|Chiang Mai|Phuket|Pattaya|Nakhon Ratchasima)\b',
        r'\b(Chulalongkorn|Thammasat|Mahidol|Kasetsart|AIT|Asian Institute of Technology|Bank of Thailand)\b',
    ]
   
    indonesia_patterns = [
        r'\bIndonesia\b',
        r'\b(Jakarta|Surabaya|Bandung|Medan|Semarang|Makassar|Palembang|Tangerang|Depok|Bogor|Yogyakarta|Malang)\b',
        r'\b(UI|Universitas Indonesia|UGM|Gadjah Mada|ITB|Institut Teknologi Bandung|IPB|Bogor Agricultural|Airlangga|Diponegoro|Hasanuddin|Padjadjaran|Brawijaya|Bank Indonesia)\b',
    ]
   
    malaysia_patterns = [
        r'\bMalaysia\b',
        r'\b(Kuala Lumpur|George Town|Penang|Johor Bahru|Ipoh|Shah Alam|Petaling Jaya|Selangor|Bandar|Subang)\b',
        r'\b(UM|University of Malaya|Universiti Malaya|UKM|Universiti Kebangsaan|UPM|Universiti Putra|USM|Universiti Sains Malaysia|UTM|Universiti Teknologi|IIUM|Bank Negara Malaysia)\b',
    ]
   
    philippines_patterns = [
        r'\bPhilippines\b',
        r'\b(Manila|Quezon City|Davao|Cebu|Zamboanga|Antipolo|Cagayan de Oro)\b',
        r'\b(UP|University of the Philippines|Ateneo de Manila|De La Salle|DLSU|University of Santo Tomas|UST|Bangko Sentral ng Pilipinas|BSP)\b',
    ]
   
    vietnam_patterns = [
        r'\bVietnam\b', r'\bViet Nam\b',
        r'\b(Hanoi|Ho Chi Minh City|Saigon|Da Nang|Hai Phong|Can Tho|Hue)\b',
        r'\b(VNU|Vietnam National University|Foreign Trade University|FTU|National Economics University|NEU|State Bank of Vietnam)\b',
    ]
   
    for pattern in thailand_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Thailand')
            break
   
    for pattern in indonesia_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Indonesia')
            break
   
    for pattern in malaysia_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Malaysia')
            break
   
    for pattern in philippines_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Philippines')
            break
   
    for pattern in vietnam_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Vietnam')
            break
   
    # Central Asian countries
    kazakhstan_patterns = [
        r'\bKazakhstan\b',
        r'\b(Almaty|Nur-Sultan|Astana|Shymkent|Aktobe|Karaganda)\b',
        r'\b(Al-Farabi|Kazakh National University)\b',
    ]
   
    uzbekistan_patterns = [
        r'\bUzbekistan\b',
        r'\b(Tashkent|Samarkand|Namangan|Andijan|Urgench)\b',
    ]
   
    azerbaijan_patterns = [
        r'\bAzerbaijan\b',
        r'\b(Baku|Ganja|Sumqayit)\b',
    ]
   
    for pattern in kazakhstan_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Kazakhstan')
            break
   
    for pattern in uzbekistan_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Uzbekistan')
            break
   
    for pattern in azerbaijan_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Azerbaijan')
            break
   
    # Other European countries
    other_europe = {
        'Slovakia': [r'\bSlovakia\b', r'\b(Bratislava|Košice|Kosice|Žilina|Zilina)\b'],
        'Slovenia': [r'\bSlovenia\b', r'\b(Ljubljana|Maribor)\b'],
        'Croatia': [r'\bCroatia\b', r'\b(Zagreb|Split|Rijeka|Pula)\b'],
        'Serbia': [r'\bSerbia\b', r'\b(Belgrade|Beograd|Novi Sad|Niš)\b'],
        'Bulgaria': [r'\bBulgaria\b', r'\b(Sofia|Plovdiv|Varna|Burgas)\b'],
        'Lithuania': [r'\bLithuania\b', r'\b(Vilnius|Kaunas|Klaipėda|Klaipeda)\b'],
        'Latvia': [r'\bLatvia\b', r'\b(Riga|Daugavpils|Liepāja|Liepaja)\b'],
        'Estonia': [r'\bEstonia\b', r'\b(Tallinn|Tartu|Narva)\b'],
        'Cyprus': [r'\bCyprus\b', r'\b(Nicosia|Limassol|Larnaca)\b'],
        'Luxembourg': [r'\bLuxembourg\b'],
        'Malta': [r'\bMalta\b', r'\b(Valletta)\b'],
        'Iceland': [r'\bIceland\b', r'\b(Reykjavik|Reykjavík)\b'],
    }
   
    for country, patterns in other_europe.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                countries.append(country)
                break
   
    # Other Asian countries
    pakistan_patterns = [
        r'\bPakistan\b',
        r'\b(Karachi|Lahore|Islamabad|Rawalpindi|Faisalabad|Multan|Peshawar|Quetta)\b',
        r'\b(LUMS|Lahore University of Management Sciences|Pakistan Institute of Development Economics|PIDE|COMSATS|State Bank of Pakistan)\b',
    ]
   
    bangladesh_patterns = [
        r'\bBangladesh\b',
        r'\b(Dhaka|Chittagong|Khulna|Rajshahi|Sylhet)\b',
        r'\b(Dhaka University|Bangladesh University)\b',
    ]
   
    sri_lanka_patterns = [
        r'\bSri Lanka\b',
        r'\b(Colombo|Kandy|Galle|Jaffna)\b',
    ]
   
    for pattern in pakistan_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Pakistan')
            break
   
    for pattern in bangladesh_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Bangladesh')
            break
   
    for pattern in sri_lanka_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            countries.append('Sri Lanka')
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
    df = pd.read_csv(input_file, low_memory=False)
   
    # Clean abstracts
    print("Cleaning abstracts...")
    df['abstract'] = df['abstract'].swifter.apply(clean_abstract)
   
    # Extract countries
    print("Extracting countries...")
    df['countries_list'] = df['institutions'].swifter.apply(get_countries)
    df['countries'] = df['countries_list'].swifter.apply(lambda x: '; '.join(x))
    df['has_china_author'] = df['countries_list'].swifter.apply(lambda x: 'China' in x)
   
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
   
    # Print country distribution
    print("\nCountry distribution:")
    all_countries = []
    for countries_str in df['countries']:
        if countries_str:
            all_countries.extend(countries_str.split('; '))
   
    from collections import Counter
    country_counts = Counter(all_countries)
    for country, count in country_counts.most_common(30):
        print(f"  {country}: {count}")

if _name_ == "_main_":
    main()