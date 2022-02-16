# -*- coding: utf-8 -*-
"""NLP_Reco.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ajq5UBkfxhX9x5OESbHb_aOnlEhscsl4

# This is the Capstone project performing sentimental analysis on Product Reviews and then suggesting a recommender system.
"""

from google.colab import drive
drive.mount('/content/drive')

"""### Importing libraries"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

"""### Import csv file"""

df = pd.read_csv('/content/drive/My Drive/NLP_Reco/sample30.csv')
print(df.shape)
df.head()

df.info()

df.describe()

"""### Plot the distribution of review ratings

"""

plt.figure(figsize = (8 ,8))
sns.set(style = 'darkgrid')
ax = sns.countplot(x = df['reviews_rating'],
                   data = df)

percent_val = 100 * df['user_sentiment'].value_counts()/len(df)
percent_val.plot.bar()
plt.show()

"""### Looking at the bar plots, we find that most users have rated the products as "5" and "Positive"

### Data exploratory analysis.
"""

df['categories'] = df['categories'].apply(lambda x: x.split(',')[0])
df['categories'].unique()

df['categories'].value_counts()

"""### Based on the above, we find that the most reviews categories are Household essentials, Movies and Personal care

##Data Visualization
"""

# Most purchased categories
plt.figure(figsize = (15, 10))
ax = sns.countplot(y = df['categories'],
                   data  = df,
                   color = 'green',
                   order = df['categories'].value_counts().index)
ax.set_title('Categories - Reviews Counts')
for p in ax.patches:
    width = p.get_width()
    plt.text(10+p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.2f}'.format(width),
             ha='center', va='center')

"""### We perform some Descriptive Statistics of ratings by considering the average ratings"""

df2 = df.groupby(['categories'])['reviews_rating'].agg(['mean']).reset_index()
df2.head()

df = df.merge(df2,
              on = 'categories',
              how = 'left')
print(df.shape)
df.head()

df2 = df.groupby(['brand'])['reviews_rating'].agg(['mean']).reset_index()
df2.head()

df = df.merge(df2,
              on = 'brand',
              how = 'left')
df.head()

df = df.rename(columns = {'mean_x': 'cat_avg_rating',
                          'mean_y': 'brand_avg_rating'})
df.head()

df2 = df.groupby(['categories'])['categories'].agg(['count']).reset_index()
df2.head()

df = df.merge(df2,
              on = 'categories',
              how = 'left')
df.head()

df2 = df.groupby(['brand'])['brand'].agg(['count']).reset_index()
df2.head()

df = df.merge(df2,
              on = 'brand',
              how = 'left')
df.head()

df = df.rename(columns = {'count_x': 'cat_count',
                          'count_y': 'brand_count'})
df.head()

df['categories'].value_counts()

"""### Setting the cut-off to 10 review counts for categories and retaining those categories

"""

df_2 = df[df['cat_count'] > 10]
df_2['categories'].value_counts()
df_2['cat_avg_rating'].unique()

"""### Visualizing the numbers"""

plt.figure(figsize = (12, 6))
ax = sns.barplot(x = df_2['cat_avg_rating'],
                 y = df_2['categories'],
                 data  = df_2,
                 order = df_2['categories'].value_counts().index,
                 color = 'green')
ax.set_title('Most Reviewed Categories - Average Rating')
for p in ax.patches:
    width = p.get_width()
    plt.text(0.1+p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.2f}'.format(width),
             ha='center', va='center')

"""### Featured brand has the highest average review ratings at 4.91 while Personal care has the lowest average reivew ratings at 3.86 among the selected categories."""

df['brand'].value_counts()

"""### As few brands have low numbers of reviews. Lets set the cutoff value at 100 review counts."""

df_3 = df[df['brand_count'] > 100]
df_3['brand'].value_counts()

#fixme df_3.loc[df_3['brand'] == "L'oreal Paris", 'brand'] = "L'Oreal Paris"

