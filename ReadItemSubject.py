# -*- coding: utf-8 -*-

import pywikibot

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()


def addsubject(subjects, subject):
  if subjects == '':
    subjects = subject
  else:
    subjects = f"{subjects}, {subject}"
  return (subjects)


def getLabel(item):
  try:
    return (item.labels['fr'])
  except:
    try:
      return(item.labels['en'])
    except:
      try:
        return(item.labels['mul'])
      except:
        return ''


def getInfo(targetfile, itemId):
  if itemId =='':
    return
  item = pywikibot.ItemPage(repo, itemId)
  print (getLabel(item) )
  itemsubject = getLabel(item)
  subject_id = 'P921'
  subjects = ''
  if subject_id in item.claims:
    for name in item.claims[subject_id]:
      data = name.toJSON()
      numeric_id = (data.get("mainsnak", {})
                        .get("datavalue", {})
                        .get("value", {})
                        .get("numeric-id") )
      item2 = pywikibot.ItemPage(repo, f"Q{numeric_id}")
      subjects = addsubject(subjects, getLabel(item2))
  print (f"{itemId}; {itemsubject}; {subjects}\n")
  targetfile.write(f"{itemId}; \"{itemsubject}\"; {subjects}\n")


def main():
    filename = 'Subject_results.txt'
    ft = open(filename, "w")
    ft.write("Id;Titre;sujet ou thème principal\n")
    filename = "Subject_id.txt"
    result = ''
    fh = open(filename, "r")
    lines = fh.readlines()
    for line in lines:
        line = line.strip()
        getInfo(ft, line)
    fh.close()
    ft.close()


main()