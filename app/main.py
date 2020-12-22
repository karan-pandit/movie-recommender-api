import uvicorn ##ASGI
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import os
import pickle
import pandas as pd
#from recommend import get_recommendations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)



df = pd.read_pickle('data.pickle')

file = open("cosine.pickle","rb")
cosine_sim = pickle.load(file)

#Construct a reverse map of indices and movie titles
indices = pd.Series(df.index, index=df['title'])

def get_recommendations(title):
    try:
        # Get the index of the movie that matches the title
        idx = indices[title.lower()]

        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        return df['title'].iloc[movie_indices]

    except:
        return None

@app.get('/')
def index():
    return RedirectResponse(url="/docs/")

@app.get('/{title}')
async def recommend(title: str):
    return get_recommendations(title)

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=int(os.environ.get('PORT',8080)))
#uvicorn main:app --reload