import requests
import pandas as pd
import time
from datetime import datetime

JOURNALS = {
    'Top 5': {
        "American Economic Review": "0002-8282",
        "Quarterly Journal of Economics": "0033-5533",
        "Journal of Political Economy": "0022-3808",
        "Econometrica": "0012-9682",
        "Review of Economic Studies": "0034-6527",
    },
    'Top Field Journals': {
        "Journal of Finance": "0022-1082",
        "Journal of Financial Economics": "0304-405X",
        "Journal of Monetary Economics": "0304-3932",
        "Journal of International Economics": "0022-1996",
        "Journal of Public Economics": "0047-2727",
        "Journal of Labor Economics": "0734-306X",
        "Journal of Development Economics": "0304-3878",
        "Journal of Urban Economics": "0094-1190",
        "Journal of Health Economics": "0167-6296",
        "Review of Financial Studies": "0893-9454",
    },
    'Mid-Tier': {
        "Economic Inquiry": "0095-2583",
        "Southern Economic Journal": "0038-4038",
        "Applied Economics": "0003-6846",
        "European Economic Review": "0014-2921",
        "Journal of Economic Behavior & Organization": "0167-2681",
        "Economics Letters": "0165-1765",
        "Oxford Economic Papers": "0030-7653",
        "International Economic Review": "0020-6598",
    },
    'Lower-Tier & Regional': {
        "China Economic Review": "1043-951X",
        "World Development": "0305-750X",
        "Emerging Markets Review": "1566-0141",
        "Modern Economy": "2152-7261",
        "International Journal of Economics and Finance": "1916-971X",
        "Theoretical Economics Letters": "2162-2078",
        "Economies": "2227-7099",
    }
}
def download_journal(journal_name, issn, tier, from_year=2005, to_year=2025):
    """Download articles from one journal using Crossref API"""
    
    base_url = f"https://api.crossref.org/journals/{issn}/works"
    articles = []
    cursor = "*"
    
    while True:
        try:
            params = {
                'filter': f'from-pub-date:{from_year},until-pub-date:{to_year}',
                'rows': 100,
                'cursor': cursor,
                'select': 'DOI,title,author,published,abstract,volume,issue,type'
            }
            
            response = requests.get(
                base_url,
                params=params,
                headers={'User-Agent': 'ResearchBot/1.0'},
                timeout=30
            )
            
            if response.status_code != 200:
                break
            
            data = response.json()
            
            if 'message' not in data or 'items' not in data['message']:
                break
            
            items = data['message']['items']
            if not items:
                break
            

            for item in items:
                authors = []
                institutions = []
                
                if 'author' in item:
                    for author in item['author']:
                        # Get author name
                        if 'given' in author and 'family' in author:
                            authors.append(f"{author['given']} {author['family']}")
                        elif 'family' in author:
                            authors.append(author['family'])
                        
                        if 'affiliation' in author:
                            for aff in author['affiliation']:
                                if 'name' in aff:
                                    institutions.append(aff['name'])
                

                title = ''
                if 'title' in item and item['title']:
                    title = item['title'][0] if isinstance(item['title'], list) else item['title']
                
                year = ''
                if 'published' in item:
                    pub_date = item['published']
                    if 'date-parts' in pub_date and pub_date['date-parts']:
                        year = str(pub_date['date-parts'][0][0])
                
                abstract = item.get('abstract', '')
                
                articles.append({
                    'tier': tier,
                    'journal': journal_name,
                    'title': title,
                    'authors': '; '.join(authors),
                    'institutions': '; '.join(set(institutions)),
                    'year': year,
                    'volume': item.get('volume', ''),
                    'issue': item.get('issue', ''),
                    'abstract': abstract,
                })
            
            if 'next-cursor' in data['message']:
                cursor = data['message']['next-cursor']
            else:
                break
            
            time.sleep(1)  # Be nice to the API
            
        except Exception as e:
            print(f"Error: {e}")

            break
    
    return articles

def main():
    """Create a CSV file containing all the inflormatio"""    
    all_articles = []
    
    for tier, journals in JOURNALS.items():
        for journal_name, issn in journals.items():
            print(f"Downloading {journal_name}...")
            
            articles = download_journal(journal_name, issn, tier, 2005, 2025)
            all_articles.extend(articles)
            
            print(f"  Got {len(articles)} articles")
            time.sleep(2)
    
    df = pd.DataFrame(all_articles)
    output_file = 'raw_data.csv'
    
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nSaved {len(df)} articles to {output_file}")

if __name__ == "__main__":
    main()
