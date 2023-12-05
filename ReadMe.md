# SpaceX Job Analysis

This project is a Python-based analysis of job listings from SpaceX. It uses web scraping and natural language
processing techniques to analyze the job descriptions and requirements and then matches them with a given resume. The
project consists of two main Python scripts: `scrape_spacex_positions.py` and `analyze_spacex_applications.py`.

## Files

- `scrape_spacex_positions.py`: This script is responsible for scraping job listings from the SpaceX website. It
  collects information such as job title, discipline, location, and qualifications.

- `analyze_spacex_applications.py`: This script takes the scraped job listings and a given resume as input. It then
  performs a series of analyses to match the resume with the job listings. The analyses include vectorization of the
  text data, clustering of the job descriptions, calculation of similarity scores between the resume and job
  descriptions, and identification of relevant jobs in each cluster. The script also identifies the skills gap between
  the resume and job listings and analyzes the impact of each section of the resume on job similarity.

## Installation

To install the dependencies for this project, you can follow these steps:

1. Install Poetry if you haven't already. You can do this by running the following command in your terminal:

```bash
curl -sSL https://install.python-poetry.org | python -
```

2. Navigate to your project directory that contains the `pyproject.toml` and `poetry.lock` files.

3. Run the following command to install the dependencies:

```bash
poetry install
```

This command will read the `pyproject.toml` file to identify the dependencies and their versions, and then install them. The `poetry.lock` file ensures that the exact same versions of the dependencies are installed if the project is set up in a different environment.

## Dependencies

This project uses the following Python libraries:

- `nltk`: For natural language processing tasks such as tokenization and stop word removal.
- `numpy` and `pandas`: For data manipulation and analysis.
- `sklearn`: For machine learning tasks such as vectorization and clustering.
- `matplotlib` and `plotly`: For data visualization.
- `selenium`: For web scraping (SpaceX's website uses dynamic content that cannot be scraped with `requests`
  or `urllib`)

## Future Work

Future improvements to this project could include the addition of more advanced natural language processing techniques,
such as sentiment analysis or named entity recognition, to provide more detailed insights into job listings and
resumes. Additionally, the project could be extended to analyze job listings from other companies or industries.

# P.S.
If you are a representative of SpaceX ...  here is my cover letter to you <3

```
Hi, my name is Ruben and I love learning and the art of learning. I want to learn from the brightest and most inspiring company I believe of this generation. My background is filled with molecular biology and have for a long time been deeply in love with chemistry. In search of deeper truths and to feed my curiosity I joined a brilliant UCF's CREOL professor Luca Argenti and combined our common love for physics and structural biology to expand his AttoSecond TRAnsitions (ASTRA) codebase to include studying electronic charge migration and its reconstruction from experimental 2D spectra data. Two years ago I began my first legally structured research and development venture to enhance my problem-solving and practical skills. From that point on I have continued to fund my passion research, I've been a strong father and husband. I have kept my head high, and I've learned when to put my head down and get things done, at this stage in my life I'm ready to go back and finish my Ph.D. in Physics but do not have the money to, I crave the next chapter in contributing to all that is around me. If you would consider me as a candidate and view my skills and positions as something to be molded over time, there is nothing I wouldn't do for a company that is giving me the future I have dreamed for my daughter. Thank you for your time and for everything you guys represent for so many. 

Best Wishes,
Ruben Alejandro Fernandez Carbon
```