plt.figure(figsize = (12, 6))
ax = sns.barplot(x = df_3['brand_avg_rating'],
                 y = df_3['brand'],
                 data  = df_3,
                 order = df_3['brand'].value_counts().index,
                 color = 'green')
ax.set_title('Most Reviewed Brands - Average Rating')
for p in ax.patches:
    width = p.get_width()
    plt.text(0.1+p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.2f}'.format(width),
             ha='center', va='center')

"""### Avery has the the highest average review rating

### Now lets see which category and brand have the highest number of 5-star ratings.
"""

df.loc[df['reviews_rating'] == 5, 'categories'].value_counts()

plt.figure(figsize = (12, 10))
ax = sns.countplot(y = df.loc[df['reviews_rating'] == 5, 'categories'],
                   data = df,
                   order = df.loc[df['reviews_rating'] == 5, 'categories'].value_counts().index,
                   color = 'green')
ax.set_title('Categories with the Most 5-Star Rating')
for p in ax.patches:
    width = p.get_width()
    plt.text(0.1+p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.2f}'.format(width),
             ha='center', va='center')

"""### Household Essentials has the highest number of 5 star ratings"""

df_3.loc[df_3['reviews_rating'] == 5, 'brand'].value_counts()

plt.figure(figsize = (12, 6))
ax = sns.countplot(y = df_3.loc[df_3['reviews_rating'] == 5, 'brand'],
                   data = df_3,
                   order = df_3.loc[df_3['reviews_rating'] == 5, 'brand'].value_counts().index,
                   color = 'green')
ax.set_title('Brands with Maximum 5-Star Rating')
for p in ax.patches:
    width = p.get_width()
    plt.text(1+p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.2f}'.format(width),
             ha='center', va='center')

"""### Clorox has highest customer base and product quality

### Precition of review rating using Natural Language processing
"""

from collections import Counter
from nltk.tokenize import RegexpTokenizer
import nltk
from nltk.corpus import stopwords
from nltk import sent_tokenize, word_tokenize
from wordcloud import WordCloud, STOPWORDS
import re
nltk.download('stopwords')
stop_words = stopwords.words('english')

"""### Let's only keep the transactions that have review texts."""

df = df.loc[df['reviews_text'].isnull() == False]
df.shape

def wc(data, bgcolor, title):
    fig = plt.figure(figsize = (8, 5), dpi = 80)
    wc = WordCloud(background_color = bgcolor,
                   max_words = 1000,
                   max_font_size = 50)
    wc.generate(' '.join(data))
    fig.suptitle(title, fontsize = 16)
    fig.subplots_adjust(top=1)
    plt.imshow(wc)
    plt.axis('off')

"""### This is to strength our dictionary of stopwords"""

stopwords_json = {"en":["a","a's","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","d","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","e","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","j","just","k","keep","keeps","kept","know","known","knows","l","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via","viz","vs","w","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","wouldn't","x","y","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","z","zero"]}

def word_freq(df):

    top_N = 100

    a = df.str.lower().str.cat(sep=' ')

    b = re.sub('[^A-Za-z]+', ' ', a)

    nltk_words = list(stopwords.words('english'))
    stopwords_json_en = list(stopwords_json['en'])
    stop_words.extend(nltk_words)
    stop_words.extend(stopwords_json_en)

    word_tokens = word_tokenize(b)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    without_single_chr = [word for word in filtered_sentence if len(word) > 2]

    cleaned_data_title = [word for word in without_single_chr if not word.isnumeric()]

    word_dist = nltk.FreqDist(cleaned_data_title)
    rslt = pd.DataFrame(word_dist.most_common(top_N),
                        columns = ['Word', 'Frequency'])

    plt.figure(figsize = (10, 10))
    ax = sns.barplot(x = "Frequency",
                     y = "Word",
                     data = rslt.head(10),
                     palette = sns.color_palette(palette = 'Set2'))

"""### Now we will visualize term frequency for each rating threshold from 1 to 5."""

