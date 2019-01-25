# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy import Spider
from parsel import Selector
from scrapy.http import Request

class SubjectsSpider(Spider):
    name = 'subjects'
    allowed_domains = ['class-central.com']
    start_urls = ['http://class-central.com/subjects']

    def __init__(self, subject=None):
    	self.subject = subject

    def parse(self, response):
    	if self.subject:
    		subject_url = response.xpath('//*[contains(@title, "' + self.subject + '")]/@href').extract_first()
    		yield Request(response.urljoin(subject_url), callback=self.parse_subject)
    	else:
    		self.logger.info("Scrapping of Subjects")
    		subjects = response.xpath('//*[@class="text--blue"]/@href').extract()
    		for subject in subjects:
    			yield Request(response.urljoin(subject), callback=self.parse_subject)

    def parse_subject(self, response):
    	subject_name = response.xpath('//title/text()').extract_first()
    	subject_name = subject_name.split(' | ')[0][6:]

    	courses = response.xpath('//*[@class="text--charcoal text-2 medium-up-text-1 block course-name"]')
    	for course in courses:
    		course_name = course.xpath('.//@title').extract_first()
    		course_url = course.xpath('.//@href').extract_first()
    		absolute_course_url = response.urljoin(course_url)

    		yield{
    			'subject_name' : subject_name,
    			'course_name' : course_name,
				'absolute_course_url' : absolute_course_url
    		}

    	#next_page = response.xpath('//*[@id="show-more-courses"]')