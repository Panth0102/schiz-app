# Deployment Guide

## Quick Deploy to Render (Recommended)

1. **Create a Render account** at [render.com](https://render.com)

2. **Connect your GitHub repository**:
   - Push your code to GitHub
   - Connect your GitHub account to Render

3. **Create a new Web Service**:
   - Choose your repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Environment: Python 3

4. **Deploy**: Render will automatically deploy your app

## Deploy to Heroku

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## Deploy to Railway

1. **Create Railway account** at [railway.app](https://railway.app)
2. **Connect GitHub** and select your repository
3. **Deploy**: Railway will auto-detect Python and deploy

## Deploy to DigitalOcean App Platform

1. **Create DigitalOcean account**
2. **Go to App Platform** and create new app
3. **Connect GitHub** repository
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python app.py`

## Environment Variables (if needed)

For production, you may want to set:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key-here`

## Database Considerations

Your app uses SQLite which works for small deployments but consider upgrading to PostgreSQL for production use.