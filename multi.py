#Imports
import random
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import csv 
from copy import deepcopy
import pandas as pd
import os


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

def get_dob(yrs):
  start_dt = date.today().replace(day=1, month=1).toordinal()
  end_dt = date.today().toordinal()
  random_day = date.fromordinal(random.randint(start_dt, end_dt))
  random_day = random_day - relativedelta(years = yrs)
  random_day = (datetime.strptime(str(random_day), "%Y-%m-%d").strftime("%d/%m/%Y"))
  return random_day 

def normalise(value):
  #print(type(value))
  if type(value) == type("test"):
    value = value.replace("-", "").replace(" ", "")
    value = value.lower()
  return value 

def preprocess(df):
  df['dob'] = df.apply(lambda row: get_dob(row.age), axis=1)
  df['workclass'] = df['workclass'].str.replace("?", "Not working")
  df['occupation'] = df['occupation'].str.replace("?", "No occupation")

  df['g_dob'] = df['dob']
  df['g_workclass'] = df['workclass']
  df['level'] = [(0, 0) for i in range(len(df.index))]
  for (columnName, columnData) in df.iteritems():
    df[columnName] = df.apply(lambda row : normalise(row[columnName]), axis = 1)
  return df


#generalisation functions
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

#check if dataset satisfies anonymity level 

#checks for the minimum value of occurences that are seen here
def get_anonymity_level(gtable, k, doblvl, wclasslvl):
  indices = dict()
  #need to return the remaining dataframe so as to apply the anonymisation again

  #iterating through all the rows of the dataframe and creating a mapping with count of occurences
  for index, row in gtable.iterrows():
    if (row["g_dob"], row["g_workclass"]) not in indices:
      indices[(row["g_dob"], row["g_workclass"])] = []
    indices[(row["g_dob"], row["g_workclass"])].append(index)

  #has all the records of the dataframe
  non_suppressed_table = pd.DataFrame(columns = ['dob', 'workclass', 'occupation', 'level', 'g_dob', 'g_workclass'])
  
  #the records not generalised after the current iteration using values (doblvl, wclasslvl)
  non_generalized_records = pd.DataFrame(columns = ['dob', 'workclass', 'occupation', 'level',  'g_dob', 'g_workclass'])
  
  #the tuples that have been generalised
  generalized_records = pd.DataFrame(columns = ['dob', 'workclass', 'occupation', 'level',  'g_dob', 'g_workclass'])
  
  #the table containing only generalised records
  #suppressed_table = pd.DataFrame(columns = ['dob', 'workclass', 'occupation', 'level',  'g_dob', 'g_workclass'])
  
  min_anonymity = float("inf")
  to_suppress = 0
  for record, count in indices.items():
    min_anonymity = min(min_anonymity, len(count))
    if len(count) < k:
      to_suppress += len(count)
      for c in range(len(count)):
        row = pd.Series({'g_dob' : record[0], 'g_workclass' : record[1], 'dob' : gtable.loc[indices[record][c], 'dob'], 'workclass' :  gtable.loc[indices[record][c], 'workclass'], 'occupation' : gtable.loc[indices[record][c], 'occupation'], 'level' : gtable.loc[indices[record][c], 'level']}, name = indices[record][c])
        #row = pd.Series({'g_dob' : gtable.loc[indices[record][c], 'g_dob'], 'g_workclass' : gtable.loc[indices[record][c], 'g_workclass'], 'dob' : record[0], 'workclass' : record[1], 'occupation' : gtable.loc[indices[record][c], 'occupation'], 'level' : gtable.loc[indices[record][c], 'level']}, name = indices[record][c])
        #non_suppressed_table = non_suppressed_table.append(row)
        non_generalized_records = non_generalized_records.append(row)
    else:
      for c in range(len(count)):
        row = pd.Series({'dob' : gtable.loc[indices[record][c], 'dob'], 'workclass' : gtable.loc[indices[record][c], 'workclass'], 'g_dob' : record[0], 'g_workclass' : record[1],'occupation' :gtable.loc[indices[record][c], 'occupation'], 'level' : (doblvl, wclasslvl)}, name = indices[record][c])
        generalized_records = generalized_records.append(row)
        #non_suppressed_table = non_suppressed_table.append(row)

  if k <= min_anonymity:
    #return True, 0, non_suppressed_table, non_generalized_records, suppressed_table
    return True, generalized_records, non_generalized_records
  else:
    #return False, to_suppress, non_suppressed_table, non_generalized_records, suppressed_table
    return False,  non_generalized_records, generalized_records



