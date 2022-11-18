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


def saveImageFromPhotoism(url, filename):
  ''' 포토이즘 링크 사진 저장 '''
  ''' 5회까지만 URL 방문 가능 '''

  splitUrl = url.split("/")
  photoId = splitUrl[-1].split("=")[-1]
  splitUrl.pop()
  splitUrl.append("take")
  splitUrl.append(photoId + ".jpg")
  formattedUrl = "/".join(splitUrl)
  req.urlretrieve(formattedUrl, BASE_DIR + f"/static/upload/{filename}.jpg")


def saveImageAndReturnUrl(brand, QRcodeUrl, filename):
  if brand == "lifeFourCuts":
    saveImageFromLifeFourCuts(QRcodeUrl, filename)
  elif brand == "photoism":
    saveImageFromPhotoism(QRcodeUrl, filename)
  
  return f"./static/upload/{filename}.jpg"

