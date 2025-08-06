# Data Analyst Agent API - Public Usage Guide

## 🌐 Public API Access

Your Data Analyst Agent API is now **publicly accessible** and accepts requests from **anyone at any time**!

### 📡 Public URL
```
https://9957e021ce3f.ngrok-free.app
```

## 🚀 Quick Start

### 1. Health Check
```bash
curl -H "ngrok-skip-browser-warning: true" \
  "https://9957e021ce3f.ngrok-free.app/health"
```

### 2. API Info
```bash
curl -H "ngrok-skip-browser-warning: true" \
  "https://9957e021ce3f.ngrok-free.app/"
```

### 3. Data Analysis
```bash
curl -H "ngrok-skip-browser-warning: true" \
  "https://9957e021ce3f.ngrok-free.app/api/" \
  -F "file=@your_question.txt"
```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/api/` | POST | Main data analysis endpoint |
| `/docs` | GET | API documentation |

## 🔧 How to Use

### Step 1: Create a Question File
Create a text file (e.g., `question.txt`) with your analysis question:

```
What is the correlation between sales and profit in the data?
```

### Step 2: Send Request
```bash
curl -H "ngrok-skip-browser-warning: true" \
  "https://9957e021ce3f.ngrok-free.app/api/" \
  -F "file=@question.txt"
```

### Step 3: Get Results
The API will return JSON with analysis results.

## 🌍 Cross-Platform Usage

### Python
```python
import requests

url = "https://9957e021ce3f.ngrok-free.app/api/"
headers = {"ngrok-skip-browser-warning": "true"}

with open("question.txt", "rb") as f:
    files = {"file": ("question.txt", f, "text/plain")}
    response = requests.post(url, files=files, headers=headers)
    print(response.json())
```

### JavaScript/Node.js
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('question.txt'));

axios.post('https://9957e021ce3f.ngrok-free.app/api/', form, {
  headers: {
    ...form.getHeaders(),
    'ngrok-skip-browser-warning': 'true'
  }
})
.then(response => console.log(response.data))
.catch(error => console.error(error));
```

### PowerShell
```powershell
$form = @{file = Get-Item "question.txt"}
Invoke-RestMethod -Uri "https://9957e021ce3f.ngrok-free.app/api/" -Method POST -Form $form -Headers @{"ngrok-skip-browser-warning"="true"}
```

## 📊 Supported Analysis Types

1. **Web Scraping Analysis**
   - Extract data from URLs
   - Analyze tables and structured data

2. **DuckDB/S3 Analysis**
   - Query large datasets
   - SQL-based analysis

3. **Statistical Analysis**
   - Correlation analysis
   - Descriptive statistics
   - Regression analysis

4. **Data Visualization**
   - Charts and graphs
   - Scatter plots
   - Time series analysis

## ⚠️ Important Notes

1. **ngrok Warning**: The free tier shows a warning page - this is normal
2. **Header Required**: Always include `ngrok-skip-browser-warning: true` header
3. **File Upload**: Send questions as text files via POST request
4. **Response Format**: All responses are in JSON format

## 🔄 Continuous Availability

- ✅ **24/7 Access**: API runs continuously
- ✅ **Public Access**: Anyone can use it
- ✅ **No Authentication**: No API keys required
- ✅ **CORS Enabled**: Works from any domain

## 🛠️ Troubleshooting

### Common Issues

1. **ngrok Warning Page**
   - Solution: Add the required header
   - Header: `ngrok-skip-browser-warning: true`

2. **Connection Timeout**
   - Check if the tunnel is still active
   - Restart ngrok if needed

3. **File Upload Error**
   - Ensure file is text format
   - Check file size (should be small)

### Test Your Connection
```bash
# Test health endpoint
curl -H "ngrok-skip-browser-warning: true" \
  "https://9957e021ce3f.ngrok-free.app/health"
```

## 📞 Support

The API is designed to be self-service. If you encounter issues:

1. Check the health endpoint
2. Verify your request format
3. Ensure you're using the correct headers

---

**🎉 Your API is now publicly accessible and ready to serve requests from anyone, anywhere, at any time!** 