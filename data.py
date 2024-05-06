#Author: Sebastian Andrade
#Due Date: 05/05/2024
#Final Project
#File Description: API connections and CLI
#Note: Main at line 382

#Libraries
import psycopg2
from psycopg2 import sql
import requests
from dotenv import load_dotenv
import os

load_dotenv()

#Access environment variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

#Function to fetch teams from La Liga
def fetch_team_data():
    print("Fetching La Liga Team Data")
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    querystring = {"league":"140","season":"2023"}

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    teams_data = data.get("response", [])
    return teams_data

#Function to fetch players from La Liga (All players from La Liga?)
def fetch_all_players():
    all_players = []
    page = 1

    while True:
        print(f"Fetching players - Page {page}")

        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        querystring = {
            "league": "140",
            "season": "2023",
            "page": page
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        players_data = data.get("response", [])

        all_players.extend(players_data)

        if not players_data:
            break
        page += 1
    return all_players



#Function to fetch matches from La Liga 2023-24 season
def fetch_matches_data():
    print("Fetching La Liga Matches Data")
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    querystring = {"league":"140","season":"2023"}

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    matches_data = data.get("response", [])
    return matches_data


#Function to fetch current standings from La Liga 2023-24 season
def fetch_standings_data():
    print("Fetching La Liga Standings Data")
    url = "https://api-football-v1.p.rapidapi.com/v3/standings"
    headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    querystring = {"league":"140","season":"2023"}

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    standings_data = data.get("response", [])
    return standings_data


#Function to fetch top scorers from La Liga 2023-24 season 
def fetch_top_scorers_data():
    print("Fetching La Liga Top Scorers Data")
    url = "https://api-football-v1.p.rapidapi.com/v3/players/topscorers"
    headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    querystring = {"league":"140","season":"2023"}

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    top_scorers_data = data.get("response", [])
    return top_scorers_data

def parse_data(table_name, data):
   print(f"Parsing data for {table_name}")
   parsed_data = []
   if table_name == "teams":
        for team_data in data:
            team_info = team_data["team"]
            venue_info = team_data["venue"]

            team_id = team_info["id"]
            team_name = team_info["name"]
            team_country = team_info["country"]
            team_founded = team_info["founded"]
            team_logo = team_info["logo"]

            venue_id = venue_info["id"]
            venue_name = venue_info["name"]
            venue_address = venue_info["address"]
            venue_city = venue_info["city"]
            venue_capacity = venue_info["capacity"]
            #Create dictionary representing a row of data
            row_data = {
                "team_id": team_id,
                "team_name": team_name,
                "team_country": team_country,
                "team_founded": team_founded,
                "team_logo": team_logo,
                "venue_id": venue_id,
                "venue_name": venue_name,
                "venue_address": venue_address,
                "venue_city": venue_city,
                "venue_capacity": venue_capacity
            }
            parsed_data.append(row_data)  #Append the row data to the list
        return parsed_data

   elif table_name == "players":
        for player_data in data:
            player_info = player_data["player"]
            statistics_info = player_data["statistics"][0]

            player_id = player_info["id"]
            player_name = player_info["name"]
            player_first_name = player_info["firstname"]
            player_last_name = player_info["lastname"]
            player_age = player_info["age"]
            player_birth_date = player_info["birth"]["date"]
            player_birth_place = player_info["birth"]["place"]
            player_birth_country = player_info["birth"]["country"]
            player_nationality = player_info["nationality"]
            player_photo = player_info["photo"]
            

            team_id = statistics_info["team"]["id"]
            team_name = statistics_info["team"]["name"]

            player_position = statistics_info["games"]["position"]

            row_data = {
                "player_id": player_id,
                "player_name": player_name,
                "player_first_name": player_first_name,
                "player_last_name": player_last_name,
                "player_age": player_age,
                "player_birth_date": player_birth_date,
                "player_birth_place": player_birth_place,
                "player_birth_country": player_birth_country,
                "player_nationality": player_nationality,
                "player_photo": player_photo,
                "team_id": team_id,
                "team_name": team_name,
                "player_position": player_position
            }
            parsed_data.append(row_data)
        return parsed_data
   elif table_name == "matches":
        for match_data in data:
            fixture_id = match_data["fixture"]["id"]
            fixture_referee = match_data["fixture"]["referee"]
            fixture_timezone = match_data["fixture"]["timezone"]
            fixture_date = match_data["fixture"]["date"]
            fixture_venue_id = match_data["fixture"]["venue"]["id"]
            fixture_venue_name = match_data["fixture"]["venue"]["name"]
            fixture_venue_city = match_data["fixture"]["venue"]["city"]
            fixture_status = match_data["fixture"]["status"]["short"]
            fixture_ft = match_data["fixture"]["status"]["elapsed"]


            league_round = match_data["league"]["round"]

            home_id = match_data["teams"]["home"]["id"]
            home_name = match_data["teams"]["home"]["name"]
            home_logo = match_data["teams"]["home"]["logo"]
            home_result = match_data["teams"]["home"]["winner"]

            away_id = match_data["teams"]["away"]["id"]
            away_name = match_data["teams"]["away"]["name"]
            away_logo = match_data["teams"]["away"]["logo"]
            away_result = match_data["teams"]["away"]["winner"]

            home_goals = match_data["goals"]["home"]
            away_goals = match_data["goals"]["away"]

            row_data = {
                "fixture_id": fixture_id,
                "fixture_referee": fixture_referee,
                "fixture_timezone": fixture_timezone,
                "fixture_date": fixture_date,
                "fixture_venue_id": fixture_venue_id,
                "fixture_venue_name": fixture_venue_name,
                "fixture_venue_city": fixture_venue_city,
                "fixture_status": fixture_status,
                "fixture_ft": fixture_ft,
                "league_round": league_round,
                "home_id": home_id,
                "home_name": home_name,
                "home_logo": home_logo,
                "home_result": home_result,
                "away_id": away_id,
                "away_name": away_name,
                "away_logo": away_logo,
                "away_result": away_result,
                "home_goals": home_goals,
                "away_goals": away_goals,
            }
            parsed_data.append(row_data)  #Append the row data to the list
        return parsed_data
   elif table_name == "standings":
        item = 0
        while item < 20:
            for standings_data in data:
                rank = standings_data["league"]["standings"][0][item]["rank"]
                team_id = standings_data["league"]["standings"][0][item]["team"]["id"]
                team_name = standings_data["league"]["standings"][0][item]["team"]["name"]
                team_logo = standings_data["league"]["standings"][0][item]["team"]["logo"]
                points = standings_data["league"]["standings"][0][item]["points"]
                goal_differential = standings_data["league"]["standings"][0][item]["goalsDiff"]
                form = standings_data["league"]["standings"][0][item]["form"]
                status = standings_data["league"]["standings"][0][item]["status"]
                description = standings_data["league"]["standings"][0][item]["description"]
                games_played = standings_data["league"]["standings"][0][item]["all"]["played"] 
                games_won = standings_data["league"]["standings"][0][item]["all"]["win"] 
                games_drawn = standings_data["league"]["standings"][0][item]["all"]["draw"] 
                games_lost = standings_data["league"]["standings"][0][item]["all"]["lose"] 
                goals_scored = standings_data["league"]["standings"][0][item]["all"]["goals"]["for"]
                goals_conceded = standings_data["league"]["standings"][0][item]["all"]["goals"]["against"]
                last_updated = standings_data["league"]["standings"][0][item]["update"]
                
                row_data = {
                    "rank": rank,
                    "team_id": team_id,
                    "team_name": team_name,
                    "team_logo": team_logo,
                    "points": points,
                    "goal_differential": goal_differential,
                    "form": form,
                    "status": status,
                    "description": description,
                    "games_played": games_played,
                    "games_won": games_won,
                    "games_drawn": games_drawn,
                    "games_lost": games_lost,
                    "goals_scored": goals_scored,
                    "goals_conceded": goals_conceded,
                    "last_updated": last_updated,
                }
            parsed_data.append(row_data)  #Append the row data to the list
            item += 1
        return parsed_data
   elif table_name == "top_scorers":
        for player_data in data:
            player_info = player_data["player"]
            statistics_info = player_data["statistics"][0]

            player_id = player_info["id"]
            player_name = player_info["name"]
            player_first_name = player_info["firstname"]
            player_last_name = player_info["lastname"]
            total_goals = statistics_info["goals"]["total"]
            player_position = statistics_info["games"]["position"]
            player_nationality = player_info["nationality"]

            team_id = statistics_info["team"]["id"]
            team_name = statistics_info["team"]["name"]

            appearances = statistics_info["games"]["appearences"]
            started = statistics_info["games"]["lineups"]
            minutes = statistics_info["games"]["minutes"]
            rating = statistics_info["games"]["rating"]
            total_shots = statistics_info["shots"]["total"]
            shots_on_target = statistics_info["shots"]["total"]
            assists = statistics_info["goals"]["assists"]
            yellow_cards = statistics_info["cards"]["yellow"]
            yellow_then_red = statistics_info["cards"]["yellowred"]
            red = statistics_info["cards"]["red"]
            penalties_scored = statistics_info["penalty"]["scored"]
            penalties_missed = statistics_info["penalty"]["missed"]


            #Create a dictionary representing a row of data
            row_data = {
                "player_id": player_id,
                "player_name": player_name,
                "player_first_name": player_first_name,
                "player_last_name": player_last_name,
                "total_goals": total_goals,
                "player_position": player_position,
                "player_nationality": player_nationality,
                "team_id": team_id,
                "team_name": team_name,
                "appearances": appearances,
                "started": started,
                "minutes": minutes,
                "rating": rating,
                "total_shots": total_shots,
                "shots_on_target": shots_on_target,
                "assists": assists,
                "yellow_cards": yellow_cards,
                "yellow_then_red": yellow_then_red,
                "red_cards": red,
                "penalties_scored": penalties_scored,
                "penalties_missed": penalties_missed
            }
            parsed_data.append(row_data)
        return parsed_data
   else:
       print("Incorrect table name\n")
       return


   
#Function that inserts data into database
def insert_data_into_postgresql(table_name, data):
    print("Inserting data into PostgreSQL")
    try:
        #Connect to PostgreSQL
        connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cursor = connection.cursor()
        for row in data:
            columns = row.keys()
            values = [row[column] for column in columns]

            insert_statement = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(values))
            )

            cursor.execute(insert_statement, values)
        #Commit the transaction
        connection.commit()
        print("Data inserted successfully into PostgreSQL")

    except psycopg2.Error as e:
        print("Error inserting data into PostgreSQL:", e)

    finally:
        #Close the cursor and connection
        cursor.close()
        connection.close()

