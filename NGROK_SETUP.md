# Setting up ngrok for Continuous Deployment

## 🚀 Quick Setup

### 1. Download ngrok
- Go to https://ngrok.com/download
- Download the Windows version
- Extract the zip file to a folder (e.g., `C:\ngrok`)

### 2. Add ngrok to PATH
- Copy the ngrok.exe to a folder in your PATH, or
- Add the ngrok folder to your system PATH

### 3. Sign up for free account
- Go to https://dashboard.ngrok.com/signup
- Create a free account
- Get your authtoken from the dashboard

### 4. Authenticate ngrok
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

## 🌐 Start the Tunnel

### Option 1: Manual Setup
1. **Start the API server** (in one terminal):
   ```bash
   python data_analyst_agent.py
   ```

2. **Start ngrok tunnel** (in another terminal):
   ```bash
   ngrok http 8000
   ```

3. **Use the provided URL** for evaluation

### Option 2: Automated Setup
```bash
python deploy_with_ngrok.py
```

## 📡 Public URL

Once ngrok is running, you'll get a URL like:
```
https://abc123.ngrok.io
```

Your API endpoints will be:
- **Main API**: `https://abc123.ngrok.io/api/`
- **Health Check**: `https://abc123.ngrok.io/health`
- **API Docs**: `https://abc123.ngrok.io/docs`

## 🔄 Continuous Operation

The ngrok tunnel will run continuously until you stop it. Keep the terminal window open.

## 📝 Usage Example

```bash
curl "https://abc123.ngrok.io/api/" -F "@question.txt"
```

## ⚠️ Important Notes

1. **Keep ngrok running** during evaluation
2. **Free tier limitations**:
   - 1 tunnel at a time
   - Random URLs each time
   - Rate limits
3. **For production**: Consider paid ngrok or other hosting services

## 🛠️ Troubleshooting

### Port already in use
```bash
# Kill existing processes
taskkill /F /IM python.exe
taskkill /F /IM ngrok.exe
```

### ngrok not found
- Ensure ngrok.exe is in your PATH
- Or run from the ngrok directory

### Authentication error
- Check your authtoken
- Run: `ngrok config add-authtoken YOUR_TOKEN` 