# Let's Get Coffee 

Los Angeles is an exciting place to live. Of course, there are beaches, museums, parks, and more. 
But when you're a student, the only place you truly have outside of campus is... well, you guessed it — coffee shops. 
With LA being LA, navigating all the different spots to study solo, hang out with a friend, or dive into a book can be overwhelming. 
That’s where Let's Get Coffee comes in!

# Explanatory Data Analysis: 

The data that was used was acquired from Google Places API. I collected the names, addrress,website,lat and long, rating, and reviews of 100 coffee shops. 
The data was really clean, my script would check for duplicats and drop them as I was grabbing the data from the API. I wanted to make sure the coffee shops are relatively close 
to each other thus I created a Map using Plotly. More EDA could be done on the ratings of the different coffee shops and if there is a relation between the reveiws and the location. 

# Methodolgy

I wanted my recommendation system to use customer reviews to build recommendation. The motivation of doing so was the detail and honesty that customers portray in the reviwews. 
It seemed fitted that the recommendation come from an unbaised source for example the coffee shop website. Google Places only allows for 5 reviews per place, thus I grouped the reviews together and used
them as the external knowledge, or documents, that I fed my RAG Pipline to leverage when outputiing recommendations. 

For the LLM, I used langchain_google_genai package where I called on the GoogleGenerativeAIEmbeddings function to acquire the embeddings of my texts and used Chroma DB to store the embeddings, 
and ChatGoogleGenerativeAI for my LLM. 

Once the model was done, I created a Flack App in order to be able to interact with my model and output the recommendations to the user. The curl command used locally was 

```
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question":"Where can I find good matcha?"}'
```
One the user ran that in the terminal, the flask app output a place with recommendations. One bug I kept running into was the embeddings showing up as a list of list. Thus I created a 
class in order to unlist the embeddings so that my model ran. The Issue might have arrised due to passing one document at a time, but this isse will be further analyzed at later stages of the project.

Once the model was running, I then containerized it using Docker, and pushed it to Docker Hub. I then used the Container URL to deploy it on Google Cloud Run to obtain a API endpoint my frontend could call upon. 

The API endpoint: 

```https://letsgetcoffee-image-508717259631.us-central1.run.app```

As for the frontend, I simply used Streamlit to creat an interactive Web App, and hosted it on Streamlit Cloud. 

# Results

Levergaing the little I know about color theory (ie. taking a graphic design class in undergrad for fun lol ), I created my web app Let's Get Coffee [https://lets-get-coffee.streamlit.app/].

This App is far from perfect. Some modification would be expanding the documents to include more information about the coffee shops rather than custome reviews, 
expanding my dataset to more than 100 coffee shops, outputting more than 1 recommendation, and better my prompt for the LLM to make it more conversational since it does not build on the previous messages. 

