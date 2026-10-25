import urllib.request,urllib.parse,re,pathlib
p=pathlib.Path('assets/fonts')
text='余烬防线开始游戏玩法图鉴已暂停继续返回首页撤离成功全队阵亡再来一局声音设置装备选择'
u='https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&display=swap&text='+urllib.parse.quote(text)
css=urllib.request.urlopen(u).read().decode()
print(css)
for i,url in enumerate(re.findall(r'url\((https[^)]+)\)',css)):
 (p/f'EmberSerif-{i}.woff2').write_bytes(urllib.request.urlopen(url).read())
(p/'Serif-OFL.txt').write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifsc/OFL.txt').read())
