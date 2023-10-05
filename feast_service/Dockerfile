FROM python:3.8

WORKDIR /work/

RUN pip install psycopg2 redis 
RUN pip install redis 
RUN pip install feast

COPY ./feature_store/ /work/feature_store
RUN cd /work/feature_store && python generate_historical.py

COPY . .

EXPOSE 8888
CMD ["/bin/bash", "-c", "cd /work/ && cd feature_store && feast apply && echo Applied. Serving... && feast serve --host 0.0.0.0 --port 8888"]