df_1 = df[df['reviews_rating'] == 1]['reviews_text']
df_2 = df[df['reviews_rating'] == 2]['reviews_text']
df_3 = df[df['reviews_rating'] == 3]['reviews_text']
df_4 = df[df['reviews_rating'] == 4]['reviews_text']
df_5 = df[df['reviews_rating'] == 5]['reviews_text']
df_6=df[df['user_sentiment'] == "Positive"]['reviews_text']
df_7=df[df['user_sentiment'] == "Negative"]['reviews_text']
print(df_1.shape,
      df_2.shape,
      df_3.shape,
      df_4.shape,
      df_5.shape,
      df_6.shape,
      df_7.shape)

nltk.download('punkt')
word_freq(df_1)

wc(df_1, 'black', 'Wordcloud for 1-Star Rating')

word_freq(df_2)
wc(df_2, 'black', 'Wordcloud for 2-Star Rating')

word_freq(df_3)
wc(df_3, 'black', 'Wordcloud for 3-Star Rating')

word_freq(df_4)
wc(df_4, 'black', 'Wordcloud for 4-Star Rating')

word_freq(df_5)
wc(df_5, 'black', 'Wordcloud for 5-Star Rating')

# Word clouds for postive user sentiment
word_freq(df_6)
wc(df_6, 'black', 'Wordcloud for Positive user sentiment')

# Word clouds for Negative user sentiment
word_freq(df_7)
wc(df_7, 'black', 'Wordcloud for Negative user sentiment')

"""### Creation of  TF-IDF vectors for our reviews. We will use Random Forest and XGboost"""

from sklearn.model_selection import cross_val_score
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer

all_text = df['reviews_text']
train_text = df['reviews_text']
y = df['reviews_rating']

# Mapping positive sentiment as 1 and negative as 0 

df['Sentiment_coded'] = np.where(df.user_sentiment == 'Positive',1,0)

# Printing the counts of each class
df['Sentiment_coded'].value_counts()

word_vectorizer = TfidfVectorizer(sublinear_tf = True,
                                  strip_accents = 'unicode',
                                  analyzer = 'word',
                                  token_pattern =r'\w{1,}',
                                  stop_words = 'english',
                                  ngram_range = (1, 1),
                                  max_features = 10000)
word_vectorizer.fit(all_text)
train_word_features = word_vectorizer.transform(train_text)

char_vectorizer = TfidfVectorizer(sublinear_tf = True,
                                  strip_accents = 'unicode',
                                  analyzer = 'char',
                                  stop_words = 'english',
                                  ngram_range = (2, 6),
                                  max_features = 50000)
char_vectorizer.fit(all_text)
train_char_features = char_vectorizer.transform(train_text)
train_features = hstack([train_char_features, train_word_features])



# Saving the vectorizer to be used for deployment

import pickle

# Save to file in the current working directory
pkl_filename = "Tfidf_vectorizer.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(char_vectorizer, file)

# Load from file
with open(pkl_filename, 'rb') as file:
    pickled_tfidf_vectorizer = pickle.load(file)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train_features,
                                                    y,
                                                    test_size = 0.3,
                                                    random_state = 42)

X_train1 = X_train[:, 0:50000] #fix for Value error
X_test1 = X_test[:, 0:50000] #fix for Value error
print(X_train1.shape)
print(X_test1.shape)
print(y_train.shape)
print(y_test.shape)

from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(n_estimators=300)
classifier.fit(X_train1, y_train)
rf_preds = classifier.predict(X_test1)

from sklearn.metrics import accuracy_score

rf_accuracy = accuracy_score(rf_preds, y_test)
print("Random Forest Model accuracy: ", rf_accuracy)

# Saving the best accuracy model as pickle file
import pickle

# Save to file in the current working directory
pkl_filename = "Randomforest_final_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(classifier, file)

# Load from file
with open(pkl_filename, 'rb') as file:
    pickled_model = pickle.load(file)

