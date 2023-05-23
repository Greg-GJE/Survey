FROM nikolaik/python-nodejs:latest

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN npm install
CMD ["node", "index.js"]
EXPOSE 80/tcp
