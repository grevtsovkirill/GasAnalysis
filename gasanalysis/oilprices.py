from datapackage import Package

#https://datahub.io/core/oil-prices#python
package = Package('https://datahub.io/core/oil-prices/datapackage.json')

# print list of all resources:
print(package.resource_names)

#print processed tabular data (if exists any)
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv':
        print(resource.read())
#print(package.resources['brent-daily_csv'].read())
