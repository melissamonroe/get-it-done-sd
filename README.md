# City of San Diego Get it Done Dashboard Project
## Team git-it-on

## INSTRUCTIONS FOR RUNNING THE APP
The following instructions for running the app are provided in the order in which they should be done:
1) Under pages/static/js, create a config.js file that contains this line:
const API_KEY = "<YOUR API KEY HERE!>";

2) Under src, add the config.py file that we have provided to you
3) From VScode, open pages/index.html with live server
4) Run app.py

## Project Description

### Audience
City of San Diego Leadership

### Goal?
Provide a dynamic dashboard for City of San Diego leadership
- Identify problem-areas
- Monitor and gage effectiveness of Get-It-Done program overall
- Monitor and gage effectiveness of program by Council district 

### What are we trying to show with the data

- Service request counts - Most volume category Get-It-Done requests
- Status (over time)
- Categories - type of service request over time and by location / council district
- Show volume of service requests over time
- Summary of open/closed service requests in date range
- Length in days to close a service request on average per category
- Drop down selector to filter data more granularly 
- Toggle heat map (layer) and markers layer (lat, lon) of get it done requests
- response time, open/close delta
- Map selector to populate data charts

## Questions we may be able to answer:

- Volume of service requests by category by year / quarter / area
    - Is volume of service requests evenly distributed by council district?
    - Do certain areas have a noticeably smaller or larger number of service requests in any category?
    - Is the volume of service requests steady or are there dips/spikes?
    - Are dips/spikes occurring during certain times of the year? Certain areas?
    
- Performance indicators
    - Average number of days from open to close by category, council district vs overall
    - Is average time to resolve a service request same across categories? Across council districts?
    - Are there dips/spikes?  Certain areas?  Certain times of year?

- Identify outliers - high/low number of service request in any category 
- Lead to action: what action? -> goal reduce number of service requests by 10% in specific category in specific location

This information may help leadership determine if certain areas lack resources, if resources are sufficient but unable to keep up for other reasons, if resources can be moved (temporarily) to other areas to assist, or if more resources need to be allocated, possibly to certain areas during certain times of the year.  

Additional analysis beyond the scope of this dashboard may have to be performed to determine cause and effect of performance issues.

## Dashboard Development

![Dashboard concept](static/images/wireframe1.png)

![Dashboard concept](static/images/wireframe2.png)

![Dashboard preview](static/images/git-it-on-preview.gif)
