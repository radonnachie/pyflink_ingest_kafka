FROM python:3.8-slim
RUN pip3 install kafka-python==2.0.2
COPY run.py run.py
CMD [ "python", "-u", "run.py"]