"""### Accuracy score of Random Forest model 76.67%"""

import xgboost as xgb

xgb = xgb.XGBClassifier()

xgb.fit(X_train,
        y_train)

xgb_preds = xgb.predict(X_test)
xgb_accuracy = accuracy_score(xgb_preds, y_test)
print("XGBoost Model accuracy: ", xgb_accuracy)

"""### Accuracy score of XGBoost model 74.64%. """

from sklearn.naive_bayes import MultinomialNB

clf = MultinomialNB().fit(X_train, y_train)

rf_preds1 = clf.predict(X_test)

rf_accuracy1 = accuracy_score(rf_preds1, y_test)
print("Naive Bayes Model accuracy: ", rf_accuracy1)

"""### Accuracy score of Naive Bayes model 70.93%.

# From the above three models, we use Random Forest model which has the highest accuracy out of the three models (Random forest, XGBoost and Naive Bayes)

# Recommendation System 
- User based recommendation
- User based prediction & evaluation
- Item based recommendation
- Item based prediction & evaluation

Different Approaches to develop Recommendation System -

1. Demographich based Recommendation System

2. Content Based Recommendation System

3. Collaborative filtering Recommendation System
"""

ratings = pd.read_csv('/content/drive/My Drive/NLP_Reco/sample30.csv', encoding='latin-1')
ratings.head()

"""## Dividing the dataset into train and test"""

# Test and Train split of the dataset.
from sklearn.model_selection import train_test_split
train, test = train_test_split(ratings, test_size=0.30, random_state=31)

print(train.shape)
print(test.shape)

# Pivot the train ratings' dataset into matrix format in which columns are product and the rows are user IDs.
df_pivot = train.pivot_table(
    index='reviews_username',
    columns='name',
    values='reviews_rating'
).fillna(0)

df_pivot.head(3)

"""### Creating dummy train & dummy test dataset
These dataset will be used for prediction 
- Dummy train will be used later for prediction of the product which has not been rated by the user. To ignore the products rated by the user, we will mark it as 0 during prediction. The products not rated by user is marked as 1 for prediction in dummy train dataset. 

- Dummy test will be used for evaluation. To evaluate, we will only make prediction on the products rated by the user. So, this is marked as 1. This is just opposite of dummy_train.
"""

# Copy the train dataset into dummy_train
dummy_train = train.copy()

# The products not rated by user is marked as 1 for prediction. 
dummy_train['reviews_rating'] = dummy_train['reviews_rating'].apply(lambda x: 0 if x>=1 else 1)

# Convert the dummy train dataset into matrix format.
dummy_train = dummy_train.pivot_table(
    index='reviews_username',
    columns='name',
    values='reviews_rating'
).fillna(1)

dummy_train.head()

"""**Cosine Similarity**

Cosine Similarity is a measurement that quantifies the similarity between two vectors [Which is Rating Vector in this case] 

**Adjusted Cosine**

Adjusted cosine similarity is a modified version of vector-based similarity where we incorporate the fact that different users have different ratings schemes. In other words, some users might rate items highly in general, and others might give items lower ratings as a preference. To handle this nature from rating given by user , we subtract average ratings for each user from each user's rating for different products.

# User Similarity Matrix

## Using Cosine Similarity
"""

from sklearn.metrics.pairwise import pairwise_distances

# Creating the User Similarity Matrix using pairwise_distance function.
user_correlation = 1 - pairwise_distances(df_pivot, metric='cosine')
user_correlation[np.isnan(user_correlation)] = 0
print(user_correlation)

user_correlation.shape

"""## Using adjusted Cosine

### Here, we are not removing the NaN values and calculating the mean only for the movies rated by the user
"""

# Create a user-movie matrix.
df_pivot = train.pivot_table(
    index='reviews_username',
    columns='name',
    values='reviews_rating'
)

df_pivot.head()

"""### Normalising the rating of the product for each user around 0 mean"""

