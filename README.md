# Data Analyst Agent

A comprehensive API that uses LLMs to source, prepare, analyze, and visualize any data. This agent can handle web scraping, data processing, statistical analysis, and visualization tasks.

## Features

- **Web Scraping**: Automatically scrape data from Wikipedia and other websites
- **Data Analysis**: Perform statistical analysis including correlations, regressions, and aggregations
- **Visualization**: Generate scatterplots, charts, and graphs with regression lines
- **DuckDB Integration**: Query large datasets from S3 using DuckDB
- **LLM Integration**: Use OpenAI GPT-4 or Anthropic Claude for advanced analysis
- **File Processing**: Handle CSV, Excel, JSON, and other data formats
- **Real-time Processing**: Complete analysis within 3 minutes

## API Endpoint

The main endpoint accepts POST requests with the following structure:

```
POST https://your-domain.com/api/
```

### Request Format

- `questions.txt` (required): Contains the analysis questions
- Additional files (optional): Data files, images, etc.

### Example Request

```bash
curl "https://your-domain.com/api/" \
  -F "questions=@questions.txt" \
  -F "data.csv=@data.csv" \
  -F "image.png=@image.png"
```

### Response Format

Returns a JSON array with answers to the questions in order.

## Supported Analysis Types

### 1. Wikipedia Data Analysis

Scrape and analyze data from Wikipedia tables:

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

### 2. Large Dataset Analysis (DuckDB/S3)

Query and analyze large datasets stored in S3:

```
The Indian high court judgement dataset contains judgements from the Indian High Courts...

Answer the following questions and respond with a JSON object containing the answer.

{
  "Which high court disposed the most cases from 2019 - 2022?": "...",
  "What's the regression slope of the date_of_registration - decision_date by year in the court=33_10?": "...",
  "Plot the year and # of days of delay from the above question as a scatterplot with a regression line. Encode as a base64 data URI under 100,000 characters": "data:image/webp:base64,..."
}
```

### 3. Generic Data Analysis

Analyze uploaded data files with custom questions.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd data-analyst-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

## Usage

### Quick Start

1. Run the deployment script:
```bash
python deploy.py
```

2. The script will:
   - Check dependencies
   - Start the server
   - Test the API
   - Optionally set up ngrok for public access

### Manual Start

1. Start the server:
```bash
python data_analyst_agent.py
```

2. The server will be available at `http://localhost:8000`

3. For public access, use ngrok:
```bash
ngrok http 8000
```

### API Testing

Test the API with the provided test script:

```bash
python test_data_analyst.py
```

## Project Structure

```
data-analyst-agent/
├── data_analyst_agent.py    # Main application
├── main.py                  # Entry point
├── deploy.py               # Deployment script
├── requirements.txt        # Dependencies
├── README.md              # This file
├── test_data_analyst.py   # Test script
└── api/                   # API directory
    └── index.py           # API endpoints
```

## Dependencies

- **FastAPI**: Web framework
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Matplotlib/Seaborn**: Data visualization
- **BeautifulSoup**: Web scraping
- **Selenium**: Dynamic web scraping
- **DuckDB**: Database queries
- **OpenAI/Anthropic**: LLM integration
- **Requests/httpx**: HTTP client

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for GPT-4 access
- `ANTHROPIC_API_KEY`: Anthropic API key for Claude access

### Server Configuration

The server runs on port 8000 by default. You can modify this in `data_analyst_agent.py`.

## API Endpoints

- `GET /health`: Health check
- `POST /api/`: Main analysis endpoint

## Error Handling

The API includes comprehensive error handling:
- Timeout protection (3-minute limit)
- Graceful handling of missing data
- Detailed error messages
- Fallback responses when LLMs are unavailable

## Performance

- **Response Time**: Typically completes within 30-120 seconds
- **Memory Usage**: Optimized for large datasets
- **Concurrent Requests**: Supports multiple simultaneous requests
- **Timeout**: 3-minute maximum processing time

## Security

- CORS enabled for cross-origin requests
- Input validation and sanitization
- Secure file handling
- No sensitive data logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open an issue on the GitHub repository. 