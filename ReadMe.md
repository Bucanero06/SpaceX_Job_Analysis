# SpaceX Job Analysis

This project is a Python-based analysis of job listings from SpaceX. It uses web scraping and natural language
processing techniques to analyze the job descriptions and requirements, and then matches them with a given resume. The
project consists of two main Python scripts: `scrape_spacex_positions.py` and `analyze_spacex_applications.py`.

## Files

- `scrape_spacex_positions.py`: This script is responsible for scraping job listings from the SpaceX website. It
  collects information such as job title, discipline, location, and qualifications.

- `analyze_spacex_applications.py`: This script takes the scraped job listings and a given resume as input. It then
  performs a series of analyses to match the resume with the job listings. The analyses include vectorization of the
  text data, clustering of the job descriptions, calculation of similarity scores between the resume and job
  descriptions, and identification of relevant jobs in each cluster. The script also identifies the skills gap between
  the resume and job listings, and analyzes the impact of each section of the resume on job similarity.

## Usage

1. Run `scrape_spacex_positions.py` to scrape job listings from the SpaceX website. The scraped data will be saved in a
   CSV file.

2. Run `analyze_spacex_applications.py` with the scraped job listings and a given resume as input. The script will
   output the results of the analyses.

## Dependencies

This project uses the following Python libraries:

- `nltk`: For natural language processing tasks such as tokenization and stop word removal.
- `numpy` and `pandas`: For data manipulation and analysis.
- `sklearn`: For machine learning tasks such as vectorization and clustering.
- `matplotlib` and `plotly`: For data visualization.
- `selenium`: For web scraping (SpaceX's webside uses dynamic content that cannot be scraped with `requests`
  or `urllib`)

## Future Work

Future improvements to this project could include the addition of more advanced natural language processing techniques,
such as sentiment analysis or named entity recognition, to provide more detailed insights into the job listings and
resume. Additionally, the project could be extended to analyze job listings from other companies or industries.

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