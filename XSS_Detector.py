from use_gpt4 import use_gpt4
import requests
import sys

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("usage: python XSS_Detector.py <url>")
        exit(-1)
    url=sys.argv[1]
    response = requests.get(url)
    html_content = response.text
    print(len(html_content))
    result=use_gpt4(html_content, "gpt-4o")
    print(result)
