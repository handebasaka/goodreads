# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read the data
books = pd.read_csv('./data/goodreads_library_export.csv')

# Check NaNs and data types
books.info()

# Review data
print(books.sample(5))

# Change data types if needed
books['Date Read'] = pd.to_datetime(books['Date Read'])
books['Date Added'] = pd.to_datetime(books['Date Added'])

# Enter null in My Rating column instead of 0 to avoid giving incorrect information
books['My Rating'].replace(0, 'null', inplace= True)
books['My Rating'] = books['My Rating'].replace('null', np.nan).astype('Int64')

# Filter the read books only (there may be to-read books still unread)
books = books[books['Read Count'] == 1]

# region My Yearly Reading Journey
# Extract the year from date
books['Year Read'] = books['Date Read'].dt.year.astype('Int64')

# I need this filter because of no regular data before 2019
yearly_books = books[books['Year Read'] > 2018].groupby('Year Read')['Book Id'].count().reset_index(name= 'Counts')

# Visualizing yearly readings
# Set the theme and size of the plot
plt.figure(figsize=(8,6))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create the plot, change the title
ax = sns.barplot(data= yearly_books, x= 'Year Read', y= 'Counts')
plt.title('My Yearly Reading Journey', fontsize= 16)

# Change labels and their settings
plt.xlabel('Year', fontsize= 12)
plt.xticks(fontsize= 12)
plt.ylabel('Number of Books', fontsize= 12)
plt.yticks(fontsize= 12)

# Add a text annotation explaining the filter
plt.text(x= 1.3, y= 50, s= 'Since no regular records existed before 2019,\nthis graph shows the period after 2019.', fontsize= 10, ha= 'center',
        bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))

# Loop through containers and add annotations
for container in ax.containers:
    ax.bar_label(container, fontsize= 13, color= 'dimgray', label_type= 'edge')

# Show the plot
plt.show();
# endregion

# region How Generous Am I with My Ratings?
# Count each rating
my_ratings = books.groupby('My Rating')['My Rating'].count().reset_index(name= 'Counts')

# Visualizing distribution of my rating
# Filter rated ones only for better visualization
books_with_rating = books.dropna(subset=['My Rating'])

# Set the theme and size of the plot
plt.figure(figsize=(6,6))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create the plot, change the title
sns.histplot(data= books_with_rating, x= 'My Rating', discrete= True)
plt.title('Distribution of My Ratings', fontsize= 16)

# Change labels and their settings
plt.xlabel('My Ratings', fontsize= 12)
plt.xticks([2, 3, 4, 5], fontsize= 12)

plt.ylabel('Counts', fontsize= 12)
plt.yticks(fontsize= 12)

# Add mean and median for rating
mean_value = np.nanmean(books_with_rating['My Rating'])
median_value = np.median(books_with_rating['My Rating'])
plt.axvline(x= mean_value, color='red', linestyle='--', label=f'Mean: {mean_value:.2f}')
plt.axvline(x= median_value, color='blue', linestyle='-', label=f'Median: {median_value:.2f}')
plt.legend()

# Show the plot
plt.show();
# endregion

# region My 5 Favorite and 5 Least Favorite Books
# Sort and filter the max-rated books
fav_5_books = books_with_rating.sort_values(['My Rating', 'Average Rating'], ascending= [False, False]).loc[:, ['Title', 'Author', 'My Rating', 'Average Rating', 'Number of Pages']].head(5)

# Sort and filter the min-rated books
least_5_books = books_with_rating.sort_values(['My Rating', 'Average Rating'], ascending= [True, True]).loc[:, ['Title', 'Author', 'My Rating', 'Average Rating', 'Number of Pages']].head(5)

# Display them
print(fav_5_books)
print(least_5_books)
# endregion

# region Do My Ratings Align with the Crowd?
# Calculate difference between my ratings and Goodreads' average ratings
books['Diff Average Rating'] = books['My Rating'] - books['Average Rating']

# Count underrated/overrated books
overrated = books[books['Diff Average Rating'] >= 0]['Book Id'].count()
underrated = books[books['Diff Average Rating'] < 0]['Book Id'].count()

# Visualizing my rating vs. average ratings
# Set the theme and size of the plot
plt.figure(figsize=(8,6))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create the plot, change the title
sns.scatterplot(data= books_with_rating, x= 'Average Rating', y= 'My Rating')
plt.title('Do I Overrate or Underrate?', fontsize= 14)

# Change labels and their settings
plt.xlabel('Goodreads Average Ratings', fontsize= 12)
plt.xticks(fontsize= 12)
plt.ylabel('My Ratings', fontsize= 12)
plt.yticks([2.0, 3.0, 4.0, 5.0], fontsize= 12)

