FROM localstack/localstack:latest
COPY code/ /code/
COPY requirements.txt /code/requirements.txt
WORKDIR /code
RUN  pip install -r requirements.txt
RUN python --version
RUN pwd
RUN ls -la
RUN chmod +x dynamodb.py

#RUN ./code/dynamodb.py
