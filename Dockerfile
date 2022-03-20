FROM python:3.8-alpine

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV ACCESS_TOKEN_FEEDLY=""
ENV USER_ID=""
ENV DATA_ARTICLES_CATEGORY=""
ENV CONSUMER_KEY=""
ENV CONSUMER_SECRET=""
ENV ACCESS_TOKEN=""
ENV ACCESS_TOKEN_SECRET=""
ENV EMAIL_ENABLED=True
ENV EMAIL_SERVER="smtp-mail.outlook.com"
ENV EMAIL_PORT=587
ENV EMAIL_SENDER="email@domain.com"
ENV EMAIL_SENDER_PASS=""
ENV EMAIL_RECEIVER="email@domain.com"

# Install dependencies:
COPY . /data_articles/
RUN pip install -r ./data_articles/requirements.txt
RUN apk update
RUN apk add --upgrade sqlite

# Run the application:
WORKDIR "/data_articles"
CMD ["python3", "-u","main.py"]
