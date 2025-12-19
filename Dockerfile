FROM python:3.13.7
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "run:app"]
EXPOSE 8000
