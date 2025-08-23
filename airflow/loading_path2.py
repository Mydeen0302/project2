import requests
def loading_path():
    url = "http://backend:5000/todo"
    response = requests.get(url)
    if response.status_code == 404:
        return None, None
    temp = response.json()
    doc_id = temp.get('doc_id')
    dataset_name = temp.get('dataset_name')
    if not doc_id or not dataset_name:
        return None, None
    return f"gs://dsstorage_1/{dataset_name}.csv", doc_id
