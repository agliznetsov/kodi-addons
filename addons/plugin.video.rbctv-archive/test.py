from rbc import RbcClient

client = RbcClient()

# for item in items:
#     print item['path']
#     items2 = client.file(item['path'])
#     for file in items2:
#         print file['path']

# print client.files('/archive/Auto/562949993842568.shtml')

# items = client.programs()
items = client.issues('/archive/oboz')
for item in items:
    print client.file(item['path'])
    break
