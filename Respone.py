import requests

query = "Spaghetti and Meatballs"
response = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search?api_key=VpP90f5EA1cbbZbyheBqpZnu1pXkoy0HPtnb9Dg5&query={0}".format(query))
print(response.status_code)
res = response.json()
for i in range(100):
    if "ingredients" in res["foods"][i]:
        print(res["foods"][i]["ingredients"])
        break 