from datapackage import Package
import pandas as pd
import pathlib
import plot_helper

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
    df = pd.DataFrame(oil_daily, columns = ["date", "oil"])
    if do_save:
        df.to_csv("data/oil/"+oil_type+".csv")
    return df

def plot_oil(oil_type = "brent"):
    my_file = pathlib.Path("data/oil/"+oil_type+".csv")
    if not my_file.exists ():
        print("No oil prices found. Request from DB:")
        df = get_prices(oil_type)
    else:
        df=pd.read_csv(my_file)
    plot_helper.plot_over_time(df,True,'oil','Price evolution of ','oil')

def main():
    #print(get_prices().head())
    plot_oil()

if __name__ == "__main__":
    main()
    
