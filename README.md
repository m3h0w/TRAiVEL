# TRAiVEL
Sentiment-based travel recommendations
https://vimeo.com/263715035

TRAiVEL is a micro-service-based web app for choosing a European travel destinations based on current sentiment in a given country, as calculated by scrapping tweets from that country.

The app is comprised of 4 back-end modules: twitter scarpping, Azure-based multi-language sentiment analysis, Skyscanner api integration, and core web-app back-end; and a front-end application written in vanilla js, using http://datamaps.github.io/ library.

Currently all the modules have to be invoked separately, as more synchronized, automated interaction would require more than 1 weekend.
