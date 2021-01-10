from datapackage import Package
import pandas as pd


def get_prices(oil_type = "brent", do_save = True):
    #https://datahub.io/core/oil-prices#python
    package = Package('https://datahub.io/core/oil-prices/datapackage.json')
    #print(package.resource_names)
    oil_key = oil_type+"-daily"
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':    
            if resource.descriptor['datahub']['derivedFrom'] == [oil_key]:
                oil_daily = resource.read()
                print(len(oil_daily))
    df = pd.DataFrame(oil_daily, columns = ["Date", "Oil_Price"])
    if do_save:
        df.to_csv("data/oil/"+oil_type+".csv")
    return df

def main():
    print(get_prices().head())

if __name__ == "__main__":
    main()
    
