# Create requirements.txt for backend dependencies
requirements_content = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
google-cloud-aiplatform==1.38.1
google-cloud-vision==3.4.5
google-cloud-speech==2.22.0
google-cloud-bigquery==3.13.0
google-cloud-storage==2.10.0
vertexai==1.38.0
python-dotenv==1.0.0
httpx==0.25.2
asyncio==3.4.3
'''

with open("requirements.txt", "w") as f:
    f.write(requirements_content)

print("✅ Created requirements.txt with all necessary dependencies")

# Create a Dockerfile for containerization
dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["uvicorn", "backend_main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
'''

with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

print("✅ Created Dockerfile for containerized deployment")

# Create environment configuration
env_content = '''# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# API Configuration
API_SECRET_KEY=your-super-secret-key
API_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gemini API Configuration
GEMINI_API_KEY=your-gemini-api-key
VERTEX_AI_PROJECT=your-vertex-ai-project
VERTEX_AI_LOCATION=us-central1

# Database Configuration (if using)
DATABASE_URL=postgresql://user:password@localhost/db_name

# External APIs
CRUNCHBASE_API_KEY=your-crunchbase-key
LINKEDIN_API_KEY=your-linkedin-key
'''

with open(".env.example", "w") as f:
    f.write(env_content)

print("✅ Created .env.example for environment configuration")