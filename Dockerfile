FROM python:3.13

WORKDIR /depip_agent
COPY ./requirements.txt /depip_agent/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /depip_agent/requirements.txt
COPY ./app /depip_agent/app
CMD ["fastapi", "run", "app/main.py"]