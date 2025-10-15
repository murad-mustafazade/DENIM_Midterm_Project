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

- ***subfield***: The article's title and abstract are scanned for keywords to classify it into one of 12 predefined economic subfields.

- ***countries***: The institutions field is parsed to identify the home countries of the authors' affiliations.

- ***has_china_author***: A boolean flag is set to True if any author has an affiliation in China or Hong Kong.
