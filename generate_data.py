import csv 
import random
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os 
import matplotlib.pyplot as plt

def get_anonymity_level(gtable, k, seed_val, doblvl, wclasslvl):
  indices = dict()
  for index, row in gtable.iterrows():
    if (row["dob"], row["workclass"]) not in indices:
      indices[(row["dob"], row["workclass"])] = []
    indices[(row["dob"], row["workclass"])].append(index)

  not_suppressed = pd.DataFrame(columns = ['dob', 'workclass', 'occupation'])
  suppressed = pd.DataFrame(columns = ['dob', 'workclass', 'occupation'])
  min_anonymity = float("inf")
  to_suppress = 0
  for record, count in indices.items():
    min_anonymity = min(min_anonymity, len(count))
    for c in range(len(count)):
      row = pd.Series({'dob' : record[0], 'workclass' : record[1], 'occupation' : gtable.loc[indices[record][c], 'occupation']}, name = indices[record][c])
      not_suppressed = not_suppressed.append(row)
    if len(count) < k:
      to_suppress += len(count)
    else:
      for c in range(len(count)):
        x = 10
        row = pd.Series({'dob' : record[0], 'workclass' : record[1], 'occupation' : gtable.loc[indices[record][c], 'occupation']}, name = indices[record][c])
        suppressed = suppressed.append(row)

  
  suppressed.to_csv("with_suppression.csv")
  not_suppressed.to_csv("without_suppression.csv")

  if k <= min_anonymity:
    return True, 0 
  else:
    return False, to_suppress

def get_dob(yrs):
  start_dt = date.today().replace(day=1, month=1).toordinal()
  end_dt = date.today().toordinal()
  random_day = date.fromordinal(random.randint(start_dt, end_dt))
  random_day = random_day - relativedelta(years = yrs)
  random_day = (datetime.strptime(str(random_day), "%Y-%m-%d").strftime("%d/%m/%Y"))
  return random_day 

def normalise(value):
  if type(value) == type("test"):
    value = value.replace("-", "").replace(" ", "")
    value = value.lower()
  return value 

def generalise_dob(dob, level):
  if level == 0:
    return dob 
  
  elif level == 1:
    return "/".join(dob.split("/")[1:])
  
  elif level == 2:
    return dob.split("/")[2]
  
  elif level == 3:
    year = int(dob.split("/")[2])
    lower = year - (year % 10)
    higher = (year + 10) - ((year + 10) % 10)
    return str(lower) + "-" + str(higher)

  elif level == 4:
    year = dob.split("/")[2]
    century = year[:2]
    rem = int(year) % 100
    if rem // 25 == 0:
      return century + "00-" + century + "25"

    elif rem // 25 == 1:
      return century + "25-" + century + "50"

    elif rem // 25 == 2:
      return century + "50-" + century + "75"
    
    else:
      return  century + "75-" + str(int(century)+1) + "00"

  elif level == 5:
    year = dob.split("/")[2]
    return year[:2] + "00"


def generalise_workclass(wclass, workclass, level):
  return workclass[wclass][level]

def preprocess(df):
  df['dob'] = df.apply(lambda row: get_dob(row.age), axis=1)
  df['workclass'] = df['workclass'].str.replace("?", "Not working")
  df['occupation'] = df['occupation'].str.replace("?", "No occupation")
  for (columnName, columnData) in df.iteritems():
    df[columnName] = df.apply(lambda row : normalise(row[columnName]), axis = 1) 
  return df

def integrate(k, doblvl, wclasslvl):
    df = pd.read_csv("adult.csv")
    workclass = dict()
    workclass["notworking"] = ["notworking", "notworking", "notworking", "notworking", "notworking", "notreleased"]
    workclass["selfempnotinc"] = ["selfempnotinc", "independent", "independent", "withpay", "working", "notreleased"]
    workclass["selfempinc"] = ["selfempinc", "independent", "independent", "withpay", "working", "notreleased"]
    workclass["private"] = ["private", "nonindependent", "nonindependent", "withpay", "working", "notreleased"]
    workclass["stategov"] = ["stategov", "gov", "nonindependent", "withpay", "working", "notreleased"]
    workclass["federalgov"] = ["federalgov", "gov", "nonindependent", "withpay", "working", "notreleased"]
    workclass["localgov"] = ["localgov", "gov", "nonindependent", "withpay", "working", "notreleased"]
    workclass["withoutpay"] = ["withoutpay", "withoutpay", "withoutpay", "withoutpay", "notworking", "notreleased"]
    workclass["worked"] = ["worked", "worked", "worked", "worked", "notworking", "notreleased"]
    workclass["neverworked"] = ["neverworked", "neverworked", "neverworked", "neverworked", "notworking", "notreleased"]

    cartesian_product = []
    for i in range(6):
        for j in range(6):
            cartesian_product.append((i, j))

    state = random.randint(2, 2**32 - 1)
    df = preprocess(df)
    headers = ["dob", "workclass", "occupation"]
    #sampling 50 records from the dataset
    idx, to_drop = [], []
    #setting the random_state to 1, so it always select the same set of samples
    table = df.sample(50, random_state=state)
    sample = pd.concat([table["dob"], table["workclass"], table["occupation"]], axis=1, keys=headers)
    sample.to_csv("sample.csv")
    index = 0

    gtable = sample.copy(deep=True)
    idx.append((doblvl, wclasslvl))
    print()
    gtable['dob'] = gtable.apply(lambda row: generalise_dob(row.dob, doblvl), axis=1)
    gtable['workclass'] = gtable.apply(lambda row: generalise_workclass(row.workclass, workclass, wclasslvl), axis=1)
    satisfies_k, to_supress = get_anonymity_level(gtable, k, state, doblvl, wclasslvl)
    to_drop.append(to_supress)
    if satisfies_k:
        print("SATISFIES k anonymity, nothing to suppress")
    else:
        print("DOES NOT satisfy k anonymity drop ", to_supress)
    index += 1
    return None

    
    