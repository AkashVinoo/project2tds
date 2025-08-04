# Data Analyst Agent API

A comprehensive data analysis API that can source, prepare, analyze, and visualize data using LLMs and various data processing tools.

## Features

- **Data Sourcing**: Web scraping from Wikipedia and other sources
- **Data Analysis**: Statistical analysis, correlations, and aggregations
- **Data Visualization**: Generate scatterplots with regression lines
- **Big Data Processing**: DuckDB integration for large datasets
- **RESTful API**: FastAPI-based endpoint for easy integration

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python run_data_analyst.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST `/api/`
Main endpoint for data analysis tasks.

**Request**: Upload a text file containing the analysis question.

**Response**: JSON array or object with analysis results.

### GET `/health`
Health check endpoint.

### GET `/`
Root endpoint with API information.

### GET `/docs`
Interactive API documentation (Swagger UI).

## Usage Examples

### 1. Wikipedia Analysis

Create a file `question.txt`:
```
Scrape the list of highest grossing films from Wikipedia. It is at the URL:
https://en.wikipedia.org/wiki/List_of_highest-grossing_films

Answer the following questions and respond with a JSON array of strings containing the answer.

1. How many $2 bn movies were released before 2000?
2. Which is the earliest film that grossed over $1.5 bn?
3. What's the correlation between the Rank and Peak?
4. Draw a scatterplot of Rank and Peak along with a dotted red regression line through it.
   Return as a base-64 encoded data URI, `"data:image/png;base64,iVBORw0KG..."` under 100,000 bytes.
```

Send request:
```bash
curl "http://localhost:8000/api/" -F "@question.txt"
```

### 2. Indian High Court Analysis

Create a file `question.txt`:
```
The Indian high court judgement dataset contains judgements from the Indian High Courts...

Answer the following questions and respond with a JSON object containing the answer.

{
  "Which high court disposed the most cases from 2019 - 2022?": "...",
  "What's the regression slope of the date_of_registration - decision_date by year in the court=33_10?": "...",
  "Plot the year and # of days of delay from the above question as a scatterplot with a regression line. Encode as a base64 data URI under 100,000 characters": "data:image/webp:base64,..."
}
```

Send request:
```bash
curl "http://localhost:8000/api/" -F "@question.txt"
```

## Testing

Run the test script to verify the API works:
```bash
python test_data_analyst.py
```

## Deployment

### Using ngrok (for public access)

1. Install ngrok:
```bash
# Download from https://ngrok.com/download
# or use package manager
```

2. Start the API server:
```bash
python run_data_analyst.py
```

3. In another terminal, expose the API:
```bash
ngrok http 8000
```

4. Use the ngrok URL as your API endpoint.

### Using other platforms

The API can be deployed to:
- Heroku
- Railway
- Render
- DigitalOcean
- AWS/GCP/Azure

## Architecture

- **FastAPI**: Web framework for the API
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Data visualization
- **DuckDB**: Big data processing
- **BeautifulSoup**: Web scraping
- **Requests**: HTTP client

## Response Format

### Wikipedia Analysis
Returns a JSON array: `[answer1, answer2, answer3, plot_data_uri]`

### Indian High Court Analysis
Returns a JSON object with question-answer pairs.

## Error Handling

The API includes comprehensive error handling:
- Invalid file uploads
- Network errors during scraping
- Data processing errors
- Visualization errors

All errors return appropriate HTTP status codes and error messages.

## Performance

- Response time: < 3 minutes for most queries
- Image size: < 100KB for visualizations
- Memory efficient: Uses streaming for large datasets

## Security

- CORS enabled for all origins (configurable)
- Input validation
- Error message sanitization
- Rate limiting (can be added)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License 