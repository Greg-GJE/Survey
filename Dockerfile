FROM nikolaik/python-nodejs:latest

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN npm install
EXPOSE 8000/tcp
CMD npm start

