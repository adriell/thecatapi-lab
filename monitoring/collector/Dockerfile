FROM python:3.6
WORKDIR /usr/src/app
COPY collector.py ./
RUN pip install prometheus_client
ENTRYPOINT ["python"]
CMD ["collector.py"]
