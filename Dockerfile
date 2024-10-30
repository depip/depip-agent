FROM python:3.13

WORKDIR /depip_agent
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /depip_agent/app
CMD ["fastapi", "run", "app/main.py", "--port", "80"]