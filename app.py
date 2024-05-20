import pickle
import streamlit as st
import pandas as pd
import requests
import random
import gdown

# CSS markdown for background
def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url('https://media.licdn.com/dms/image/D5612AQGy6sM0SJAdxg/article-cover_image-shrink_720_1280/0/1693150322893?e=2147483647&v=beta&t=tmyCkhGahTKcBOOftyXZLhkLjtUIkqio94iGE3Y670E');
             background-size: cover;
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

add_bg_from_url()

# CONTACT US    
def contact_us():
    st.title("Contact Us Page")
    st.write("Please fill out the form below to provide feedback:")
    # Create a form for feedback
    name = st.text_input("Name:")
    email = st.text_input("Email:")
    feedback = st.text_area("Feedback:")
    if st.button("Submit"):
        # Save the feedback to a CSV file
        feedback_data = pd.DataFrame({"Name": [name], "Email": [email], "Feedback": [feedback]})
        feedback_data.to_csv("feedback.csv", mode='a', header=False, index=False)
        st.success("Thank you for your feedback!")

# ABOUT US
def about_us():     
    st.title("About Us")
    st.markdown("""
    ## Welcome to Film Finder
    Your ultimate destination for personalized movie recommendations. At Film Finder, we believe that every movie lover deserves to find the perfect film to match their unique tastes and preferences. Our advanced recommendation system leverages cutting-edge technology and the power of data to bring you tailored suggestions that enhance your viewing experience.

    ### Created By
    Film Finder was created by Rounak Bhowmick,Arpan Modak,Koushik Ghosh, Snigdha Sahoo , some passionate movie enthusiast and tech expert, dedicated to making movie recommendations more personalized and enjoyable for everyone.

    """, unsafe_allow_html=True)
    
# Function to download a file from Google Drive
def download_file_from_google_drive(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, destination, quiet=False)

# ID of the similarity.pkl file on Google Drive
similarity_file_id = '10SDRapIZIY27BHumhfLx2FgtRgVAy8td'

# Download the similarity.pkl file
download_file_from_google_drive(similarity_file_id, 'similarity.pkl')

# LOAD THE PICKLE FILES
movies_dict = pickle.load(open('movie_dict.pkl','rb'))   # Loading the dumped dictionary
movies = pd.DataFrame(movies_dict)  # Creating a dataframe
similarity = pickle.load(open('similarity.pkl','rb'))

# FETCH POSTERS
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)   # API
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# RECOMMEND
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    top_10_similar = distances[1:10]    # Take top 10 movies from distances
    select_similar = random.sample(top_10_similar, 5)    # Recommend 5 movies randomly from that.
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in select_similar:
        movie_id = movies.iloc[i[0]].movie_id   # To fetch posters
        poster_url = fetch_poster(movie_id)    # Fetch poster URL
        if poster_url:
            recommended_movie_posters.append(poster_url)
            recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# LAYOUT
def main():     
    st.markdown("<h2 <b  style='text-align: center; font-family: Times New Roman, Times, serif; '> FILM FINDER </b></h2>", unsafe_allow_html=True)
    st.sidebar.title("Navigation")
    st.sidebar.markdown('<div class="st-bx">', unsafe_allow_html=True)
    page = st.sidebar.radio("Go to", ["Home","Contact Us", "About Us"])
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    if page == "Home":
        selected_movie = st.selectbox('Select your movie',movies['title'].values)
        if st.button('Recommend'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
            col1, col2, col3, col4, col5 = st.columns(5)
            for i, (name, poster_url) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
                with locals()[f"col{i+1}"]:
                    st.text(name)
                    st.image(poster_url, caption=name, use_column_width=True)

    elif page == "Contact Us":
        contact_us()

    elif page == "About Us":
        about_us()
    
if __name__ == "__main__":
    main()
