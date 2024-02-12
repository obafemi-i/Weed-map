import requests
from selectolax.parser import HTMLParser
import os
import pandas as pd


output = 'play.csv'

session = requests.Session()


def get_html(url):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    response = session.get(url, headers=header)

    html = HTMLParser(response.content)

    return html


def parse_attribute_error(html, selector):
    try:
        return html.css_first(selector).text().strip()
    except AttributeError:
        return None


def export_to_csv(ads: list):
    file_exists = os.path.isfile(output)

    output_df = pd.DataFrame(ads)

    if not file_exists:
        output_df.to_csv(output, index=False)  
    else:
        output_df.to_csv(output, mode='a', header=False, index=False)


def extract_and_save_info(url):
    content = get_html(url)

    products = content.css('li[data-test-id=menu-item-list-item]')
    for product in products:
        category = parse_attribute_error(product, 'div[data-testid=menu-item-category]')
        name = parse_attribute_error(product, 'div[data-testid=menu-item-title]')
        price = parse_attribute_error(product, 'div.Text-sc-42443ba-0.PriceText-sc-b03e0af1-1.bpRqjV.fpIvWp')
        deals = parse_attribute_error(product, 'div.src__Box-sc-1sbtrzs-0.klazS').split(' ')[0]

        info_list = []

        info_dict = {
            'category': category,
            'Product': name,
            'Price': price,
            'Deals': deals
        }

        info_list.append(info_dict)

        export_to_csv(info_list)


def main():
    for x in range(1, 39):       
        url = f'https://weedmaps.com/dispensaries/mr-nice-guy-costa-mesa?page={x}'
        extract_and_save_info(url)
        print(f'Page {x} extracted. Moving on...')
    
    print('All done')


if __name__=='__main__':
    main()