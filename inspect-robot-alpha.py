from PIL import Image
for name in ['mech-bosses-v15.png','robot-enemies-v15.png']:
 im=Image.open('assets/'+name);print(name,im.mode,im.size,im.getextrema()[-1],im.getpixel((0,0)))