# Add y = x reference line
plt.plot([min(books_with_rating['My Rating']), max(books_with_rating['My Rating'])], 
         [min(books_with_rating['My Rating']), max(books_with_rating['My Rating'])], 
         color='red', linestyle='-')

# Add a text annotation explaining underrated/overrated
plt.text(x= 2.6, y= 4.67, s= f"Overrated Zone: I overrated {overrated} books\n compared to Goodreads' average.", fontsize= 10, ha= 'center',
        bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))

plt.text(x= 4.4, y= 2.45, s= f"Underrated Zone: I underrated {underrated}\n books compared to Goodreads' average.", fontsize= 10, ha= 'center',
        bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))

# Show the plot
plt.show();
# endregion

# region How Long Are the Books I Read?
# Visualizing distribution of number of pages
# Set the theme and size of the plot
plt.figure(figsize=(12,8))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create the plot, change the title
sns.histplot(data= books['Number of Pages'])
plt.title('Distribution of Number of Pages', fontsize= 18)

# Change labels and their settings
plt.xlabel('Number of Pages', fontsize= 16)
plt.xticks(fontsize= 16)
plt.ylabel('Counts', fontsize= 16)
plt.yticks(fontsize= 16)

# Show the plot
plt.show();
# endregion

# region What were the shortest and longest books I've ever read?
# Finding the shortest and longest book I've read
shortest_book = books[books['Number of Pages'] == books['Number of Pages'].min()]['Title'].values[0]
shortest_page = round(books[books['Number of Pages'] == books['Number of Pages'].min()]['Number of Pages'].values[0])

longest_book = books[books['Number of Pages'] == books['Number of Pages'].max()]['Title'].values[0]
longest_page = round(books[books['Number of Pages'] == books['Number of Pages'].max()]['Number of Pages'].values[0])

print(f"The shortest book you've read is '{shortest_book}' with {shortest_page} pages.")
print(f"The longest book you've read is '{longest_book}' with {longest_page} pages.")
# endregion

# region Who Are My Most-Read Authors?
# Filter top N authors
n = 15
author_top_n = books.groupby('Author')['Book Id'].count().reset_index(name= 'Counts').sort_values('Counts', ascending= False).head(n)

# Visualizing top N authors
# Set the theme and size of the plot
plt.figure(figsize=(8,6))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create the plot, change the title
sns.barplot(data= author_top_n, x= 'Counts', y= 'Author')
plt.title(f'My Most-Read Authors - Top {n}', fontsize= 16)

# Change labels and their settings
plt.xlabel('Number of Books', fontsize= 12)
plt.xticks(fontsize= 12)
plt.ylabel('', fontsize= 12)
plt.yticks(fontsize= 12)

# Show the plot
plt.show();
# endregion

# region Gender Distribution of the Authors
# Find percentages of gender
author_gender = books['Author Gender'].value_counts(normalize= True).reset_index(name= 'Percentage')

# Visualizing gender distribution of authors
# Create the plot, change the title
plt.pie(x= author_gender['Percentage'], labels= author_gender['Author Gender'], colors= ['darkgray', 'darkorange'], autopct='%1.1f%%')
plt.title('Gender Distribution of the Authors', fontsize= 14)

# Show the plot
plt.show();
# endregion

# region Top 10 Publishers on My Shelf
# Filter top 10 publishers
publisher_top_10 = books.groupby('Publisher')['Book Id'].count().reset_index(name= 'Counts').sort_values('Counts', ascending= False).head(10)

# Visualizing top 10 publishers
# Set the theme and size of the plot
plt.figure(figsize=(8,6))
sns.set_theme(style= 'darkgrid', palette='Set2')

# Create the plot, change the title
sns.barplot(data= publisher_top_10, x= 'Counts', y= 'Publisher')
plt.title('Top 10 Publishers on My Shelf', fontsize= 16)

# Change labels and their settings
plt.xlabel('Number of Books', fontsize= 12)
plt.xticks(fontsize= 12)
plt.ylabel('', fontsize= 12)
plt.yticks(fontsize= 12)

# Show the plot
plt.show();
# endregion

# region What Book Formats Do I Really Love?
# Visualizing top 10 publishers
# Set the theme and size of the plot
plt.figure(figsize=(6,4))
sns.set_theme(style= 'dark', palette='Set2')

# Create the plot, change the title
ax = sns.countplot(data= books, y= 'Binding', hue= 'Binding', width= 0.4)
plt.title('What Book Formats Do I Really Love?', fontsize= 16)

# Loop through containers and add annotations
for container in ax.containers:
    ax.bar_label(container, fontsize= 13, color= 'black', label_type= 'center')

# Change labels and their settings
plt.xlabel('Number of Books', fontsize= 12)
ax.set(xticklabels=[])
plt.ylabel('', fontsize= 12)
plt.yticks(fontsize= 12)

# Show the plot
plt.show();
# endregion