def display_json_data(data):
    for item in data:
        print(data)

def main():
    #MAIN CALLS

    #Call to fetch team data, parse, and insert into PostgreSQL
    teams_data = fetch_team_data()
    display_json_data(parse_data("teams", teams_data))
    insert_data_into_postgresql("teams", parse_data("teams", teams_data))

    #Call to fetch all player data, parse, and insert into PostgreSQL
    all_players = fetch_all_players()
    insert_data_into_postgresql("players", parse_data("players", all_players))

    #Call to fetch match data from current season, parse, and insert into PostgreSQL
    matches_data = fetch_matches_data()
    display_json_data(parse_data("matches", matches_data))
    insert_data_into_postgresql("matches", parse_data("matches", matches_data))

    #Call to fetch standings data from current season, parse, and insert into PostgreSQL
    standings_data = fetch_standings_data()
    insert_data_into_postgresql("standings", parse_data("standings", standings_data))

    #Call to fetch top scorers from La Liga 2023-24 season, parse, and insert into PostgreSQL
    top_scorers = fetch_top_scorers_data()
    insert_data_into_postgresql("top_scorers", parse_data("top_scorers", top_scorers))
    
    print("------------La Liga Soccer Database------------\n")
    print("Welcome to the La Liga soccer database!\n")
    print("        _...----.._")
    print("     ,:':::::.     `>.")
    print("   ,' |:::::;'     |:::.")
    print("  /    `'::'       :::::\\")
    print(" /         _____     `::;\\")
    print(":         /:::::\      `  :")
    print("| ,.     /:::::::\        |")
    print("|;:::.   `::::::;'        |")
    print("::::::     `::;'      ,.  ;")
    print(" \:::'              ,::::/")
    print("  \                 \:::/")
    print("   `.     ,:.        :;'")
    print("     `-.::::::..  _.''")
    print("        ```----'''")
    print("                 ")


    previous_choices = []
    while True:
        print("Type '1' to add data into the database.")
        print("Type '2' to retrieve data from the database.")
        print("Type '3' to exit.")
        print("WARNING: Make sure there is no current data in the tables but the tables are already created with correct attributes, otherwise there will be duplicates or there will be errors!!!")
        user_choice = input("Please enter your choice: ")

        if user_choice == '1':
            previous_choices.append(user_choice)
            print("Type '1' to add a team into La Liga.")
            print("Type '2' to add a player into La Liga.")
            print("Type '3' to add a match that has already occurred into the current season.")
            print("Type '4' to go back to previous page.")
            add_data_choice = input("Please enter your choice: ")
            if add_data_choice == '1':
                team_name = input("Provide the name of the team to add: ")
                team_country = input("Provide the country the team is from: ")
                team_founded = input("Provide the year in which the team was founded: ")
                team_logo = input("Provide a link to the image of the team logo: ")
                venue_name = input("What is the name of the stadium? ")
                venue_address = input("What is the address of the stadium? ")
                venue_city = input("In what city is this stadium in? ")
                venue_capacity = input("How many people can this stadium hold? ")
                try:
                    #Connect to PostgreSQL
                    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
                    with connection.cursor() as cur:
                        cur.execute("SELECT MAX(team_id) FROM teams")
                        max_team_id = cur.fetchone()[0]
                        int_team_id = int(max_team_id)
                        next_team_id = int_team_id + 1
                        str_next_team = str(next_team_id)

                        cur.execute("SELECT MAX(venue_id) FROM teams")
                        max_venue_id = cur.fetchone()[0]
                        int_venue_id = int(max_venue_id)
                        next_venue_id = int_venue_id + 1
                        str_next_venue = str(next_venue_id)

                        cur.execute("""
                                        INSERT INTO teams (team_id, team_name, team_country, team_founded, team_logo, venue_id, venue_name, venue_address, venue_city, venue_capacity)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """, (str_next_team, team_name, team_country, team_founded, team_logo, str_next_venue, venue_name, venue_address, venue_city, venue_capacity))
                        cur.execute("SELECT * FROM teams ORDER BY team_id DESC LIMIT 1")
                        last_row = cur.fetchone()
                        print("Last row inserted: ", last_row)
                        connection.commit()
                        print("Data inserted successfully into PostgreSQL")

                except psycopg2.Error as e:
                    print("Error inserting data into PostgreSQL:", e)

                finally:
                    #Close the cursor and connection
                    cur.close()
                    connection.close()
                            
            elif add_data_choice == '2':
                #player_id
                player_name = input("Provide the name of the player they want to go by: ")
                player_first_name = input("Provide the player's first name: ")
                player_last_name = input("Provide the player's last name: ")
                player_age = input("Provide the player's current age: ")
                player_birth_date = input("Provide the player's date of birth in the format YYYY-MM-DD: ")
                player_birth_place = input("Provide the player's birth city: ")
                player_birth_country = input("Provide the player's birth country: ")
                player_nationality = input("Provide the player's nationality: ")
                player_photo = input("Provide a link of the player's photo, otherwise type N/A: ")
                #team_id
                team_name = input("What club does this player play for? ")
                player_position = input("What is the player's position of choice? ")
                try:
                    #Connect to PostgreSQL
                    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
                    with connection.cursor() as cur:
                        cur.execute("SELECT MAX(player_id) FROM players")
                        max_player_id = cur.fetchone()[0]
                        int_player_id = int(max_player_id)
                        next_player_id = int_player_id + 1
                        str_next_player = str(next_player_id)

                        cur.execute("SELECT MAX(team_id) FROM players")
                        max_team_id = cur.fetchone()[0]
                        int_team_id = int(max_team_id)
                        next_team_id = int_team_id + 1
                        str_next_team = str(next_team_id)

                        cur.execute("""
                                        INSERT INTO players (player_id, player_name, player_first_name, player_last_name, player_age, player_birth_date, player_birth_place, player_birth_country, player_nationality, player_photo, team_id, team_name, player_position )
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """, (str_next_player, player_name, player_first_name, player_last_name, player_age, player_birth_date, player_birth_place, player_birth_country, player_nationality, player_photo, str_next_team, team_name, player_position))
                        cur.execute("SELECT * FROM players ORDER BY player_id DESC LIMIT 1")
                        last_row = cur.fetchone()
                        print("Last row inserted: ", last_row)
                        connection.commit()
                        print("Data inserted successfully into PostgreSQL")

                except psycopg2.Error as e:
                    print("Error inserting data into PostgreSQL:", e)

                finally:
                    #Close the cursor and connection
                    cur.close()
                    connection.close()
            elif add_data_choice == '3':
                #fixture_id
                fixture_referee = input("Provide the full name of the referee and the country they're from: ")
                fixture_timezone = input("Provide the timezone the match occurred in: ")
                fixture_date = input("Provide the date in which the match took place in format YYYY-MM-DD: ")
                #fixture_venue_id
                fixture_venue_name = input("What is the name of the stadium the match took place in? ")
                fixture_venue_city = input("In what city is this stadium in? ")
                fixture_status = input("Did the game finish, was it suspended, or was it postponed? Type FT, SS, or PP: ")
                fixture_ft = input("How many minutes total did the match play for? ")
                league_round = input("What round in the regular season did this match occur in? Type 'Regular Season - #' with # being the round number: ") 
                #home_id
                home_name = input("Provide the name of the club that played at home: ")
                home_logo = input("Provide the link of the club's logo: ")
                home_result = input("Did the home team win? If yes, type 'true'. If no, type 'false: ")
                #away_id
                away_name = input("Provide the name of the club that played away: ")
                away_logo = input("Provide the link of the club's logo: ")
                away_result = input("Did the away team win? If yes, type 'true'. If no, type 'false: ")
                home_goals = input("How many goals did the home team score? ")
                away_goals = input("How many goals did the away team score? ")

                try:
                    # Connect to PostgreSQL
                    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
                    with connection.cursor() as cur:
                        cur.execute("SELECT MAX(fixture_id) FROM matches")
                        max_fixture_id = cur.fetchone()[0]
                        int_fixture_id = int(max_fixture_id)
                        next_fixture_id = int_fixture_id + 1
                        str_next_fixture = str(next_fixture_id)

                        cur.execute("SELECT MAX(fixture_venue_id) FROM matches")
                        max_fixture_venue_id = cur.fetchone()[0]
                        int_fixture_venue_id = int(max_fixture_venue_id)
                        next_fixture_venue_id = int_fixture_venue_id + 1
                        str_next_fixture_venue_id = str(next_fixture_venue_id)

                        cur.execute("SELECT MAX(home_id) FROM matches")
                        max_home_id = cur.fetchone()[0]
                        int_home_id = int(max_home_id)
                        next_home_id = int_home_id + 1
                        str_next_home_id = str(next_home_id)

                        cur.execute("SELECT MAX(fixture_venue_id) FROM matches")
                        max_away_id = cur.fetchone()[0]
                        int_away_id = int(max_away_id)
                        next_away_id = int_away_id + 1
                        str_next_away_id = str(next_away_id)

                        cur.execute("""
                                        INSERT INTO matches (fixture_id, fixture_referee, fixture_timezone, fixture_date, fixture_venue_id, fixture_venue_name, fixture_venue_city, fixture_status, fixture_ft, league_round, home_id, home_name, home_logo, home_result, away_id, away_name, away_logo, away_result, home_goals, away_goals)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """, (str_next_fixture, fixture_referee, fixture_timezone, fixture_date, str_next_fixture_venue_id, fixture_venue_name, fixture_venue_city, fixture_status, fixture_ft, league_round, str_next_home_id, home_name, home_logo, home_result, str_next_away_id, away_name, away_logo, away_result, home_goals, away_goals))
                        cur.execute("SELECT * FROM matches ORDER BY fixture_id DESC LIMIT 1")
                        last_row = cur.fetchone()
                        print("Last row inserted: ", last_row)
                        connection.commit()
                        print("Data inserted successfully into PostgreSQL")

                except psycopg2.Error as e:
                    print("Error inserting data into PostgreSQL:", e)

                finally:
                    # Close the cursor and connection
                    cur.close()
                    connection.close()
            elif add_data_choice == '4':
                if previous_choices:
                    previous_choices.pop()
            else:
                print("\nPlease enter a valid choice.\n")

        elif user_choice == '2':
            previous_choices.append(user_choice)
            print("Type '1' to retrieve all of the teams in La Liga.")
            print("Type '2' to retrieve all of the players in La Liga.")
            print("Type '3' to retrieve the current league standings.")
            print("Type '4' to retrieve all of the current matches played in La Liga.")
            print("Type '5' to retrieve all of the current top scorers in the current season.")
            print("Type '6' to go back to previous page.")
            retrieve_data_choice = input("Please enter your choice from which table to retrieve from: ")
            if retrieve_data_choice == '1':
                try:
                #Connect to PostgreSQL
                    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
                    with connection.cursor() as cur:
                        cur.execute("SELECT * FROM teams")
                        all_teams = cur.fetchall()
                        for team in all_teams:
                            print(team)  
                    print("\nData retrieved successfully from PostgreSQL\n")
                except psycopg2.Error as e:
                    print("Error retrieving data from PostgreSQL:", e)
                finally:
                    #Close the cursor and connection
                    cur.close()
                    connection.close()
            elif retrieve_data_choice == '2':
                try:
                #Connect to PostgreSQL
                    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
                    with connection.cursor() as cur:
                        cur.execute("SELECT * FROM players")
                        all_players = cur.fetchall()
                        for player in all_players:
                            print(player)  
                    print("\nData retrieved successfully from PostgreSQL\n")
                except psycopg2.Error as e:
                    print("Error retrieving data from PostgreSQL:", e)
                finally:
                    #Close the cursor and connection
                    cur.close()
                    connection.close()
            elif retrieve_data_choice == '3':
                try:
                #Connect to PostgreSQL
                    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
                    with connection.cursor() as cur:
                        cur.execute("SELECT * FROM standings")
                        all_standings = cur.fetchall()
                        for standing in all_standings:
                            print(standing)  
                    print("\nData retrieved successfully from PostgreSQL\n")
                except psycopg2.Error as e:
                    print("Error retrieving data from PostgreSQL:", e)
                finally:
                    #Close the cursor and connection
                    cur.close()
                    connection.close()
            elif retrieve_data_choice == '4':
                try:
                #Connect to PostgreSQL
                    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
                    with connection.cursor() as cur:
                        cur.execute("SELECT * FROM matches")
                        all_matches = cur.fetchall()
                        for matches in all_matches:
                            print(matches)  
                    print("\nData retrieved successfully from PostgreSQL\n")
                except psycopg2.Error as e:
                    print("Error retrieving data from PostgreSQL:", e)
                finally:
                    #Close the cursor and connection
                    cur.close()
                    connection.close()
            elif retrieve_data_choice == '5':
                try:
                #Connect to PostgreSQL
                    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
                    with connection.cursor() as cur:
                        cur.execute("SELECT * FROM top_scorers")
                        all_top_scorers = cur.fetchall()
                        for top_scorer in all_top_scorers:
                            print(top_scorer)  
                    print("\nData retrieved successfully from PostgreSQL\n")
                except psycopg2.Error as e:
                    print("Error retrieving data from PostgreSQL:", e)
                finally:
                    #Close the cursor and connection
                    cur.close()
                    connection.close()
            elif retrieve_data_choice == '6':
                if previous_choices:
                    previous_choices.pop()
            else:
                print("\nPlease enter a valid choice.\n")
        elif user_choice == '3':
            print("Exiting...")
            exit()
        else:
            print("\nPlease enter a valid choice.\n")

if __name__ == "__main__":
    main()