mean = np.nanmean(df_pivot, axis=1)
df_subtracted = (df_pivot.T-mean).T

df_subtracted.head()

"""### Finding cosine similarity"""

from sklearn.metrics.pairwise import pairwise_distances

# Creating the User Similarity Matrix using pairwise_distance function.
user_correlation = 1 - pairwise_distances(df_subtracted.fillna(0), metric='cosine')
user_correlation[np.isnan(user_correlation)] = 0
print(user_correlation)

"""## Prediction - User User

Doing the prediction for the users which are positively related with other users, and not the users which are negatively related as we are interested in the users which are more similar to the current users. So, ignoring the correlation for values less than 0.
"""

user_correlation[user_correlation<0]=0
user_correlation

"""Rating predicted by the user (for movies rated as well as not rated) is the weighted sum of correlation with the movie rating (as present in the rating dataset)."""

user_predicted_ratings = np.dot(user_correlation, df_pivot.fillna(0))
user_predicted_ratings

user_predicted_ratings.shape

"""Since we are interested only in the products not rated by the user, we will ignore the products rated by the user by making it zero."""

user_final_rating = np.multiply(user_predicted_ratings,dummy_train)
user_final_rating.head()

"""### Finding the top 20 recommendation for the *user*"""

# Take the user ID as input.
user_input = input("Enter your user name")
print(user_input)

user_final_rating.head(2)

d = user_final_rating.loc[user_input].sort_values(ascending=False)[0:20]
d

mapping=ratings[['id','name']]
mapping = pd.DataFrame.drop_duplicates(mapping)
mapping.head()

#Merging product id with mapping file to get the name of the recommended product
d = pd.merge(d,mapping, left_on='name', right_on='name', how = 'left')
d

"""# Evaluation - User User

Evaluation will we same as you have seen above for the prediction. The only difference being, you will evaluate for the movie already rated by the user insead of predicting it for the movie not rated by the user.
"""

# Find out the common users of test and train dataset.
common = test[test.reviews_username.isin(train.reviews_username)]
common.shape

common.head()

# convert into the user-product matrix.
common_user_based_matrix = common.pivot_table(index='reviews_username', columns='name', values='reviews_rating')

# Convert the user_correlation matrix into dataframe.
user_correlation_df = pd.DataFrame(user_correlation)

df_subtracted.head(1)

user_correlation_df['reviews_username'] = df_subtracted.index
user_correlation_df.set_index('reviews_username',inplace=True)
user_correlation_df.head()

common.head(1)

list_name = common.reviews_username.tolist()

user_correlation_df.columns = df_subtracted.index.tolist()


user_correlation_df_1 =  user_correlation_df[user_correlation_df.index.isin(list_name)]

user_correlation_df_1.shape

user_correlation_df_2 = user_correlation_df_1.T[user_correlation_df_1.T.index.isin(list_name)]

user_correlation_df_3 = user_correlation_df_2.T

user_correlation_df_3.head()

user_correlation_df_3.shape

user_correlation_df_3[user_correlation_df_3<0]=0

common_user_predicted_ratings = np.dot(user_correlation_df_3, common_user_based_matrix.fillna(0))
common_user_predicted_ratings

dummy_test = common.copy()

dummy_test['reviews_rating'] = dummy_test['reviews_rating'].apply(lambda x: 1 if x>=1 else 0)

dummy_test = dummy_test.pivot_table(index='reviews_username', columns='name', values='reviews_rating').fillna(0)

dummy_test.shape

common_user_predicted_ratings = np.multiply(common_user_predicted_ratings,dummy_test)

common_user_predicted_ratings.head(2)

"""Calculating the RMSE for only the products rated by user. For RMSE, normalising the rating to (1,5) range."""

from sklearn.preprocessing import MinMaxScaler
from numpy import *

X  = common_user_predicted_ratings.copy() 
X = X[X>0]

scaler = MinMaxScaler(feature_range=(1, 5))
print(scaler.fit(X))
y = (scaler.transform(X))

