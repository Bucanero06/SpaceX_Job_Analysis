from collections import Counter
from pprint import pprint

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Example data
resume = open("Ruben_FernandezCarbon_Resume_2023.txt").read()
resume_json = pd.read_json("split_resume_sections.json", typ='series')

df = pd.read_csv("spacex_jobs_.csv")
df = df.fillna('')
#
job_listings = []
for index, row in df.iterrows():

    job_listings.append(
        row['RESPONSIBILITIES'] + row['BASIC QUALIFICATIONS'] +
        row['PREFERRED SKILLS AND EXPERIENCE'] + row['ADDITIONAL REQUIREMENTS'] +
        row['COMPENSATION AND BENEFITS']
    )



# Vectorization
vectorizer = TfidfVectorizer()
all_vectors = vectorizer.fit_transform([resume] + job_listings).toarray()

# Clustering Job Descriptions
job_vectors = all_vectors[1:]  # Exclude resume
kmeans = KMeans(n_clusters=20)  # Number of clusters can be adjusted
kmeans.fit(job_vectors)
job_clusters = kmeans.labels_

# Calculate Similarity
resume_vector = all_vectors[0]
similarities = cosine_similarity([resume_vector], job_vectors).flatten()

# Aggregate Similarity Scores by Cluster
cluster_similarity = {}
for i, cluster in enumerate(job_clusters):
    cluster_similarity.setdefault(cluster, []).append(similarities[i])

# Average Similarity per Cluster
average_similarity = {cluster: np.mean(scores) for cluster, scores in cluster_similarity.items()}

# Rank Clusters
ranked_clusters = sorted(average_similarity, key=average_similarity.get, reverse=True)

# Identify Relevant Jobs in Clusters
cluster_job_mapping = {}
for cluster_id in ranked_clusters:
    jobs_in_cluster = np.where(job_clusters == cluster_id)[0]
    sorted_jobs = sorted(jobs_in_cluster, key=lambda x: similarities[x], reverse=True)
    cluster_job_mapping[cluster_id] = sorted_jobs

    jobs_in_cluster = df.iloc[cluster_job_mapping[cluster_id]]

    # Job Title
    job_titles = jobs_in_cluster['JOB TITLE']
    title_freq = Counter(job_titles)
    most_common_titles = title_freq.most_common(10)
    print(f"Cluster {cluster_id} common titles: {most_common_titles}")

    # Discipline
    disciplines = jobs_in_cluster['DISCIPLINE']
    discipline_freq = Counter(disciplines)
    most_common_disciplines = discipline_freq.most_common(10)
    print(f"Cluster {cluster_id} common disciplines: {most_common_disciplines}")

    # Location
    locations = jobs_in_cluster['LOCATION']
    location_freq = Counter(locations)
    most_common_locations = location_freq.most_common(10)
    print(f"Cluster {cluster_id} common locations: {most_common_locations}")

    # Qualification
    all_text = ' '.join(jobs_in_cluster['Qualifications']).lower()
    words = nltk.word_tokenize(all_text)
    words = [word for word in words if word.isalpha() and word not in stop_words]
    qualification_freq = Counter(words)
    most_common_qualifications = qualification_freq.most_common(10)
    print(f"Cluster {cluster_id} common words: {most_common_qualifications}")

    print()


# Interactive Visualization
import plotly.graph_objects as go

# Prepare data for Plotly
viz_data = pd.DataFrame({
    'Cluster': job_clusters,
    'Similarity': similarities,
    'Job Title': df['JOB TITLE']
})
import plotly.express as px

fig = px.scatter(viz_data, x="Cluster", y="Similarity", color="Similarity", hover_data=['Job Title'])
fig.show()

for i, cluster in enumerate(ranked_clusters):
    if i == 1:  # todo remove, rn it prints too much
        break
    # Filter data for the current cluster
    cluster_data = viz_data[viz_data['Cluster'] == cluster]

    # Convert the dictionary to lists
    job_titles = list(cluster_data['Job Title'])
    resume_similarity = list(cluster_data['Similarity'])


    # Create an interactive bar plot
    fig = go.Figure(data=[go.Bar(x=resume_similarity, y=job_titles, orientation='h')])
    fig.update_layout(title=f'Resume - Job Similarity for Cluster {cluster}', xaxis_title='Similarity',
                      yaxis_title='Resume Section', yaxis={'categoryorder': 'total ascending'})
    fig.show()


def extract_skills(text):
    return set(nltk.word_tokenize(text.lower()))


resume_skills = extract_skills(resume)
all_job_skills = set().union(*[extract_skills(job) for job in job_listings])
skill_gap = all_job_skills - resume_skills
print("\nSkills to consider adding to your resume:", skill_gap)

# Resume Section Impact Analysis
section_impact = {}
for section, content in resume_json.items():
    if isinstance(content, str):  # For single string sections
        section_vector = vectorizer.transform([content]).toarray()
        section_similarity = cosine_similarity(section_vector, job_vectors).flatten()
        section_impact[section] = np.mean(section_similarity)
    elif isinstance(content, list):  # For list-based sections like Education, Research Experience
        for item in content:
            if isinstance(item, dict):
                for subitem in item.values():
                    if isinstance(subitem, str):
                        item_vector = vectorizer.transform([subitem]).toarray()
                        item_similarity = cosine_similarity(item_vector, job_vectors).flatten()
                        section_impact[f"{section}: {subitem}"] = np.mean(item_similarity)
                    elif isinstance(subitem, list):
                        for elem in subitem:
                            elem_vector = vectorizer.transform([elem]).toarray()
                            elem_similarity = cosine_similarity(elem_vector, job_vectors).flatten()
                            section_impact[f"{section}: {elem}"] = np.mean(elem_similarity)
            else:
                item_vector = vectorizer.transform([item]).toarray()
                item_similarity = cosine_similarity(item_vector, job_vectors).flatten()
                section_impact[f"{section}: {item}"] = np.mean(item_similarity)

pprint("Resume Section Impact:")
pprint(section_impact)

# Plot Impact
sections = list(section_impact.keys())
impacts = list(section_impact.values())

# Create an interactive bar plot
fig = go.Figure(data=[go.Bar(x=impacts, y=sections, orientation='h')])
fig.update_layout(title='Impact of Resume Section on Job Similarity', xaxis_title='Impact',
                  yaxis_title='Resume Section', yaxis={'categoryorder': 'total ascending'})
fig.show()

