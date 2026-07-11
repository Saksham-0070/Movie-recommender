# 🎬 CineMatch – Movie Recommender System

Find your next favorite movie with AI-powered recommendations.

🔗 **Live Demo:** [Add your Streamlit link here]  
💻 **GitHub:** https://github.com/Saksham-0070/Movie-recommender

---

## 📖 Overview

CineMatch is a content-based movie recommendation system that suggests movies similar to a user's selected title using Natural Language Processing (NLP) and Machine Learning techniques.

Instead of relying on user ratings, the recommender analyzes movie metadata such as genres, cast, crew, keywords, and overview to identify similar movies.

Movie posters are fetched dynamically using the TMDB API, creating an interactive and visually appealing recommendation experience.

---

## ✨ Features

- 🎬 Content-Based Movie Recommendations
- 🤖 NLP-based similarity matching
- 🖼️ Live movie posters using TMDB API
- ⚡ Fast recommendation generation
- 🌐 Interactive Streamlit web interface
- 📱 Responsive and easy-to-use UI

---

## 🛠️ Tech Stack

### Programming Language
- Python

### Libraries
- Pandas
- NumPy
- Scikit-learn
- NLTK
- Streamlit
- Pickle

### APIs
- TMDB API

---

## 🧠 Machine Learning Pipeline

The recommendation engine follows these steps:

1. Load TMDB 5000 Movies Dataset
2. Clean and preprocess movie metadata
3. Combine important textual features:
   - Genres
   - Keywords
   - Cast
   - Crew
   - Overview
4. Tokenization
5. Stop-word removal
6. Stemming using PorterStemmer
7. Vectorization using CountVectorizer
8. Compute cosine similarity
9. Return Top-N similar movies

---

## 📂 Project Structure

```
Movie-recommender/
│
├── app.py
├── movies_dict.pkl
├── requirements.txt
├── README.md
└── screenshots/
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Saksham-0070/Movie-recommender.git
```

Go into the project directory

```bash
cd Movie-recommender
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

### Home Page

_Add screenshot here_

---

### Recommendations

_Add screenshot here_

---

## 📊 Dataset

- TMDB 5000 Movies Dataset
- Approximately 4,800 movies

Metadata used:

- Genres
- Keywords
- Cast
- Crew
- Overview

---

## 🔮 Future Improvements

- Hybrid recommendation system
- User authentication
- Collaborative filtering
- Personalized watchlists
- Trailer integration
- Genre-based filtering
- Movie search autocomplete

---

## 👨‍💻 Author

**Saksham Shendre**

- LinkedIn: https://linkedin.com/in/saksham-shendre
- GitHub: https://github.com/Saksham-0070

---

## ⭐ If you like this project

Please consider giving the repository a ⭐ on GitHub.