print(y)

common_ = common.pivot_table(index='reviews_username', columns='name', values='reviews_rating')

# Finding total non-NaN value
total_non_nan = np.count_nonzero(~np.isnan(y))

rmse = (sum(sum((common_ - y )**2))/total_non_nan)**0.5
print(rmse)

"""## Using Item similarity

# Item Based Similarity

Taking the transpose of the rating matrix to normalize the rating around the mean for different product names. In the user based similarity, we had taken mean for each user instead of each product.
"""

df_pivot = train.pivot_table(
    index='reviews_username',
    columns='name',
    values='reviews_rating'
).T

df_pivot.head()

"""##Normalising the product rating for each product for using the Adujsted Cosine"""

mean = np.nanmean(df_pivot, axis=1)
df_subtracted = (df_pivot.T-mean).T

df_subtracted.head()

"""#Finding the cosine similarity using pairwise distances approach"""

from sklearn.metrics.pairwise import pairwise_distances

# Item Similarity Matrix
item_correlation = 1 - pairwise_distances(df_subtracted.fillna(0), metric='cosine')
item_correlation[np.isnan(item_correlation)] = 0
print(item_correlation)

"""#Filtering the correlation only for which the value is greater than 0. (Positively correlated)"""

item_correlation[item_correlation<0]=0
item_correlation

"""# Prediction - Item Item"""

item_predicted_ratings = np.dot((df_pivot.fillna(0).T),item_correlation)
item_predicted_ratings

item_predicted_ratings.shape

dummy_train.shape

"""### Filtering the rating only for the products not rated by the user for recommendation"""

item_final_rating = np.multiply(item_predicted_ratings,dummy_train)
item_final_rating.head()

"""### Finding the top 20 recommendation for the *user*"""

# Take the reviewer_usernam as input
user_input = input("Enter your user name")
print(user_input)

# Recommending the Top 20 products to the user.
d = item_final_rating.loc[user_input].sort_values(ascending=False)[0:20]
d

mapping=ratings[['id','name']]
mapping = pd.DataFrame.drop_duplicates(mapping)
mapping.head()

d = pd.merge(d,mapping, left_on='name', right_on='name', how = 'left')
d

"""# Evaluation - Item Item

##Evaluation will we same as you have seen above for the prediction. The only difference being, you will evaluate for the product already rated by the user insead of predicting it for the product not rated by the user.
"""

test.columns

common =  test[test.name.isin(train.name)]
common.shape

common.head(4)

common_item_based_matrix = common.pivot_table(index='reviews_username', columns='name', values='reviews_rating').T

common_item_based_matrix.shape

item_correlation_df = pd.DataFrame(item_correlation)

item_correlation_df.head(1)

item_correlation_df['name'] = df_subtracted.index
item_correlation_df.set_index('name',inplace=True)
item_correlation_df.head()

list_name = common.name.tolist()

item_correlation_df.columns = df_subtracted.index.tolist()

item_correlation_df_1 =  item_correlation_df[item_correlation_df.index.isin(list_name)]

item_correlation_df_2 = item_correlation_df_1.T[item_correlation_df_1.T.index.isin(list_name)]

item_correlation_df_3 = item_correlation_df_2.T

item_correlation_df_3.head()

item_correlation_df_3[item_correlation_df_3<0]=0

common_item_predicted_ratings = np.dot(item_correlation_df_3, common_item_based_matrix.fillna(0))
common_item_predicted_ratings

common_item_predicted_ratings.shape

"""##Dummy test will be used for evaluation. To evaluate, we will only make prediction on the products rated by the user. So, this is marked as 1. This is just opposite of dummy_train

"""

dummy_test = common.copy()

dummy_test['reviews_rating'] = dummy_test['reviews_rating'].apply(lambda x: 1 if x>=1 else 0)

dummy_test = dummy_test.pivot_table(index='reviews_username', columns='name', values='reviews_rating').T.fillna(0)

