import requests
import json
import csv

# StockX Data Downloader
# Downloads sales data from given search term and puts it in a CSV
# Do you hate how I code? Fork and pull request. You won't, no balls.
# @dogman_aud

def search(sku):

    search = requests.get(
            f'https://stockx.com/api/search?query={sku}&currency=USD'
        )

    searchJSON = json.loads(search.text)
    firstSearch = searchJSON['hits'][0]
    name = firstSearch['url']
    objectid = firstSearch['objectID']
    saleRAW = requests.get((
                'https://stockx.com/api/products/{}'
                '/activity?state=480&currency=USD'
                '&limit=100000000&page=1&sort=createdAt&order=DESC'
                .format(objectid)
            )
        )

    saleJSON = json.loads(saleRAW.text)

    return saleJSON

def toCSV(saleJSON):

    with open(f'{name}.csv','w') as outputCSV:
        csvWriter = csv.writer(outputCSV)
        csvWriter.writerow(['Date','Size','Price'])
        for item in saleJSON['ProductActivity']:
            csvWriter.writerow([item['createdAt'],item['shoeSize'],item['amount']])
        #   uncomment the following if you like terminal spam
        #     print(
        #     f'Wrote: Date: {item['createdAt']} | Size: {item['shoeSize']} | Amount: {item['amount']}'
        # )

def main():

    print('')
    print('StockX Data Downloader')
    print('by @dogman_aud')
    print('made better by you!')
    print('')

    sku = input('Input SKU (or search term, if you\'re feeling lucky): ')

    saleJSON = search(str(sku))

    toCSV(saleJSON)

    print('')
    print('Success: wrote {}.csv'.format(name))
    print('Total Sales: {}'.format(str(saleJSON['Pagination']['total'])))
    print('')

if __name__ == '__main__':
    main()
