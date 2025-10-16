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


### Visualizations

#### Part 0: All Journals Over Time

For a complete but less readable overview, the following chart plots the publication volume for all 30 journals on a single set of axes.

**Figure 0: All Articles by Journal Over Time**
<img width="1000" height="500" alt="All articles by journals over time" src="https://github.com/user-attachments/assets/f89a6261-628b-447f-8905-4cbbd9acaeaa" />


#### Part 1: Overall Publication Trends by Journal Tier
First, we examine the overall publication volume. The number of articles published per year varies significantly across tiers, with mid-tier journals publishing the highest volume.

**Figure 1: Number of Articles Over Time — All Tiers Summary**
<img width="800" height="500" alt="Number of articles over time- Tier Summary" src="https://github.com/user-attachments/assets/9b56f98d-90b1-45d1-a7f5-ee4d9f684c9e" />



To see the detail behind this summary, the following plots show the trends for each individual journal within the four tiers.

**Figure 2: Trends in Top 5 Journals**
<img width="1000" height="500" alt="Number of articles over time- Top 5 journals" src="https://github.com/user-attachments/assets/35a8a716-9e5f-4cb7-8bae-08b6c863ba11" />


**Figure 3: Trends in Field Specific Journals**
<img width="1000" height="500" alt="Number of articles over time- Field Specific Journals" src="https://github.com/user-attachments/assets/d27a46a7-faaf-41b2-86d6-6398d3b828a7" />


**Figure 4: Trends in Mid-Tier Journals**
<img width="1000" height="500" alt="Number of articles over time- Mid Tier Journals" src="https://github.com/user-attachments/assets/e7c43568-ee20-4100-89a0-4fac838a4039" />


**Figure 5: Trends in Lower-Tier & Regional Journals**
<img width="1000" height="500" alt="Number of articles over time- Low tier Journals" src="https://github.com/user-attachments/assets/5db4f1bf-d99c-4be7-8919-750dc4749381" />

#### Part 2: Country-Level Publication Analysis

Next, we analyze the geographic distribution of author affiliations. 

**Figure 6: Total Articles per Country, Split by Journal Tier**

This chart shows the total number of articles for each country, stacked by the tier of the journal.
<img width="1000" height="600" alt="Number of articles per country by tier" src="https://github.com/user-attachments/assets/1bfe5c56-e39e-479c-899f-670366835ae8" />


While the bar chart shows absolute numbers, it's also useful to see the proportional distribution. The following pie charts show, for the top 6 contributing countries, what percentage of their total output is published in each tier. This reveals different publication patterns; for instance, a higher proportion of US & Canada-affiliated papers are in top-tier journals compared to other countries, while China-affiliated papers are focused on mid-tier journals.

**Figure 7: Tier Distribution for the Top 6 Countries**
<img width="1280" height="692" alt="Tier distribution of top 6 countries" src="https://github.com/user-attachments/assets/96844ce7-e2f4-402c-b540-be69f4aa83ba" />

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
