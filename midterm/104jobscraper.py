from bs4 import BeautifulSoup
import requests
from googletrans import Translator
import pandas as pd

def translate_to_english(text):
    translator = Translator()
    return translator.translate(text, src='zh-tw', dest='en').text

def scrape_104_jobs(Location, keyword):
    url = f"https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={keyword}&jobsource=2018indexpoc&city=6001001000&area={Location}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        job_listings = soup.find_all("article", class_="job-list-item")

        jobs_data = []  # List to store job details

        for job in job_listings:
            title = job.find("a", class_="js-job-link").text.strip()

            translated_title = translate_to_english(title)

            location = job.find("ul", class_="job-list-intro").find("li").text.strip()

            translated_location = translate_to_english(location)

            experience = job.find("ul", class_="job-list-intro").find_all("li")[1].text.strip()

            translated_experience = translate_to_english(experience)

            salary_element = job.find("a", class_="b-tag--default")
            if salary_element:
                salary = salary_element.text.strip()
            else:
                salary = "Salary not available"

            translated_salary = translate_to_english(salary)

            job_link = job.find("a", class_="js-job-link")["href"]
            job_link = job_link[2:]

            job_data = {
                "Title": translated_title,
                "Location": translated_location,
                "Experience": translated_experience,
                "Salary or other descriptions": translated_salary,
                "Job Link": job_link,
            }
            jobs_data.append(job_data)

        jobs_df = pd.DataFrame(jobs_data)

        print(jobs_df.to_string())

    else:
        print("Failed to retrieve data from 104 Job Bank.")

area_data = {
    "City": ["Taipei", "New Taipei City", "Yilan", "Keelung", "Taoyuan", "Hsinchu", "Miaoli", "Taichung",
             "Changhua", "Nantou", "Yunlin", "Chiayi", "Tainan", "Kaoshiung", "Pingtung", "Taitung",
             "Hualien", "Penghu", "Kinmen", "Lianjiang"],
    "Code": [6001001000, 6001002000, 6001003000, 6001004000, 6001005000, 6001006000, 6001007000, 6001008000,
             6001010000, 6001011000, 6001012000, 6001013000, 6001014000, 6001016000, 6001018000, 6001019000,
             6001020000, 6001021000, 6001022000, 6001023000]
}

area_df = pd.DataFrame(area_data)
print(area_df)

if __name__ == "__main__":
    Location = input("Enter the location code(e.g., 6001001000): ")
    keyword = input("Enter the keyword (e.g., part-time): ")

    scrape_104_jobs(Location, keyword)



