import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def main():
    # Abre o navegador com Selenium
    driver = webdriver.Chrome()
    driver.get("https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm")
    time.sleep(5)  # espera o JavaScript carregar

    # Captura o HTML já renderizado
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Cada filme está em um <li> com essa classe
    movie_rows = soup.find_all("li", attrs={"class": "ipc-metadata-list-summary-item"})

    # Cria o CSV com cabeçalho
    with open("movies.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Título", "Ano", "Nota"])

        # Extrai dados de cada filme
        for row in movie_rows:
            # título
            title_tag = row.find("h3")
            title = title_tag.get_text(strip=True) if title_tag else ""

            # ano (primeiro item da metadata)
            year_tag = row.find("span", class_="cli-title-metadata-item")
            year = year_tag.get_text(strip=True) if year_tag else ""

            # nota (se existir)
            rating_tag = row.find("span", class_="ipc-rating-star--rating")
            rating = rating_tag.get_text(strip=True) if rating_tag else ""

            print(title, year, rating)
            writer.writerow([title, year, rating])

if __name__ == "__main__":
    main()

