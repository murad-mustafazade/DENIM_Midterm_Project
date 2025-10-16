# Analysis of Publication Trends in Economics Journals (2005-2025)

## 1. Project Goal

The goal of this project is to collect data on publications and analyze the publication landscape of 30 prominent economics journals over 2005-2025. It is often the case that the majority of articles within published journals are affiliated with American universities/authors. However, there is a common belief that this trend is changing over time. The primary goal of this project is to investigate the representation of authors affiliated with Chinese institutions and to identify how this presence has evolved over time and across different tiers of journal prestige.

The key research questions are:

- **How has the number of publications with foreign-affiliated authors changed in top economics journals since 2005?**

- **Is there a significant difference in the representation of foreign-affiliated authors among journal reputation tiers?**

- **What are the most common economic subfields for articles with foreign-affiliated authors?**

---

##  2. Data Source and Collection
### Data Source
The data source for this project is the **Crossref API**. Crossref is a non-profit organization that does not require an API key or authentification. Crossref maintains a massive, public database of scholarly publication metadata. This data is supplied directly by the publishers, ensuring it is a reliable and authoritative source for bibliographic information.

### Data Collection Method

The data collection process was the following:

1.  **Journal Identification:** Each of the 30 target journals is identified by its unique International Standard Serial Number (ISSN).

2.  **API Querying:** The script sends HTTP GET requests to the Crossref API endpoint for each journal.

3.  **Filtering and Pagination:** Each request is filtered to retrieve articles published between January 1, 2005, and December 31, 2025. The API returns data in batches, and the script uses a cursor to navigate through all pages until the complete publication history is downloaded.

4.  **Data Extraction and Cleaning:** For each article, the script parses the raw JSON response to extract key metadata and performs cleaning operations, such as removing HTML tags from abstracts.

5.  **Feature Engineering:** We created several new columns to help facilitate the analysis:
    * `subfield`: The article's title and abstract are scanned for an extensive dictionary of keywords to classify it into one of 18 predefined economic subfields. 
    * `countries`: We created an extensive dictionary of words most seen in the `institutions` column to assign countries to each article. We then cross-verified the accuracy of this through some manual tests on the CSV. 
    * `has_china_author`: A boolean flag is set to `True` if any author has an affiliation in Mainland China, Hong Kong or Macao.

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
<img width="1000" height="500" alt="Figure_1" src="https://github.com/user-attachments/assets/153e72b2-d0ba-41be-b94f-47282cc4dc9a" />



#### Part 1: Overall Publication Trends by Journal Tier
First, we examine the overall publication volume. The number of articles published per year varies significantly across tiers, with mid-tier journals publishing the highest volume.

**Figure 1: Number of Articles Over Time — All Tiers Summary**
<img width="800" height="500" alt="Figure_6" src="https://github.com/user-attachments/assets/2a83cfb6-906c-483d-8135-2d96432cffce" />




To see the detail behind this summary, the following plots show the trends for each individual journal within the four tiers.

| Journals Grouped by Tier                                                                                                                              |                                                                                                                                                         |
| :----------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                                             **Figure 2: Trends in Top 5 Journals**<br><img alt="Figure_2" src="https://github.com/user-attachments/assets/d0d7165d-157e-4761-8fac-9ff06cd7dbd6">                                             |                                       **Figure 3: Trends in Top Field Journals**<br><img alt="Figure_3" src="https://github.com/user-attachments/assets/ce4a2147-f5e2-4490-ad22-8221a1b4eb70">                                        |
|                                            **Figure 4: Trends in Mid-Tier Journals**<br><img alt="Figure_4" src="https://github.com/user-attachments/assets/f1f44953-479a-4d42-9783-694f617be16b">                                            |                                 **Figure 5: Trends in Lower-Tier & Regional Journals**<br><img alt="Figure_5" src="https://github.com/user-attachments/assets/042a8308-ce86-4643-8d42-1b7791b013ad">                                 |


#### Part 2: Country-Level Publication Analysis

Next, we analyze the geographic distribution of author affiliations. 

**Figure 6: Total Articles per Country, Split by Journal Tier**

This chart shows the total number of articles for each country, stacked by the tier of the journal.
<img width="1000" height="600" alt="Figure_7 (1)" src="https://github.com/user-attachments/assets/f73667ae-8b96-4eb0-b479-cd1f57b91e36" />



While the bar chart shows absolute numbers, it's also useful to see the proportional distribution. The following pie charts show, for the top 6 contributing countries, what percentage of their total output is published in each tier. This reveals different publication patterns; for instance, a higher proportion of US & Canada-affiliated papers are in top-tier journals compared to other countries, while China-affiliated papers are focused on mid-tier journals.

**Figure 7: Tier Distribution for the Top 6 Countries**
<img width="1920" height="967" alt="Figure_8" src="https://github.com/user-attachments/assets/d3feff78-43fc-41b2-bc9e-0f16f5e4b5cb" />

**Figure 8: Share of Journal Tiers in China**
<img width="1920" height="967" alt="Figure_9" src="https://github.com/user-attachments/assets/eff94011-d3cd-4760-a34a-6428e4f5d57a" />


#### Part 3: Subfield Analysis
**Figure 9: Number of Articles in Each Subfield Over Time**
<img width="1200" height="600" alt="Figure_10" src="https://github.com/user-attachments/assets/e1848431-67f8-4028-9cb4-22fc307a6311" />


**Figure 10: Growth in Number of Articles by Subfield (2005-2025)**
<img width="1000" height="600" alt="Figure_11" src="https://github.com/user-attachments/assets/2358bf13-b911-42bb-b8a0-b515ba0c3e63" />

**Figure 11: Country Specialization by Subfield**
<img width="1200" height="800" alt="Figure_12" src="https://github.com/user-attachments/assets/8d8187d6-8f6c-46b4-be11-92296df3a9ed" />


### Limitations of the Analysis

* **Author Origin vs. Affiliation:** This analysis tracks the location of the author's **institution**, not their nationality. An American-born professor working at Peking University would be counted as "China-affiliated."
* **Single Country Affiliation:** The `has_china_author` flag is `True` even if only one of multiple co-authors is based in that country.
* **No Causal Analysis:** The analysis identifies trends and correlations but does not make any causal claims about why these trends are occurring.

---

## 4. Extensions and Future Research

* **Validate Subfield Classification:** The heuristic `subfield` classification could be validated against a subset of articles where author-provided JEL (Journal of Economic Literature) codes are available.
* **Granular Affiliation Analysis:** The dataset could be extended to analyze contributions from specific universities (e.g., Tsinghua University vs. University of Chicago) rather than just countries.
* **International Collaboration Analysis:** The script could be modified to generate a `num_countries` column to analyze trends in international co-authorship over time.
* **Author-Level Tracking:** The analysis could be extended to track the publication records of individual authors to study career trajectories, international mobility, and collaboration patterns.
