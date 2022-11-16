import ast
import urllib.request as req
from config import BASE_DIR

def formatTagsList(tagsList):
  for i, tag in enumerate(tagsList):
    if not tag.startswith("#"):
      tagsList[i] = "#" + tag
  return tagsList

def strTagToTagsList(tags):
  return ast.literal_eval(tags)

def tagsListToStrTag(tagsList):
  return f'{list(set(formatTagsList(tagsList)))}'

def saveImageFromLifeFourCuts(url, filename):
  ''' 인생 네컷 링크 사진 저장'''
  splitUrl = url.split("/")
  splitUrl[-1] = "image.jpg"
  formattedUrl = "/".join(splitUrl)
  req.urlretrieve(formattedUrl, BASE_DIR + f"/static/upload/{filename}.jpg")


def saveImageAndReturnUrl(brand, QRcodeUrl, filename):
  if brand == "lifeFourCuts":
      saveImageFromLifeFourCuts(QRcodeUrl, filename)
      return f"./static/upload/{filename}.jpg"