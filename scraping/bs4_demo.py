#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup


def main():
    URL = "https://realpython.github.io/fake-jobs/"
    page = requests.get(URL)

    # print(page.text)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="ResultsContainer")
    # print(results.prettify())

    # Print all job elements
    # job_elements = results.find_all("div", class_="card-content")
    # for job_element in job_elements:
    #     # print(job_element, end="\n"*2)
    #     title_element = job_element.find("h2", class_="title")
    #     company_element = job_element.find("h3", class_="company")
    #     location_element = job_element.find("p", class_="location")
    #     print(title_element.text.strip())
    #     print(company_element.text.strip())
    #     print(location_element.text.strip())
    #     print()

    # Filter results by search term
    # The lambda function looks at the text of each <h2> element, converts it to lowercase,
    # and checks whether the substring "python" is found anywhere.
    python_jobs = results.find_all(
        name="h2", string=lambda text: "python" in text.lower()
    )

    # List comprehension that operates on each of the <h2> title elements in
    # python_jobs that you got by filtering with the lambda expression. You’re selecting
    # the parent element of the parent element of the parent element of each <h2> title element.
    python_job_elements = [
        h2_element.parent.parent.parent for h2_element in python_jobs
    ]
    # print(len(python_job_elements))

    for python_job in python_job_elements:
        title_element = python_job.find("h2", class_="title")
        company_element = python_job.find("h3", class_="company")
        location_element = python_job.find("p", class_="location")
        links = python_job.find_all("a")
        link_url = python_job.find_all("a")[1]["href"]

        print(title_element.text.strip())
        print(company_element.text.strip())
        print(location_element.text.strip())
        print(f"Apply here: {link_url}\n")

        print()


if __name__ == "__main__":
    main()
