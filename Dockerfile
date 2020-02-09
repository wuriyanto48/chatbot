FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x download_corpus.py

RUN chmod +x train_bot.py

RUN chmod +x app.py

RUN ./download_corpus.py

RUN ./train_bot.py

EXPOSE 9000

CMD ["./app.py", "runserver"]