# Tripadvisor Scraper

## Overview

Tripadvisor Scraper is a Python-based web scraping project designed to extract detailed information from Tripadvisor listings. This project specifically focuses on scraping data from Michelin Star restaurants, with an example using Gallaghers Steakhouse in New York City.

You can find the step-by-step here in [Rayobyte community](https://rayobyte.com/community/scraping-project/extract-restaurant-details-customer-reviews-and-ratings-from-tripadvisor-using-python/)

You can watch the [video here](https://youtu.be/kFs9YkxGvZE)

## Features

- Scrapes comprehensive restaurant details including:
  - Restaurant Name
  - Price Level
  - Cuisine Type
  - Total Rating
  - Total Reviews
  - Ranking
  - City
  - Food Rating
  - Service Rating
  - Value Rating
  - Atmosphere Rating
  - Address
  - Phone Number
- Extracts customer reviews with:
  - Review Title
  - Review Details
  - Customer Type
  - Written Date
- Outputs data in a structured format for easy analysis.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/ainacodes/tripadvisor_scraper.git
   ```

2. Navigate to the project directory:
   ```bash
   cd tripadvisor_scraper
   ```

### Code functionality
- `restaurant_review_details.py`: Scrape the custmomer reviews from the first page only
- `restaurant_review_details_pagination.py`: Scrape all the reviews from all pages.
- `restaurant_review_details_pagination_proxy.py`: Implemeting proxy rotation by rotating the proxy for every page scrape.
    - Please include a new file name `proxy.txt` that includes a list of proxy in this format `username:password@host:port`

## Contributing

Contributions are welcome! If you have suggestions for improvements or find bugs, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any inquiries, please email me at noraina.nordin16@gmail.com
