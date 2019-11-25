import grequests


payloads = [{"a": 4, "b": 5}]
urls = ["https://us-central1-braided-grammar-239803.cloudfunctions.net/tmb_test"]
rs = (grequests.post(urls[0], json=u) for idx, u in enumerate(payloads))
print (rs)
#rs = (grequests.get(u) for u in urls)
#print (rs)
res = grequests.map(rs)
print (dir(res[0]))
print (res[0].status_code)
