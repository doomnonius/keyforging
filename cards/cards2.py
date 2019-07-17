import json


def removeUseless(S):
  """Removes spaces from a string.
  """
  if len(S) == 0:
    return ''
  if S[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
    return S[0] + removeUseless(S[1:])
  else:
    return '' + removeUseless(S[1:])

def parse():
  """Sorts the cards by card number into a list.
  """
  def sortID(val):
    """Key for sorting by id
    """
    return val['card_number']
  
  with open('cards/cards.json') as f:
    data = json.load(f)
    data.sort(key = sortID)
    n = 0
    missing = []
    for b in data:
      if b['card_number'] == n + 1:
        last = b['card_number']
        n += 1
      else:
        current = b['card_number']
        while last < current:
          last += 1
          missing.append(last)
        n = current
    print(missing)

  with open('cards/sortedCards.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

  with open('cards/sortedCards.json') as f:
    data = json.load(f)
    for b in data:
      print(b['card_title'])

[51, 90, 91, 105, 130, 131, 134, 135, 159, 160, 168, 169, 176, 177, 184, 185, 246, 247, 248, 249, 250, 264, 265, 339, 340]
# card_title = name
# card_type = card_type
# front_image = imageUrl
# description = card_text
# is_maverick = isMaverick
# power and armor are strings
# rarity is a value
parse()