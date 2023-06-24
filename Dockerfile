FROM python:3.8

RUN mkdir /code
WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Define as variáveis de ambiente HOST e PORT
ENV HOST=0.0.0.0
ENV PORT=5000

EXPOSE 5000

CMD [ "python", "app.py" ]
