from bs4 import BeautifulSoup
import requests
from googletrans import Translator


def translate_to_english(text):
    translator = Translator()
    return translator.translate(text, src='zh-tw', dest='en').text


def scrape_104_jobs(Location, keyword):
    url = f"https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={keyword}&jobsource=2018indexpoc&city=6001001000&area={Location}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        job_listings = soup.find_all("article", class_="job-list-item")

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

            print("Title:", translated_title)
            print("Location:", translated_location)
            print("Experience:", translated_experience)
            print("Salary or others:", translated_salary)
            print("Job Link:", job_link)
            print("-" * 50)
    else:
        print("Failed to retrieve data from 104 Job Bank.")


area = {
    "taipei": 6001001000,
    "newtaipeicity": 6001002000,
    "yilan": 6001003000,
    "keelung": 6001004000,
    "taoyuan": 6001005000,
    "hsinchu": 6001006000,
    "miaoli": 6001007000,
    "taichung": 6001008000,
    "changhua": 6001010000,
    "nantou": 6001011000,
    "yunlin": 6001012000,
    "chiayi": 6001013000,
    "tainan": 6001014000,
    "kaoshiung": 6001016000,
    "pingtung": 6001018000,
    "taitung": 6001019000,
    "hualien": 6001020000,
    "penghu": 6001021000,
    "kinmen": 6001022000,
    "lianjiang": 6001023000
}

for city, code in area.items():
    print(f"{city.capitalize()}, {code}")

if __name__ == "__main__":
    Location = input("Enter the location (e.g., 6001001000): ")
    keyword = input("Enter the keyword (e.g., part-time): ")

    scrape_104_jobs(Location, keyword)


