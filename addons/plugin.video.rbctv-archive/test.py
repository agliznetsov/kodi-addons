from rbc import RbcClient

client = RbcClient()

# items = client.folder('/archive/oboz')
# for item in items:
#     print item['path']
#     items2 = client.file(item['path'])
#     for file in items2:
#         print file['path']

# print client.files('/archive/Auto/562949993842568.shtml')

items = client.programs()
for item in items:
    print item