#sample number of records from the dataset
def sample_table(number_of_records, df):
  state = random.randint(2, 2**32 - 1)
  #print("the state is ", state)
  headers = ["dob", "workclass", "occupation", "level", "g_dob", "g_workclass"]
  #sampling 50 records from the dataset
  #setting the random_state to 1, so it always select the same set of samples
  table = df.sample(number_of_records, random_state=state)
  sample = pd.concat([table["dob"], table["workclass"], table["occupation"], table['level'], table["g_dob"], table["g_workclass"]], axis=1, keys=headers)
  sample.to_csv("sample.csv")
  return sample, state

#given a tuple combination, returns the generalised table to that level
def generalise_tuple(sample, doblvl, wclasslvl, k):
  gtable = sample.copy(deep=True)
  temp = pd.read_csv("sample.csv")

  for row in gtable.itertuples():
    w = row.workclass[:]
    d = row.dob[:]
    gtable.at[row.Index, 'g_workclass'] = generalise_workclass(w, workclass, wclasslvl)
    gtable.at[row.Index, 'g_dob'] = generalise_dob(d, doblvl)
  
  satisfies_k,  non_generalized_records, generalized_records = get_anonymity_level(gtable, k, doblvl, wclasslvl)
  return satisfies_k, non_generalized_records, generalized_records


def try_path(path, samp, k):
  all_r = pd.DataFrame(columns = ['dob', 'workclass', 'occupation', 'level', 'g_dob', 'g_workclass'])
  for doblvl, wclasslvl in path:
    #print(samp.head())
    satisfies_k, non_generalized_records, generalized_records = generalise_tuple(samp, doblvl, wclasslvl,  k)
    for row in generalized_records.itertuples():
      row = pd.Series({'g_dob' : row.g_dob, 'g_workclass' : row.g_workclass, 'dob' : row.dob, 'workclass' : row.workclass, 'occupation' : row.occupation,  'level' : row.level}, name = row.Index)
      all_r = all_r.append(row)
    #print(doblvl, wclasslvl, " the length of all records is ", len(all_r.index))
    samp = non_generalized_records
    if satisfies_k == True:
      #print("done at ", doblvl, wclasslvl)
      break  
    # print("generalised are ", len(generalized_records.index))
    # print("non gene count ", len(non_generalized_records.index))
    # print()
  

  for row in non_generalized_records.itertuples():
      row = pd.Series({'g_dob' : row.g_dob, 'g_workclass' : row.g_workclass, 'dob' : row.dob, 'workclass' : row.workclass, 'occupation' : row.occupation,  'level' : row.level}, name = row.Index)
      all_r = all_r.append(row)
  
  for row in all_r.itertuples():
      if all_r.at[row.Index, 'level'] == (0, 0):
        try:
          all_r.at[row.Index, 'level'] = (5, 5) 
        except Exception as ex:
          template = "An exception of type {0} occurred. Arguments:\n{1!r}"
          message = template.format(type(ex).__name__, ex.args)
          print(message)
  #print("all records lenghth is ", len(all_r.index))
  return all_r 


from collections import Counter
def multilevel_generalise(nof, k):
    df = preprocess(pd.read_csv("adult.csv"))
    samp, st = sample_table(nof, df) 
    pth = []
    for i in range(5):
        for j in range(5):
            pth.append((i, j))
    generalized_table = try_path(pth, samp,  k)
    print()
    # for lvl, count in (Counter(generalized_table['level']).items()):
    #   print(lvl, count)
    generalized_table.to_csv("result.csv")
    print()
#multilevel_generalise(10, 4)