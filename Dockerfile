FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Railway/Render use PORT env variable
ENV PORT=5000
EXPOSE 5000

CMD ["python", "app.py"]
