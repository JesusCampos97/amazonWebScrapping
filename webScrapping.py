from bs4 import BeautifulSoup
import requests
import csv
# obtenemos el html de la url
url = "https://www.amazon.com/-/es/Los-ms-vendidos-Computadoras-y-Accesorios/zgbs/pc/ref=zg_bs_nav_0"
# ponemos la informacion dle header para simular una conexion web valida
headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
}
# obtenemos la info de la pagina con el request. El timeout es para esperar a que cargue la pagina. Si no lo hacemos, los datos carados posteriormente con css mediante before o javascript no estarán disposnibles
page = requests.get(url, headers=headers, timeout=(1000, 1500))
soup = BeautifulSoup(page.content, 'html.parser')
# buscams todos los productos que esten dentro del contenido 0
products = soup.find_all(id="gridItemRoot")

# creamos las cabeceras del css donde guardaremos los datos
csv_headers = ["Tiutlo", "Valoracion", "Precio"]
with open('amazon_products.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)
# para cada no de los productos dentro del contenido de gridItemRoot
for product in products:
    # buscamos el contenido que esté dentro del card en el producto
    children = product.find('div', class_="zg-grid-general-faceout").div
    # tenemos 4 sub-contenidos. Contenido 0 no tiene nada de texto solo la imagen
    title = children.contents[1].text
    rank = children.contents[2].text
    price = children.contents[3].text
  
    with open('amazon_products.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([title, rank, price])
      
print("Work completed")
