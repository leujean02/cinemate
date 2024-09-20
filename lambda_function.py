import json
import requests

def lambda_handler(event, context):
    # TODO implement
    api_key = "ac1b44ea"
    
    print(event)
    
    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    print("intent: " + str(intent))
    print("slots: " + str(slots))
    
    def fetch_movies(keyword, year):
        if not year:
            url = f"http://www.omdbapi.com/?i=tt3896198&apikey={api_key}&s={keyword}"
        else:
            url = f"http://www.omdbapi.com/?i=tt3896198&apikey={api_key}&s={keyword}&y={year}"
        
        response = requests.get(url)
        movies = response.json()
        
        print("movies: " + str(movies))


        if movies['Response'] == "True":
            message = "Here are the movies:\n" + "\n".join([movie['Title'] for movie in movies['Search']])
            message += "... and " + str(movies['totalResults'] + " more")
        else:
            message = "No movies matched your filters."
            
        print("message: " + str(message))
        
        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Close',
                    'fulfillmentState': 'Fulfilled',
                },
                'intent': {
                    'name': intent,
                    'state': 'Fulfilled',
                    'slots': slots
                }
            },
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': message 
                },
                {
                    'contentType': 'PlainText',
                    'content': "Is there anything else I can help with? Type 'Exact movie name' if you want to search for a specific movie title, or 'Keyword' to search for movies based on a word or phrase."  # Closing response
                }
            ]
        }
    
    if intent == "GetExactMovieByTitle":
        if not slots['MovieTitle']:
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': 'MovieTitle'
                    },
                    'intent': {
                        'name': intent,
                        'slots': slots,
                        'state': 'InProgress'
                    }
                }
            }
        
        movie_title = slots['MovieTitle']['value']['interpretedValue']
        # print("release year: " + str(slots['ReleaseYear']))
        
        if not slots['ReleaseYear']:
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': 'ReleaseYear'
                    },
                    'intent': {
                        'name': intent,
                        'slots': slots,
                        'state': 'InProgress'
                    }
                }
            }
        
        
        release_year = slots['ReleaseYear']['value']['interpretedValue']
            
        # print("release year: " + str(release_year))
        
        if release_year.lower() == 'n/a':
            url = f"http://www.omdbapi.com/?i=tt3896198&apikey={api_key}&t={movie_title}"
        elif not release_year.isdigit():
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': 'ReleaseYear'
                    },
                    'intent': {
                        'name': intent,
                        'slots': slots,
                        'state': 'InProgress'
                    }
                },
                'messages': [
                    {
                        'contentType': 'PlainText',
                        'content': 'Please enter a valid release year or type "n/a" if you do not want to specify a year.'
                    }
                ]
            }
        else:
            url = f"http://www.omdbapi.com/?i=tt3896198&apikey={api_key}&t={movie_title}&y={release_year}"
        
        response = requests.get(url)
        data = response.json()
        
        
        if data['Response'] == "True":
            message = f"Here's information for '{movie_title}':\n" \
                  f"Title: {data['Title']}\n" \
                  f"Released: {data['Released']}\n" \
                  f"Genre: {data['Genre']}\n" \
                  f"Director: {data['Director']}\n" \
                  f"Actors: {data['Actors']}\n" \
                  f"Plot: {data['Plot']}\n"
        else:
            message = f"Sorry, I couldn't find a movie with the title '{movie_title}'."
 
        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Close',
                    'fulfillmentState': 'Fulfilled',
                },
                'intent': {
                    'name': intent,
                    'state': 'Fulfilled',
                    'slots': slots
                }
            },
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': message 
                },
                {
                    'contentType': 'PlainText',
                    'content': "Is there anything else I can help with? Type 'Exact movie name' if you want to search for a specific movie title, or 'Keyword' to search for movies based on a word or phrase."  # Closing response
                }
            ]
        }
    
    elif intent == "GetMoviesByKeyword":
        if not slots['Keyword']:
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': 'Keyword'
                    },
                    'intent': {
                        'name': intent,
                        'slots': slots,
                        'state': 'InProgress'
                    }
                }
            }
        
        keyword = slots['Keyword']['value']['interpretedValue']
        year = slots['Year']['value']['interpretedValue'] if slots['Year'] else None
        filterDecision = slots['FilterDecision']['value']['interpretedValue'] if slots['FilterDecision'] else None
        
    
        
        if not filterDecision:
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': 'FilterDecision'
                    },
                    'intent': {
                        'name': intent,
                        'slots': slots,
                        'state': 'InProgress'
                    }
                }
            }
            
            
        print("year " + str(year))
        print("filter decision " + str(filterDecision))

            
        
        if not year:
            if filterDecision.lower() == 'yes':
                return {
                    'sessionState': {
                        'dialogAction': {
                            'type': 'ElicitSlot',
                            'slotToElicit': 'Year',
                        },
                        'intent': {
                            'name': intent,
                            'slots': slots,
                            'state': 'InProgress'
                        }
                    }
                }
            elif filterDecision.lower() == 'no':
                return fetch_movies(keyword, None)
        elif not year.isdigit():
            print("not valid")
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': 'Year'
                    },
                    'intent': {
                        'name': intent,
                        'slots': slots,
                        'state': 'InProgress'
                    }
                },
                'messages': [
                    {
                        'contentType': 'PlainText',
                        'content': 'Please enter a valid release year.'
                    }
                ]
            }
        else:
            return fetch_movies(keyword, year)