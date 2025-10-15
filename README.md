# Analysis of Publication Trends in Economics Journals (2005-2025)

## 1. Project Goal

This project aims to analyze the publication landscape of 30 prominent economics journals over the past two decades (2005-2025). The primary goal is to investigate the representation of authors affiliated with Chinese institutions and to identify how this presence has evolved over time and across different tiers of journal prestige.

The key research questions are:

- **How has the number of publications with China-affiliated authors changed in top economics journals since 2005?**

- **Is there a significant difference in the representation of China-affiliated authors between top-tier, mid-tier, and lower-tier journals?**

- **What are the most common economic subfields for articles with China-affiliated authors?**


##  2. Data Source and Collection
### Data Source
The sole data source for this project is the Crossref API. Crossref is a non-profit organization that maintains a massive, public database of scholarly publication metadata. This data is supplied directly by the publishers, ensuring it is a reliable and authoritative source for bibliographic information.

### Data Collection Method
The data was collected using a custom Python script that programmatically queries the Crossref API. The process is as follows:

#### 1. Journal Identification: Each of the 30 target journals is identified by its unique International Standard Serial Number (ISSN).

#### 2. API Querying: The script sends HTTP GET requests to the Crossref API endpoint for each journal (e.g., https://api.crossref.org/journals/{ISSN}/works).

#### 3. Filtering and Pagination: Each request is filtered to retrieve articles published between January 1, 2005, and December 31, 2025. The API returns data in batches (pages), and the script uses a cursor to navigate through all pages until the complete publication history for the period is downloaded.

#### 4. Data Extraction and Cleaning: For each article, the script parses the raw JSON response to extract key metadata and performs cleaning operations, such as removing HTML tags from abstracts.

#### 5. Feature Engineering: Three new features are generated to facilitate the analysis:

- ***subfield***: The article's title and abstract are scanned for an extensive dictionary of keywords to classify it into one of 18 predefined economic subfields. The classification uses a weighted scoring system (giving more importance to multi-word phrases like "instrumental variable") and intelligent tie-breaking logic to improve accuracy.

- ***countries***: The institutions field is parsed using a comprehensive list of patterns to identify the home countries of authors. This method goes beyond simple country names and recognizes major universities, research institutions (e.g., NBER), central banks, and major cities to significantly enhance matching accuracy.

- ***has_china_author & has_usa_author***: Boolean flags are set to **True** if any author has an affiliation in China/Hong Kong or the USA, respectively.
- ***num_countries***: A count of the unique countries identified for each article, used to gauge international collaboration.
- ***no_country_identified***: A boolean flag to easily filter for articles where affiliation data was missing or unidentifiable.

### Data Dictionary
The final dataset (cleaned_data.csv) is organized with the following columns:
| Column                  | Description                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------- |
| `tier`                  | The prestige category of the journal (e.g., 'Top 5', 'Mid-Tier').                                       |
| `journal`               | The name of the journal.                                                                                |
| `year`                  | The publication year of the article.                                                                    |
| `title`                 | The title of the article.                                                                               |
| `authors`               | A semicolon-separated list of the article's authors.                                                    |
| `institutions`          | A semicolon-separated list of unique author affiliations.                                               |
| `abstract`              | The abstract of the article (if available).                                                             |
| `volume`                | The journal volume number.                                                                              |
| `issue`                 | The journal issue number.                                                                               |
| `subfield`              | The classified economic subfield (e.g., 'Labor Economics', 'Political Economy').                        |
| `countries`             | A semicolon-separated list of unique author countries, derived from affiliations.                       |
| `num_countries`         | The number of unique countries identified from author affiliations.                                     |
| `has_china_author`      | A boolean (`True`/`False`) indicating if any author is affiliated with an institution in China/Hong Kong. |
| `has_usa_author`        | A boolean (`True`/`False`) indicating if any author is affiliated with an institution in the USA.         |
| `no_country_identified` | A boolean (`True`/`False`) indicating if no country could be identified from the affiliation data.        |

### Limitations of the Data

The primary limitation of this dataset is its reliance on the completeness of the Crossref database.

- **Missing Abstracts**: A significant portion of abstracts, especially for articles published before ~2010, are not available. This directly impacts the accuracy of the subfield classification.

- **Incomplete Affiliations**: While the new country identification method is far more robust, its accuracy is still constrained by the quality of the affiliation data provided by publishers.

- **Keyword Classification Errors**: The subfield classification, while significantly improved, is still a heuristic method and may not capture the nuance of every paper perfectly, especially for interdisciplinary work.
