import time
import csv
import concurrent.futures
from bs4 import BeautifulSoup
from selenium import webdriver

# número máximo de threads (pode mudar para 5, 10, 20)
MAX_THREADS = 10

def extract_movie_details(row):
    """Extrai título, ano e nota de um item da lista"""
    title_tag = row.find("h3")
    title = title_tag.get_text(strip=True) if title_tag else ""

    year_tag = row.find("span", class_="cli-title-metadata-item")
    year = year_tag.get_text(strip=True) if year_tag else ""

    rating_tag = row.find("span", class_="ipc-rating-star--rating")
    rating = rating_tag.get_text(strip=True) if rating_tag else ""

    return [title, year, rating]

def extract_movies(soup):
    movie_rows = soup.find_all("li", attrs={"class": "ipc-metadata-list-summary-item"})
    print(f"Total de filmes encontrados: {len(movie_rows)}")

    # usa threads para acelerar a extração
    threads = min(MAX_THREADS, len(movie_rows))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(extract_movie_details, movie_rows))

    # grava no CSV
    with open("movies.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Título", "Ano", "Nota"])
        for movie in results:
            print(movie)
            writer.writerow(movie)

def main():
    start_time = time.time()  # marca o início

    driver = webdriver.Chrome()
    driver.get("https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm")
    time.sleep(5)  # espera JS carregar

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    extract_movies(soup)

    end_time = time.time()  # marca o fim
    print("Tempo total:", end_time - start_time, "segundos")

if __name__ == "__main__":
    main()
