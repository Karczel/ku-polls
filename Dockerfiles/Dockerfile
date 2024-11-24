FROM python:3-alpine
# An argument needed to be passed
ARG SECRET_KEY
ARG ALLOWED_HOSTS=127.0.0.1,localhost

WORKDIR /app/polls

# Set needed settings
ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=True
ENV TIMEZONE=UTC
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS:-127.0.0.1,localhost}

# Test for secret key
RUN if [ -z "$SECRET_KEY" ]; then echo "No secret key specified in build-arg"; exit 1; fi

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./entrypoint.sh

EXPOSE 8000

# Run application
CMD ["./entrypoint.sh"]