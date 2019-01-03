Events Marketplace
==================

An open source **Events Marketplace** built with Django.

Requirements
************

- Python 3.6+
- Django 2.0+
- Elasticsearch 2.4 + Java 8 (install through openjdk-8-jre-headless)
- Google Maps API key

Tests
*****

Elasticsearch should run for tests to pass::

    $ cd elasticsearch-2.4.6/bin
    $ ./elasticsearch
    $ curl -X GET 'http://localhost:9200'
