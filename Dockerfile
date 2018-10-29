FROM python:3
RUN mkdir /app
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD [ "python", "/app/quietcool/__init__.py" ]