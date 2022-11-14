import ast

def formatTagsList(tagsList):
  for i, tag in enumerate(tagsList):
    if not tag.startswith("#"):
      tagsList[i] = "#" + tag
  return tagsList

def strTagToTagsList(tags):
  return ast.literal_eval(tags)

def tagsListToStrTag(tagsList):
  return f'{list(set(formatTagsList(tagsList)))}'
