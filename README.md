# Analysis of Publication Trends in Economics Journals (2005-2025)

## 1. Project Goal

This project aims to analyze the publication landscape of 30 prominent economics journals over the past two decades (2005-2025). It is often the case that the majority of articles within published journals are affiliated with American universities/authors. However, there is a common belief that this trend is changing over time. The primary goal of this project is to investigate the representation of authors affiliated with Chinese institutions and to identify how this presence has evolved over time and across different tiers of journal prestige.

The key research questions are:

- **How has the number of publications with foreign-affiliated authors changed in top economics journals since 2005?**

- **Is there a significant difference in the representation of foreign-affiliated authors between top-tier, mid-tier, lower-tier and field-specific journals?**

- **What are the most common economic subfields for articles with foreign-affiliated authors?**

---

##  2. Data Source and Collection
### Data Source
The sole data source for this project is the **Crossref API**. Crossref is a non-profit organization that doesn't require an API key or authentification. Crossref maintains a massive, public database of scholarly publication metadata. This data is supplied directly by the publishers, ensuring it is a reliable and authoritative source for bibliographic information.

### Data Collection Method

The data was collected using a custom Python script that programmatically queries the Crossref API. The process is as follows:

1.  **Journal Identification:** Each of the 30 target journals is identified by its unique International Standard Serial Number (ISSN).

2.  **API Querying:** The script sends HTTP GET requests to the Crossref API endpoint for each journal.

3.  **Filtering and Pagination:** Each request is filtered to retrieve articles published between January 1, 2005, and December 31, 2025. The API returns data in batches, and the script uses a cursor to navigate through all pages until the complete publication history is downloaded.

4.  **Data Extraction and Cleaning:** For each article, the script parses the raw JSON response to extract key metadata and performs cleaning operations, such as removing HTML tags from abstracts.

5.  **Feature Engineering:** Several new features are generated using advanced heuristics to facilitate the analysis:
    * `subfield`: The article's title and abstract are scanned for an extensive dictionary of keywords to classify it into one of 18 predefined economic subfields. The classification uses a **weighted scoring system** (giving more importance to multi-word phrases like "instrumental variable") and intelligent tie-breaking logic to improve accuracy.
    * `countries`: The `institutions` field is parsed using a comprehensive list of patterns to identify the home countries of authors. This method goes beyond simple country names and recognizes **major universities, research institutions (e.g., NBER), central banks, and major cities** to significantly enhance matching accuracy.
    * `has_china_author`: A boolean flag is set to `True` if any author has an affiliation in China or Hong Kong.

### Data Dictionary
The final dataset (cleaned_data.csv) is organized with the following columns:
| Column             | Description                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------- |
| `tier`             | The prestige category of the journal (e.g., 'Top 5', 'Mid-Tier').                                       |
| `journal`          | The name of the journal.                                                                                |
| `year`             | The publication year of the article.                                                                    |
| `title`            | The title of the article.                                                                               |
| `authors`          | A semicolon-separated list of the article's authors.                                                    |
| `institutions`     | A semicolon-separated list of unique author affiliations.                                               |
| `abstract`         | The abstract of the article (if available).                                                             |
| `volume`           | The journal volume number.                                                                              |
| `issue`            | The journal issue number.                                                                               |
| `subfield`         | The classified economic subfield (e.g., 'Labor Economics', 'Political Economy').                        |
| `countries`        | A semicolon-separated list of unique author countries, derived from affiliations.                       |
| `has_china_author` | A boolean (`True`/`False`) indicating if any author is affiliated with an institution in China/Hong Kong. |

### Limitations of the Data

> **Note:** The primary limitation of this dataset is its reliance on the completeness of the Crossref database.

* **Missing Abstracts:** A significant portion of abstracts, especially for articles published before ~2010, are not available. This directly impacts the accuracy of the `subfield` classification.
* **Incomplete Affiliations:** While the new country identification method is far more robust, its accuracy is still constrained by the quality of the affiliation data provided by publishers. For instance, certain articles do not provide enough institution information to deduct country information from that column.
* **Keyword Classification Errors:** The subfield classification, while significantly improved, is still a heuristic method and may not capture the nuance of every paper perfectly, especially for interdisciplinary work.

---

## 3. Analysis and Findings
### Methodology
The analysis is conducted using the pandas library in Python. It involves grouping, aggregating, and counting the data to answer the core research questions. Proportions and percentages are calculated to compare trends across different groups (tiers, years, countries). The findings are visualized using Matplotlib to create line charts, pie charts, and stacked bar charts.

### Project Findings

### Visualizations

### Limitations of the Analysis

* **Author Origin vs. Affiliation:** This analysis tracks the location of the author's **institution**, not their nationality. An American-born professor working at Peking University would be counted as "China-affiliated."
* **Single Country Affiliation:** The `has_china_author` flag is `True` even if only one of multiple co-authors is based in that country.
* **No Causal Claims:** The analysis identifies trends and correlations but does not make any causal claims about why these trends are occurring.

---

## 4. Extensions and Future Research

* **Validate Subfield Classification:** The heuristic `subfield` classification could be validated against a subset of articles where author-provided JEL (Journal of Economic Literature) codes are available.
* **Granular Affiliation Analysis:** The dataset could be extended to analyze contributions from specific universities (e.g., Tsinghua University vs. University of Chicago) rather than just countries.
* **International Collaboration Analysis:** The script could be modified to generate a `num_countries` column to analyze trends in international co-authorship over time.
* **Author-Level Tracking:** The analysis could be extended to track the publication records of individual authors to study career trajectories, international mobility, and collaboration patterns.
