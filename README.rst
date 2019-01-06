Events Marketplace
==================

An open source **Events Marketplace** built with Django.

Requirements
************

- Python 3.6+
- Django 2.0+
- Elasticsearch 2.4 + Java 8 (install through openjdk-8-jre-headless)
- Google Maps API key

Build index after adding the instances of indexed model::

    $ python manage.py rebuild_index

Tests
*****

Elasticsearch should run for tests to pass::

    Run Elasticsearch
    $ cd elasticsearch-2.4.6/bin
    $ ./elasticsearch

    Check that Elasticsearch is running
    $ curl -X GET 'http://localhost:9200'

    Check the content of the index
    $ curl -X GET 'http://localhost:9200/haystack/_search?pretty'
