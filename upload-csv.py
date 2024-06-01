# upload_csv.py
import requests

def main():
    filename = input("Enter the path to the CSV file: ")
    with open(filename, "rb") as f:
        files = {"file": f}
        response = requests.post("http://localhost:8000/upload/", files=files)
        print(response.json())

if __name__ == "__main__":
    main()
