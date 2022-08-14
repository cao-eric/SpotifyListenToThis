from bs4 import BeautifulSoup
import requests

def find_jobs():

    # Requests for the reddit HTML page
    html_text = requests.get(
        'https://www.indeed.com/jobs?q=software%20engineer%20intern&l=75040&vjk=98120fd42844e1e5').text

    # Parses through the page with soup
    soup = BeautifulSoup(html_text, 'html.parser')
    # Find the html element that contains the posts
    posts = soup.find_all('div', class_= "job_seen_beacon")
    for post in posts:
        # Title of the post
        job_title = post.find('h2', class_ = "jobTitle").span.text
        if job_title != "new":
            print(job_title)
        job_company = post.find('span', class_="companyName").text
        company_rating = post.find('span', class_ = "ratingNumber").text
        print(job_company + " -- " + company_rating + " stars")
        print()


find_jobs()