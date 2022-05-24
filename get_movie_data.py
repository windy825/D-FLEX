import requests
import json



def get_genre(genre_ids):
    API_URL = 'https://api.themoviedb.org/3/genre/movie/list?api_key=95df29b4b9da9e2aca14c18f410253ee&language=ko-KR'
    
    data = requests.get(API_URL).json()['genres']

    answer = []
    for genre_id in genre_ids:
        for genre in data:
            if genre['id'] == genre_id:
                answer.append(genre['name'])
    return answer


def get_people(option, movie_id):
    API_URL = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=95df29b4b9da9e2aca14c18f410253ee&language=ko-KR"
    
    data = requests.get(API_URL).json()
    
    if option == 'director':
        target = data['crew']
        for crew in target:
            if crew['known_for_department'] == "Directing":
                return crew['name']

    elif option == 'actors':
        answer = []
        target = data['cast']
        for actor in target:
            answer.append([actor['name'], actor['popularity']])
        
        answer.sort(key= lambda x:-x[1])
        answer = [name for name, score in answer[:5]]
        return answer



def upcoming():
    answer = []

    cnt = 0
    for page in range(51,100):
        API_URL = f"https://api.themoviedb.org/3/movie/top_rated?api_key=95df29b4b9da9e2aca14c18f410253ee&language=ko-KR&page={page}"
        
        movies = requests.get(API_URL).json()
        cnt += len(movies)
        print(cnt)


        for movie in movies['results']:
            if movie['overview']:
                fields = {
                    'title' : movie['title'],
                    'overview' : movie['overview'],
                    'poster_path' : f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
                    'genres' : get_genre(movie['genre_ids']),
                    'popularity' : movie['vote_average'],
                    'director' : get_people('director', movie['id']),
                    'actors' : get_people('actors', movie['id']),
                    'release_date' : movie['release_date'],
                    'adult' : movie['adult']
                }

                if not fields['director']:
                    continue

                data = {
                    'pk' : movie['id'],
                    'model' : 'movies.movie',
                    'fields' : fields,
                }
                answer.append(data)

    
    with open('new_data2.json', 'w', encoding='utf-8') as w:
        json.dump(answer, w, indent='\t', ensure_ascii=False)


upcoming()