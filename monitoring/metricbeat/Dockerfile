FROM docker.elastic.co/beats/metricbeat:6.5.2

COPY metricbeat.yml /usr/share/metricbeat/metricbeat.yml

USER root

RUN mkdir /var/log/metricbeat \
    && chown root /usr/share/metricbeat/metricbeat.yml \
    && chmod 777 -R /usr/share/metricbeat/ \
    && chmod go-w /usr/share/metricbeat/metricbeat.yml \
    && chown root /var/log/metricbeat
