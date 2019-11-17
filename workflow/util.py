import datetime
import json
from numbers import Number, Real
import re
from .string import Lines

def __should_quote(string: str) -> bool:
  # special characters
  if re.search(r'[\u0000-\u001F\u0023\u002C\u003A]', string): return True
  if string[0] in [' ', '!', '"', '&', "'", '*', '-', '[', '{', '|']: return True
  if string.endswith(" "): return True

  # number
  if re.search(r'^\d+(,\d+)*(\.\d+)?$', string): return True
  if re.search(r'^0x[0-9A-Fa-f]+$', string): return True
  
  # boolean
  if string in ['true', 'yes', 'on', 'false', 'no', 'off']: return True

  # null
  if string == '~' or string == 'null': return True

  # date and time
  try: datetime.fromisoformat(string); return True
  except: pass

  return False

def yaml_from_string(string: str, force_flow_style: bool = False) -> Lines:
  if len(string) == 0: return Lines("''")
  
  numberOfLF = string.count("\n")
  if numberOfLF == 0:
    if __should_quote(string):
      return Lines(json.dumps(string, ensure_ascii=False))
    return Lines(string)
  
  if force_flow_style or (numberOfLF == 1 and string.endswith("\n")):
    return Lines(json.dumps(string, ensure_ascii=False))
  
  result: Lines = Lines(string)
  result.shift_right()
  result.insert(0, ('|+' if string.endswith("\n") else '|'))
  return result

def yaml_from_number(number: Number) -> Lines:
  if not isinstance(number, Real):
    raise ValueError("Not a real number.")
  return Lines(str(number))

def yaml_from_boolean(boolean: bool) -> Lines:
  return Lines('true' if boolean else 'false')
