# 下載wwm模型
import requests


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    total_index = int(response.headers.get('content-length'))/CHUNK_SIZE+1
    with open(destination, "wb") as f:
        for idx,chunk in enumerate(response.iter_content(CHUNK_SIZE)):
            if idx % 100 == 0:
                print(f"Downloading{'.'*(int(idx%1000/100)+1)}:{round(float(idx*100/int(total_index)),2)}%",end="\r")
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


if __name__ == "__main__":
    # file_id = "1d-_D_wPVXV9IX-n9rkyyGdu77FWY9myx"
    # destination = './pytorch_model.bin'
    # download_file_from_google_drive(file_id, destination)

    file_id = "1Dc2EHJgRop2AayGvr_NVk4AQRuTm-Sgu"
    destination = './config.json'
    download_file_from_google_drive(file_id, destination)



