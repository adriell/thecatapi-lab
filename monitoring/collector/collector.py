import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily, SummaryMetricFamily, HistogramMetricFamily
from prometheus_client import start_http_server


class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        g = GaugeMetricFamily("MemoryUsage", 'Help text', labels=['instance'])
        g.add_metric(["api"], 20)
        yield g

        c = CounterMetricFamily("HttpRequests", 'Help text', labels=['http_request'])
        c.add_metric(["api"], 1000)
        yield c

        h = HistogramMetricFamily('request_latency_seconds','Description of histogram', labels=['request_latency'])
        h.add_metric(["api"], buckets=[('0', 1), ('+Inf', 2)], sum_value=3)
        yield h

        #s = SummaryMetricFamily('request_latency_seconds', 'Description of summary')
        #s.add_metric(["api"], 4.7)
        #yield s  


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)