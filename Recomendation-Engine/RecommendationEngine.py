import pandas as pd
import PySimpleGUI as sg
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#gives path to access CSV file containing steam data
url = 'https://drive.google.com/file/d/1qrvArX7jJ8uMztFFAcr7-3eFUXALKZjK/view'
path = 'https://drive.google.com/uc?export=download&id=' + url.split('/')[-2]
ds = pd.read_csv(path, encoding= 'ISO-8859-1')

'''
Transforms text to feature vectors that can be used as input to estimator
TF-IDF stands for Term Frequency - Inverse Document Frequency is a statistic used 
to better define how important a word is for a document by looking at how many times 
a word appears into a document while also paying attention to 
how many times the same word appears in other documents
'''
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['tags'])

#Measures the similarity between two vectors and the distance between them, used to measaure similarity in text anylysis
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

# Creates an empty list for the results of the filter
results = {}

# Sorts the similarities between the games the user entered and the games in the csv file
# Adds the appid of the game that is going to be recommended to the array
for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['appid'][i]) for i in similar_indices]
    results[row['appid']] = similar_items[1:]
    
#print('done!')

def item(appid):
    return ds.loc[ds['appid'] == appid]['name'].tolist()[0]

# Calls the gui program for the user input
import gui


# Creates empty lists
review_list2 = []
price_list2 = []
game_list2 = []
tup_list = []
recommended_list = []


# Just reads the results out of the dictionary
def recommend(item_id, num):
    recs = results[item_id][:num]
    for rec in recs:
        game_list2.append(item(rec[1]))

        # Checks the game being recommended to every game in the csv file to find the price and review rating
        # Once the price and review rating are found, they will be added to the list
        for i in range(len(game_list2)):
            for j in range(len(ds.name)):
                if game_list2[i] != ds.name[j]:
                    result = False
                    j+=1
                    if j >= len(ds.name):
                        j = 0
                if game_list2[i] == ds.name[j]:
                    result = True
                    price_list2.append(ds.price[j])
                    review_list2.append(ds.review_rating[j])
                    break
            i+=1
        
        # Converts the elements from price_list2 from tuple to string
        # Checks for the price length and adds the price to the list
        for tup in price_list2:
            tup = str(tup)
            if len(tup) == 4:
                tup = "$" + tup[0:2] + "." + tup[2:]
                tup_list.append(tup)
            if len(tup) == 3:
                tup = "$" + tup[0:1] + "." + tup[1:]
                tup_list.append(tup)
            if len(tup) == 2:
                tup = "0." + tup
                tup_list.append(tup)  
            if len(tup) == 1:
                tup = "$" + tup + ".00"
                tup_list.append(tup)
        
        # Appends the recommended games
        recommended_list.append("Recommended: " + item(rec[1]) + " | Price: " + tup_list[0] + " | Rating: " + str(review_list2[0]) + "/10" + "\n\n")
        
        # Clears all of the arrays 
        game_list2.clear()
        price_list2.clear()
        review_list2.clear()
        tup_list.clear()



    '''
    Prints out the results in order of:
        * Recommended games
        * Prices
        * Review ratings
    '''
    sg.popup_scrolled("Recommending " + str(num) + " products similar to " + item(item_id) + "...\n" + "------------------------------------------------------------------------------------------------------------------------------------------------\n"
    , *recommended_list, size=(80, 15),title="Recommended Games", font='10')
    


#Determines number of games recommmended per game inputted (default set to 10)
# Calls the recommend function to publish the games in the pop-up window
for i in range(len(gui.appid_list)):
    recommend(item_id=(gui.appid_list[i]), num=10)
    print()