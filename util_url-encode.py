from urllib import parse
 
url_encoded = parse.quote('./2_데이터셋 생성하기.ipynb')
url_decoded = parse.unquote('')

print(url_encoded)
print(url_decoded)