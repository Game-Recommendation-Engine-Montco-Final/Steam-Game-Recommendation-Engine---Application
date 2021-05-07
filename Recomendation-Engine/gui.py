import pandas as pd
import PySimpleGUI as sg

# Creates a path to access the CSV file containing the steam data
# Reads the path to make the CSV file usable
url = 'https://drive.google.com/file/d/1qrvArX7jJ8uMztFFAcr7-3eFUXALKZjK/view'
path = 'https://drive.google.com/uc?export=download&id=' + url.split('/')[-2]
ds = pd.read_csv(path, encoding= 'ISO-8859-1')

# Creates empty lists
games_list = []
appid_list = []

# Sets the color theme for the GUI
sg.theme('DarkBlue2')

# Popup welcoming using to the game recomender
sg.popup_no_buttons("Welcome to Steam Game Recommender!\n\n\n" + "Created by Nassim Guetiteni, Akash Shar, and Quang Bui\n\n", title= "Steam Game Recommender", auto_close=True, auto_close_duration=5, font=('5'))

# While loop to deduce the number of games the user wishes to input
while True:
    try:
        n = int(sg.popup_get_text('Please enter the number of games you want to add: ', title="Steam Game Recommender", size=(80,None), font= '10'))

        # If the user enters a number outside the range (1-3), they will be prompted with an error and be asked to try again
        if n < 1 or n > 3:
            raise ValueError
        break
    except ValueError:
        sg.popup_error("No valid integer! Please try again in the range 1-3 ...", title="ERROR")   

# Sets the length of the game list equal to the user input
games_list = [] * n

# While loop to ask for the name(s) of the game(s) the user wants to enter
i = 0
while i < n:
    game = sg.popup_get_text('Enter the name of the game you want to add:', title="Steam Game Recommender", size=(80,None), font= '10')

    # For loop to store the game name(s) from user input in game list
    for x in range(len(ds.name)):
        
        # Closes the popup if the user closes or cancels the program
        if game == sg.WIN_CLOSED or game == 'Cancel':
            sys.exit(0)     

        # Checks to see if the game exists within the database, if the game is not found it prompts the user with a error and asks for a new name
        if game != ds.name[x]:
            x+=1
            if x >= len(ds.name):
                sg.popup_error('Invalid Game Entered\n\n Returning to previous page', auto_close=True, auto_close_duration=3) # Sets the duration in case the user does not click the button
                x = 0

        # If the game is found within the database, it is appended to the games list
        if game == ds.name[x]:
            sg.popup_ok('Game Accepted', auto_close=True, auto_close_duration=2) # Sets the duration in case the user does not click the button
            games_list.append(game)
            i+=1
            break

# Tells the user that all of the games are accepted 
sg.popup_ok('Results Ready', title="Games Accepted", auto_close=True, auto_close_duration=3) # Sets the duration in case the user does not click the button

# Double checks all of the games the user entered with the games in the csv file
# Appends the appid of the inputted games to the appid list
# Skips the game the user entered if it is not found in the database
for i in range(len(games_list)):
    for j in range(len(ds.name)):
        if games_list[i] != ds.name[j]:
            result = False
            j+=1
            if j >= len(ds.name):
                j = 0
        if games_list[i] == ds.name[j]:
            result = True
            appid_list.append(ds.appid[j])
            break
    i+=1
