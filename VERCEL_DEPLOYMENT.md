# Vercel Deployment Guide for Data Analyst Agent

This guide will help you deploy the Data Analyst Agent to Vercel with a 3-minute timeout configuration.

## ⚠️ Important Notes

**Vercel has limitations for this type of application:**
- Default timeout is 10 seconds for serverless functions
- We've configured it for 300 seconds (5 minutes) maximum
- Cold starts may affect performance
- Large dependencies may cause deployment issues

## 🚀 Quick Deployment

### Option 1: Automated Deployment

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Run the deployment script**:
   ```bash
   python deploy_vercel.py
   ```

### Option 2: Manual Deployment

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy the project**:
   ```bash
   vercel --prod
   ```

## 📁 Project Structure

```
data-analyst-agent/
├── api/
│   └── index.py          # Main FastAPI application
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── deploy_vercel.py      # Deployment script
└── README.md            # Project documentation
```

## ⚙️ Configuration Details

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/health",
      "dest": "/api/index.py"
    }
  ],
  "functions": {
    "api/index.py": {
      "maxDuration": 300
    }
  }
}
```

### Key Configuration Points:
- **maxDuration**: Set to 300 seconds (5 minutes) to handle the 3-minute requirement
- **Routes**: Configured to handle both `/api/` and `/health` endpoints
- **Build**: Uses Vercel's Python runtime

## 🔧 Optimizations for Vercel

### 1. Reduced Dependencies
- Removed heavy dependencies like Selenium, DuckDB
- Kept only essential packages for core functionality
- Optimized for faster cold starts

### 2. Performance Optimizations
- Shorter HTTP timeouts (20-25 seconds)
- Limited table parsing (first 3 tables only)
- Smaller plot sizes and lower DPI
- Efficient data processing

### 3. Error Handling
- Graceful timeout handling
- Comprehensive error messages
- Fallback responses for failed operations

## 🧪 Testing Your Deployment

### Health Check
```bash
curl https://your-app.vercel.app/health
```

### API Test
```bash
curl -X POST https://your-app.vercel.app/api/ \
  -F "questions=@test_question.txt"
```

### Sample Test Question
Create a file `test_question.txt`:
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

## 📊 Monitoring

### Vercel Dashboard
- Monitor function execution times
- Check for timeout errors
- View deployment logs

### Function Logs
```bash
vercel logs
```

## 🚨 Troubleshooting

### Common Issues:

1. **Timeout Errors**
   - Check if requests are taking too long
   - Optimize data processing
   - Consider reducing data size

2. **Cold Start Delays**
   - First request may be slow
   - Subsequent requests should be faster
   - Consider keeping function warm

3. **Dependency Issues**
   - Some packages may not work on Vercel
   - Check Vercel's Python runtime compatibility
   - Use alternative packages if needed

4. **Memory Issues**
   - Large datasets may cause memory problems
   - Optimize data processing
   - Consider streaming for large files

### Debug Commands:
```bash
# Check deployment status
vercel ls

# View function logs
vercel logs

# Redeploy
vercel --prod

# Remove deployment
vercel remove
```

## 🔄 Alternative Deployment Options

If Vercel doesn't meet your needs, consider:

1. **Railway** - Better for long-running processes
2. **Render** - Good Python support, longer timeouts
3. **DigitalOcean App Platform** - More control, longer timeouts
4. **AWS Lambda** - Configurable timeouts up to 15 minutes

## 📋 Final Checklist

- [ ] Vercel CLI installed
- [ ] Project deployed successfully
- [ ] Health endpoint working
- [ ] API endpoint responding within 3 minutes
- [ ] Test with sample data
- [ ] Monitor for timeout errors
- [ ] Ready for submission

## 🎯 Submission

Once deployed, your API endpoint will be:
```
https://your-app-name.vercel.app/api/
```

Use this URL for your TDS Data Analyst Agent submission.
