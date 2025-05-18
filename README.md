# Netflix Dataset Analyis

## Data Sources

Main dataset: [shivamb/netflix-shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

Other datasets:

- [shivamb/amazon-prime-movies-and-tv-shows](https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows)

- [shivamb/disney-movies-and-tv-shows](https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows)

Notes:

- The analysis project is Netflix-centric, as expected by the requirement.
- The other datasets serves the purpose of horizontal comparison purposes.

## Development Environment Setup

**Python version**: `3.12`

**Required Packages**: [requirements.txt](requirements.txt) (I tried to use the latest versions whereever possible)

**Virtual Environment**: I chose `conda`. Feel free to use `pyenv`, `venv`, `vitualenv` etc.

**OS**: The code should work for windows and mac, it's running fine on my windows machine.

**IDE**: VS Code or PyCharm are recommended if you would like to nevigate the code better, but not essential. I used VS Code to do this analysis challenge.

## Runing The Code

==================================================

First, we need to do the following:

- Download the zip files from the Kaggle datasets

- Extract the CSV file from each of the zip file

- Merge the data and produce a mulip-platform dataset

- Enrich the dataset with useful features

- Normalise the data from the one-to-many relationships, including:

    - The co-directors
    
    - The casts

    - The producer countries

    - The categories of the listing (e.g. Comedy etc.)

To run the data prep step for yourself, please run:

```bash
# make sure you are in the right virtual environment
# make sure you have run "pip install -r requirements.txt" at this point

# DISCLAIMER - the python file was developed with the assistance of Github Copilot and ChatGPT

python3 step_01_prepare_data.py
```

After running the script you will see files created in the following paths:

- `data/downloaded` - the zip files

- `data/extracted` - the csv files

- `data/enriched` - the merged and enriched dataset

- `data/normalised` - the normalised "table"s for all the one-to-many relationships

==================================================

After step 1, we can open the Jupyter notebook: [step_02_adhoc_analysis.ipynb](step_02_adhoc_analysis.ipynb) .

The notebook includes most of the data explore analysis I have done. 

Please note that I have included **interactive components** to the charts as I saw fit. 

If you open the jupyter notebook by yourself, you can play with those interactive elements.

## Data Exploration Approach

Over my past exprience I have come up with the following framework for open-ended data explore analysis:

- Find available financial indicators, like revenue, cost etc. Can't find any from Nexflix dataset.

- Find number of sales etc. For Netflix it means subscription events, the dataset doesn't provide that.

- Find user activity related information. For Netflix it means number of views for each Movie or TV Show. The dataset doesn't provide that.

- Now it's time to see the products. ***We do have that in the Netflix dataset***, so we will focus on that for this data explore analysis.

## Key Insights

All the below key insights are solely based on the dataset, and for the purpose of this exercise we **assume that the data is complete and accurate**.

### Key Insight - Volume Analysis / Market Share Analysis

![volumn-analysis-overall](/images/total-listings-over-time-multi-platform.png)

### Key Insight - Amazon Prime Dataset Data Quality Analysis

Since Amazon Prime has the most listings, I was curious on the volumes each alendar year. analysis.

```
   added_year     type  total_listings
0         NaN    Movie            7798
1         NaN  TV Show            1715
2      2021.0    Movie              16
3      2021.0  TV Show             139
```

But I found that lots of the `date_added` values are `null` in the original dataset, which makes analysis less insightful. 

Luckily we have relatively good data quality for Netflix for year-on-year analysis.

### Key Insight - Netflix Lists More Movies Than TV Shows

This is very obvious through the chart. 

Although usually TV Shows contain 8 to 10 episodes, movies and tv shows individually attract viewers, so this is still meaningful, as a show as a produce attracts viewers, not episodes.

### Key Insight - Netflix Focuses On Recreational Contents The Most

Again this is shown from the chart. 

The top categories for each year are consistently Drama, Comedy, Action, Romance etc. This is consistent throughout the years. Presumably they do a good job attracting viewers. 

### Key Insight - Netflix Predominant Producer Countries

For movies, Netflix enlists movies produced mainly from the US and India. (Holywood and Bollywood).

For tv shows, Netflix enlists series mainly from the US and the UK. (Black Mirror!!!)

### Key Insight - Netflix Movie Length vs Disney Plus

Netflix has an average movie length of around 2 hours, in comparison to Disney's 70 minutes length. 

Natrually Disney is more catering towards children and won't have the same length in comparison to Netflix, whose focus are mainly adults.

### Key Insight - Netflix TV Show Seasons

Among the tv shows from the datasets, most of the TV shows have 2 seaosons, then 3 seasons. Only around 30% of the shows already have more than 3 seasons.

### Key Insight - Directors And Casts

According to the data, Netflix work with a variety of directors and casts, each year the highest producing directors and casts vary, assuming the completeness of this dataset, it indicates that Netflix focuses more on listing attractive contents than working with particular directors or casts.

### Key Insights - Common Keywords For Movies Of Different Categories

We have found some consistently common keywords in a few movie categories, using the description in the dataset.

For example, "family", "friend", "young", "life" are the most commonly appearing word in the description of Dramas and Comedies. This shows that those are the most commonly discussed topics in those categories of movies.
