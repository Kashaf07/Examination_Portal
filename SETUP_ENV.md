# Environment Setup for AI Question Generation

## Required Environment Variables

Create a `.env` file in the **root directory** with:

```
GROQ_API_KEY=your_groq_api_key_here
```

Create a `.env` file in the **backend directory** with:

```
GROQ_API_KEY=your_groq_api_key_here
```

## For Docker Deployment

The root `.env` file will be automatically loaded by docker-compose.

## For Local Development

The backend `.env` file will be loaded by the Flask application.

## Security Note

⚠️ **NEVER commit `.env` files to git!**

The `.gitignore` file is configured to exclude:
- `.env`
- `backend/.env`

## Getting Your Groq API Key

1. Visit https://console.groq.com/keys
2. Sign up or log in
3. Create a new API key
4. Copy and paste it into your `.env` files
