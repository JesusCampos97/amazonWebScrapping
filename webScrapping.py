from bs4 import BeautifulSoup
import requests
import csv

# obtenemos el html
url = "https://www.amazon.com/-/es/Los-ms-vendidos-Computadoras-y-Accesorios/zgbs/pc/ref=zg_bs_nav_0"

# ponemos la información del header para simular una conexion web valida
headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
}
# time_out para esperar que cargue la pagina. Si no lo hacemos los datos cargados posteriormente en css con before o javascript pueden no aparecer
page = requests.get(url, headers=headers, timeout=(1000, 1500))
soup = BeautifulSoup(page.content, 'html.parser')
# buscamos todos los producto que estén dentro del contenido 0
products = soup.find_all(id="gridItemRoot")

#creamos las cabeceras del css donde guardaremos los datos
csv_headers = ['Titulo', 'Valoracion', 'Descuento', 'Precio']
with open('amazon_product.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)

#para cada uno de los productos dentro del contenido de gridItemRoot
for product in products:
    #buscamos el contenido que esté en el card del producto
    children = product.find('div', class_='zg-grid-general-faceout').div
    #4 sub-contenidos
    #contenido 0 no tiene nada de texto. Es la imagen
    title = children.contents[1].text
    rank = children.contents[2].text
    #el sub-contenido 3 está compuesto por descuento y precio
    content = children.contents[3].find('div').div.div.contents
    #puede no tener descuento por lo que comparamos
    if (len(content) > 1):
        discount = content[0].text
        price = content[2].text
    else:
        discount = 0
        price = content[0].text

    with open('amazon_product.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([title, rank, discount, price])

print("Work completed")
