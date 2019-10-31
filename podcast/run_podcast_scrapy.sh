#!/bin/bash

cd /myfolder/podcast/
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl podcast_spider