common_item_predicted_ratings = np.multiply(common_item_predicted_ratings,dummy_test)

"""#The products not rated is marked as 0 for evaluation. And make the item- item matrix representaion."""

common_ = common.pivot_table(index='reviews_username', columns='name', values='reviews_rating').T

from sklearn.preprocessing import MinMaxScaler
from numpy import *

X  = common_item_predicted_ratings.copy() 
X = X[X>0]

scaler = MinMaxScaler(feature_range=(1, 5))
print(scaler.fit(X))
y = (scaler.transform(X))

print(y)

# Finding total non-NaN value
total_non_nan = np.count_nonzero(~np.isnan(y))

rmse = (sum(sum((common_ - y )**2))/total_non_nan)**0.5
print(rmse)

# Take the user ID as input
user_input = str(input("Enter your user name"))
print(user_input)

recommendations = user_final_rating.loc[user_input].sort_values(ascending=False)[0:20]
mapping= ratings[['id','name']]
mapping = pd.DataFrame.drop_duplicates(mapping)
recommendations = pd.merge(recommendations,mapping, left_on='name', right_on='name', how = 'left')
recommendations

"""#RMSE for User based recommendation system is lower and is chosen"""

import pickle

user_final_rating.to_pickle("user_final_rating.pkl")
pickled_user_final_rating = pd.read_pickle("user_final_rating.pkl")
pickled_user_final_rating

# Save to file in the current working directory

mapping.to_pickle("prod_id_name_mapping.pkl")
pickled_mapping = pd.read_pickle("prod_id_name_mapping.pkl")
pickled_mapping

# Save to file in the current working directory

df.to_pickle("reviews_data_all_cols.pkl")
pickled_reviews_data = pd.read_pickle("reviews_data_all_cols.pkl")
pickled_reviews_data

"""
#Improving the recommendations using the sentiment analysis model
### Recommending top 5 products to the user based based on Random forest model chosen"""

#Improving recommender system

improved_recommendations= pd.merge(recommendations,pickled_reviews_data[['name','reviews_text']], left_on='name', right_on='name', how = 'left')
test_data_for_user = pickled_tfidf_vectorizer.transform(improved_recommendations['reviews_text'])
print(test_data_for_user.shape)
sentiment_prediction_for_user= pickled_model.predict(test_data_for_user)
df = pd.DataFrame(df, columns=['Predicted_Sentiment'])
improved_recommendations= pd.concat([improved_recommendations, df], axis=1)

# Recommending top 5 products
a=improved_recommendations.groupby('name')
b=pd.DataFrame(a['Predicted_Sentiment'].count()).reset_index()
b.columns = ['name', 'Total_reviews']
c=pd.DataFrame(a['Predicted_Sentiment'].sum()).reset_index()
c.columns = ['name', 'Total_predicted_positive_reviews']
improved_recommendations_final=pd.merge( b, c, left_on='name', right_on='name', how='left')
improved_recommendations_final['Positive_sentiment_rate'] = improved_recommendations_final['Total_predicted_positive_reviews'].div(improved_recommendations_final['Total_reviews']).replace(np.inf, 0)
improved_recommendations_final= improved_recommendations_final.sort_values(by=['Positive_sentiment_rate'], ascending=False )
improved_recommendations_final=pd.merge(improved_recommendations_final, pickled_mapping, left_on='name', right_on='name', how='left')

#Top 5 recommended product
improved_recommendations_final['name'].head(5)

#Downloading Pickle files
#from google.colab import files
#files.download('user_final_rating.pkl')

#files.download('Randomforest_final_model.pkl')

"""#Deploying the project with a user interface
An end-to-end web application is deployed using Flask and Heroku Random forest model and User based recommendation system at given URL- https://nlp-reco.herokuapp.com/

The app takes the username as input and submitting, it recommends the top 5 products based on the username entered

All files used to deploy the model are placed at - https://github.com/Nibha2022/sentiment_analysis
"""

