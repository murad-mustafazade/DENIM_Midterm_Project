import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ----------------------------------------
# Load cleaned data
# ----------------------------------------
df = pd.read_csv("cleaned_data.csv", low_memory=False)

# Convert 'year' to numeric and drop missing
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df = df.dropna(subset=['year'])
df['year'] = df['year'].astype(int)

# ----------------------------------------
# Articles over time by journal
# ----------------------------------------
plt.figure(figsize=(10, 5))
df.groupby(['year', 'journal']).size().unstack().plot(ax=plt.gca())
plt.title("Number of Articles Over Time by Journal")
plt.xlabel("Year")
plt.ylabel("Articles")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# ----------------------------------------
# Plotting functions by tier
# ----------------------------------------
def plot_top5(df):
    tier_df = df[df['tier'] == 'Top 5']
    plt.figure(figsize=(10, 5))
    tier_df.groupby(['year', 'journal']).size().unstack().plot(ax=plt.gca())
    plt.title("Number of Articles Over Time — Top 5 Journals")
    plt.xlabel("Year")
    plt.ylabel("Articles")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_top_field(df):
    tier_df = df[df['tier'] == 'Top Field Journals']
    plt.figure(figsize=(10, 5))
    tier_df.groupby(['year', 'journal']).size().unstack().plot(ax=plt.gca())
    plt.title("Number of Articles Over Time — Field Specific Journals")
    plt.xlabel("Year")
    plt.ylabel("Articles")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_mid_tier(df):
    tier_df = df[df['tier'] == 'Mid-Tier']
    plt.figure(figsize=(10, 5))
    tier_df.groupby(['year', 'journal']).size().unstack().plot(ax=plt.gca())
    plt.title("Number of Articles Over Time — Mid-Tier Journals")
    plt.xlabel("Year")
    plt.ylabel("Articles")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_lower_tier(df):
    tier_df = df[df['tier'] == 'Lower-Tier & Regional']
    plt.figure(figsize=(10, 5))
    tier_df.groupby(['year', 'journal']).size().unstack().plot(ax=plt.gca())
    plt.title("Number of Articles Over Time — Lower-Tier & Regional Journals")
    plt.xlabel("Year")
    plt.ylabel("Articles")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_all_tiers_summary(df):
    plt.figure(figsize=(8, 5))
    df.groupby(['year', 'tier']).size().unstack().plot(ax=plt.gca())
    plt.title("Number of Articles Over Time — All Tiers Summary")
    plt.xlabel("Year")
    plt.ylabel("Articles")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

# ----------------------------------------
# Run plots
# ----------------------------------------
plot_top5(df)
plot_top_field(df)
plot_mid_tier(df)
plot_lower_tier(df)
plot_all_tiers_summary(df)

# ----------------------------------------
# Expand multi-country entries
# ----------------------------------------
df_expanded = df.copy()
df_expanded['countries_list'] = (
    df_expanded['countries']
    .fillna('')
    .apply(lambda x: [c.strip() for c in x.split(';') if c.strip()])
)

# Explode so each country gets its own row
df_exploded = df_expanded.explode('countries_list')
df_exploded = df_exploded[df_exploded['countries_list'] != '']

# ----------------------------------------
# Country stacked bar chart by tier
# ----------------------------------------
# ----------------------------------------
# Country stacked bar chart by tier (only countries with >300 articles)
# ----------------------------------------
country_tier = df_exploded.groupby(['countries_list', 'tier']).size().unstack(fill_value=0)

# Filter countries with more than 300 total articles
country_tier = country_tier[country_tier.sum(axis=1) > 300]

plt.figure(figsize=(10, 6))
country_tier.plot(kind='bar', stacked=True, ax=plt.gca())
plt.title("Country Split by Journal Tier (Countries with >300 Articles)")
plt.xlabel("Country")
plt.ylabel("Articles")
plt.tight_layout()
plt.show()


# ----------------------------------------
# Pie charts: Tier distribution for selected countries
# ----------------------------------------
selected_countries = ['USA', 'China', 'Canada', 'United Kingdom', 'Germany', 'France']

# Define uniform colors for tiers
tier_colors = {
    'Top 5': '#1f77b4',               # Blue
    'Top Field Journals': '#ff7f0e',  # Orange
    'Mid-Tier': '#2ca02c',            # Green
    'Lower-Tier & Regional': '#d62728' # Red
}

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

for i, country in enumerate(selected_countries):
    subset = df_exploded[df_exploded['countries_list'] == country]
    tier_counts = subset['tier'].value_counts()

    # Keep only tiers present in tier_colors, in correct order
    counts = [tier_counts.get(tier, 0) for tier in tier_colors.keys()]
    colors = [tier_colors[tier] for tier in tier_colors.keys()]

    axes[i].pie(
        counts,
        labels=None,
        colors=colors,
        startangle=140,
        autopct='%1.1f%%'
    )
    axes[i].set_title(country)

# Add legend on the right
handles = [
    plt.Line2D([0], [0], marker='o', color='w', label=tier,
               markerfacecolor=color, markersize=15)
    for tier, color in tier_colors.items()
]
fig.legend(handles=handles, loc='center right', title="Journal Tier")

plt.suptitle("Tier Distribution by Country", fontsize=16)
plt.tight_layout(rect=[0, 0, 0.85, 0.95])
plt.show()

# ----------------------------------------
# Share of each journal tier over time for China
# ----------------------------------------

# Filter only China's papers
china_df = df_exploded[df_exploded['countries_list'] == 'China']

# Group by year and tier
china_tier_year = china_df.groupby(['year', 'tier']).size().unstack(fill_value=0)

# Convert counts to shares (row-wise)
china_tier_share = china_tier_year.div(china_tier_year.sum(axis=1), axis=0)

# Plot
plt.figure(figsize=(10, 6))
china_tier_share.plot(kind='area', stacked=True, colormap='tab10', alpha=0.85, ax=plt.gca())

plt.title("China: Share of Journal Tiers Over Time")
plt.xlabel("Year")
plt.ylabel("Share of Articles")
plt.legend(title="Journal Tier", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

