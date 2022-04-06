#Imports
import random
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import pickle
import csv 
from copy import deepcopy
import pandas as pd
from collections import Counter
import os
import time

class hierarchies:
  def __init__(self):
    self.workclass = dict()
    self.education = dict()
    #workclass graph
    self.wg = dict()
    self.w_map = dict()
    self.w_score = dict()
    
    #education graph
    self.eg  = dict()
    self.e_map = dict()
    self.e_score = dict()

    self.instantiate_workclass()
    self.instantiate_education()
    self.workclass_graph()
    self.education_graph()

  def workclass_graph(self):
    #scores
    self.w_score[8] = (1/5, 1)
    self.w_score[9] = (1/5, 1)
    self.w_score[10] = (1/5, 2)
    self.w_score[12] = (1/6, 3)
    self.w_score[13] = (1/6, 3)
    self.w_score[14] = (1/6, 3)
    self.w_score[5] = (1/3, 4)
    self.w_score[3] = (1/2, 5)

    #self.wg["notreleased"] = {"worked", "neverworked"}
    self.wg[1] = {2, 3}
    self.w_map["notreleased"] = 1

    #self.wg["worked"] = {"withpay", "withoutpay"}
    self.wg[2] = {4, 5}
    self.w_map["worked"] = 2

    self.wg[3] = {}
    self.w_map["neverworked"] = 3

    #self.wg["withpay"] = {"nonindependent", "independent"}
    self.wg[4] = {6, 7}
    self.w_map["withpay"] = 4

    self.wg[5] = {}
    self.w_map["withoutpay"] = 5

    #self.wg["independent"] = {"selfempnotinc", "selfempinc"}
    self.wg[6] = {8, 9}
    self.w_map["independent"] = 6

    self.wg[7] = {10, 11}
    #self.wg["nonindependent"] = {"private", "gov"}
    self.w_map["nonindependent"] = 7 
    
    self.wg[8] = {}
    self.wg[9] = {}

    self.w_map["selfempnotinc"] = 8
    self.w_map["selfempinc"] = 9
    
    self.wg[10] = {}
    self.w_map["private"] = 10
    
    self.wg[11] = {12, 13, 14}
    #self.wg["gov"] = {"stategov", "federalgov", "localgov"}
    self.w_map["gov"] = 11

    self.wg[12] = {}
    self.wg[13] = {}
    self.wg[14] = {}
    
    self.w_map["stategov"] = 12
    self.w_map["federalgov"] = 13
    self.w_map["localgov"] = 14

  def education_graph(self):
    #scores

    self.e_score[8] = (1/5, 1)
    self.e_score[9] = (1/5, 1)
    self.e_score[7] = (1/4, 2)
    self.e_score[10] = (1/4, 3)
    self.e_score[11] = (1/4, 3)
    self.e_score[12] = (1/4, 3)
    self.e_score[13] = (1/3, 4)
    self.e_score[19] = (1/4, 5)
    self.e_score[20] = (1/4, 5)
    self.e_score[21] = (1/4, 6)
    self.e_score[22] = (1/4, 7)
    self.e_score[23] = (1/4, 7)
    self.e_score[24] = (1/4, 8)
    self.e_score[25] = (1/4, 8)
    self.e_score[26] = (1/4, 9)
    self.e_score[27] = (1/4, 9)


    self.eg[1] = {2, 3}
    self.e_map["educated"] = 1

    self.eg[2] = {4, 5}
    self.e_map["professional"] = 2

    self.eg[4] = {6, 7}
    self.e_map["skilldevelopment"] = 4

    self.eg[5] = {10, 11, 12}
    self.e_map["degreeholder"] = 5

    self.eg[6] = {8, 9}
    self.e_map["associatedegree"] = 6

    self.eg[8] = {}
    self.e_map["assocacdm"] = 8

    self.eg[9] = {}
    self.e_map["assocvoc"] = 9

    self.eg[7] = {}
    self.e_map["somecollege"] = 7

    self.eg[10] = {}
    self.e_map["bachelors"] = 10

    self.eg[11] = {}
    self.e_map["masters"] = 11

    self.eg[12] = {}
    self.e_map["doctorate"] = 12

    self.eg[3] = {13, 14, 15, 16, 17, 18}
    self.e_map["school"] = 3

    self.eg[13] = {}
    self.e_map["preschool"] = 13

    self.eg[14] = {19, 20}
    self.e_map["primary"] = 14

    self.eg[15] = {21}
    self.e_map["middle"] = 15

    self.eg[16] = {22, 23}
    self.e_map["secondary"] = 16

    self.eg[17] = {24, 25}
    self.e_map["highersecondary"] = 17

    self.eg[18] = {26, 27}
    self.e_map["postschool"] = 18

    self.eg[19] = {}
    self.e_map["1st4th"] = 19

    self.eg[20] = {}
    self.e_map["5th6th"] = 20

    self.eg[21] = {}
    self.e_map["7th8th"] = 21

    self.eg[22] = {}
    self.e_map["9th"] = 22

    self.eg[23] = {}
    self.e_map["10th"] = 23

    self.eg[24] = {}
    self.e_map["11th"] = 24

    self.eg[25] = {}
    self.e_map["12th"] = 25

    self.eg[26] = {}
    self.e_map["hsgrad"] = 26

    self.eg[27] = {}
    self.e_map["profschool"] = 27

  def instantiate_workclass(self):
    self.workclass["neverworked"] = ["neverworked", "notreleased"]
    self.workclass["selfempnotinc"] = ["selfempnotinc", "independent", "withpay", "worked", "notreleased"]
    self.workclass["selfempinc"] = ["selfempinc", "independent", "withpay", "worked", "notreleased"]
    self.workclass["private"] = ["private", "nonindependent", "withpay", "worked", "notreleased"]
    self.workclass["stategov"] = ["stategov", "gov", "nonindependent", "withpay", "worked", "notreleased"]
    self.workclass["federalgov"] = ["federalgov", "gov", "nonindependent", "withpay", "worked", "notreleased"]
    self.workclass["localgov"] = ["localgov", "gov", "nonindependent", "withpay", "worked", "notreleased"]
    self.workclass["withoutpay"] = ["withoutpay", "neverworked", "notreleased"]
    self.workclass["worked"] = ["worked", "neverworked", "notreleased"]
    self.workclass["neverworked"] = ["neverworked", "notreleased"]
    return self.workclass 
  
  def instantiate_education(self):
    self.education['assocacdm'] = ["assocacdm", "associatedegree", "skilldevelopment", "professional", "educated"]
    self.education['assocvoc'] = ["assocvoc", "associatedegree", "skilldevelopment", "professional", "educated"]
    self.education['somecollege'] = ["somecollege", "skilldevelopment", "professional", "educated"]
    self.education['bachelors'] = ['bachelors', 'degreeholder', "professional", "educated"]
    self.education['masters'] = ['masters', 'degreeholder', "professional", "educated"]
    self.education['doctorate'] = ['doctorate', 'degreeholder', "professional", "educated"]
    self.education['1st4th'] = ['1st4th', 'primary', 'school', 'educated']
    self.education['5th6th'] = ['5ht6th', 'primary', 'school', 'educated']
    self.education['7th8th'] = ['7th8th', 'middle',  'school', 'educated']
    self.education['9th'] = ['9th', 'secondary', 'school', 'educated']
    self.education['10th'] = ['10th', 'secondary', 'school', 'educated']
    self.education['11th'] = ['11th', 'highersecondary', 'school', 'educated']
    self.education['12th'] = ['12th', 'highersecondary', 'school', 'educated']
    self.education['hsgrad'] = ['hsgrad', 'postschool','school', 'educated']
    self.education['profschool'] = ['profschool', 'postschool', 'school', 'educated']
    self.education['preschool'] = ['preschool', 'school', 'educated']
    return self.education


class pre_process_data:
  def __init__(self, output_path, number_of_records=32560, input_path=None):
    self.number_of_records = number_of_records
    self.output = output_path
    self.input = input_path
    self.hierarchies = hierarchies()
    self.headers = ["workclass", "hours", "education", "age", "g_workclass", "g_hours", "g_education", "g_age", "income", "g_income", "level"]
    self.df = pd.read_csv("adult.csv")
    #self.df = pd.read_csv("/content/drive/MyDrive/Database/input.csv")
    self.preprocess()
    self.dataset, self.state = self.sample_table()
    
  def normalise(self, value):
    #print(type(value))
    if type(value) == type("str"):
      value = value.replace("-", "").replace(" ", "")
      value = value.lower()
    return value 

  def chose_random(self, val):
    if val == "<=50K":
      return random.choices([1, 2], weights=(0.4, 0.6))[0]
    else:
      return random.choices([3, 4, 5], weights=(0.35, 0.35, 0.3))[0]

  def assign_income(self, table):
    table['income'] = table['income'].apply(self.chose_random)
    return table

  def convert_to_numeric(self):
    self.df['g_workclass'] = self.df['g_workclass'].apply(self.convert_workclass)
    self.df['g_education'] = self.df['g_education'].apply(self.convert_education)

  def convert_education(self, education):
    return self.hierarchies.e_map[education]

  def convert_workclass(self, wclass):
    return self.hierarchies.w_map[wclass]

  def preprocess(self):
    #apply the transformation and add the extra columns as need arises
    self.df['workclass'] = self.df['workclass'].str.replace("?", "neverworked")
    self.df['occupation'] = self.df['occupation'].str.replace("?", "No occupation")
    self.df.rename(columns = {'hours.per.week' : 'hours'}, inplace=True)
    self.df['g_age'] = self.df['age']
    self.df['g_income'] = self.df['income']
    self.df['g_education'] = self.df['education']
    self.df['g_hours'] = self.df['hours']
    self.df['g_workclass'] = self.df['workclass']
    self.df = self.assign_income(self.df)
    self.df['level'] = [(0, 0, 0, 0) for i in range(len(self.df.index))]
    for (columnName, columnData) in self.df.iteritems():
      self.df[columnName] = self.df.apply(lambda row : self.normalise(row[columnName]), axis = 1)
    self.convert_to_numeric()

  def sample_table(self):

    state = random.randint(2, 2**32 - 1)
    table = self.df.sample(self.number_of_records, random_state=state)
    sample = pd.concat([table[header] for header in self.headers], axis=1, keys=self.headers)
    sample.to_csv(self.output)
    return sample, state

#This will perform the scoring or each tuple, sort the data and group it

class sac(pre_process_data):
  def __init__(self, input_path, output_path, number_of_records=32560):
    pre_process_data.__init__(self, output_path, number_of_records, input_path=input_path)
    self.input_path = input_path
    self.output_path = output_path
    self.dataset = pd.read_csv(self.input_path, index_col=[0])
    self.w = Counter(self.dataset['workclass'])
    self.h = Counter(self.dataset['hours'])
    self.a = Counter(self.dataset['age'])
    self.e = Counter(self.dataset['education'])

  def score_numeric(self, val):
    return val
  
  def score_workclass(self, node):
    x, y = self.hierarchies.w_score[node]
    return pow((x*x + y*y), 0.5) 

  def score_education(self, node, edu):
    try:
      x, y = self.hierarchies.e_score[node]
      return pow((x*x + y*y), 0.5)
    except:
      print("problem at node ", node, edu)
      return 0
  
  def score_p_workclass(self, w, h, e, a):
    return (self.w[w] + self.h[h] + self.a[a] + self.e[e]) / len(self.df)

  def score_record(self, w, h, e, a, edu):
    #based on probability
    w_score = self.score_workclass(w) / (self.w[w] + 1)
    h_score = self.score_numeric(h) / (self.h[h] + 1)
    e_score = self.score_education(e, edu) / (self.e[e] + 1)
    a_score = self.score_numeric(a) / (self.a[a] + 1)
    record_score = 14 * w_score +  h_score / 8  + 27 * e_score + a_score / 12
    #record_score =  14 * w_score + (max(self.h) - min(self.h)) * h_score + 27 * e_score +  (max(self.a) - min(self.a)) * a_score 
    return record_score
  
  def score(self):
    scores = []
    for row in self.dataset.itertuples():
      score = self.score_record(row.g_workclass, row.g_hours, row.g_education, row.g_age, row.education)
      scores.append(score)
    self.dataset['scores'] = scores
    self.dataset = self.dataset.sort_values(["scores"], ascending=True)
    self.dataset.to_csv(self.output_path)



#This will anonymize the dataset after the scores have been calculated
class k_anonymity:
  def __init__(self, filename, output_path, k):
    self.df = pd.read_csv(filename, index_col=[0])
    self.wclass_lca = dict()
    self.edu_lca = dict()
    self.k = k
    self.output = output_path
    self.load_lca_relations()

  #the lowest common ancestors for all pairs of nodes are loaded from the precomputed pickle file
  def load_lca_relations(self):
    edu = open("education_lca", "rb")
    try:
      self.edu_lca = (pickle.load(edu))
    except EOFError:
      print("Loading from pickle file error")
    edu.close()

    wclass = open("workclass_lca", "rb")
    try:
      self.wclass_lca = (pickle.load(wclass))
    except EOFError:
      print("Loading from pickle file error")
    wclass.close()
  
  def get_node(self, nodes, lca_dict):
    if len(nodes) > 0:
      lca = nodes[0]
      for i in range(1, len(nodes)):
        lca = lca_dict[(lca, nodes[i])] 
      return lca

  def get_lca(self, nodes, choice):
    if choice == "workclass":
      return self.get_node(nodes, self.wclass_lca)
    else:
      return self.get_node(nodes, self.edu_lca)

  def anonymize(self):
    for i in range(0, len(self.df), self.k):
      four_records = self.df.iloc[i : i+self.k , :]
      #does the computation on the 4 chosen records
      age = four_records['g_age']
      hours = four_records['g_hours']
      wclass = list(four_records['g_workclass'])
      edu = list(four_records['g_education'])
    
      wlca = self.get_lca(wclass, "workclass")
      elca = self.get_lca(edu, "education")

      for j in range(i, i+self.k+1):
        try:
          p = (self.df.iloc[j])
          self.df.at[p.name, 'g_ag'] = str(min(age)) + "-" + str(max(age))
          self.df.at[p.name, 'g_h'] = str(min(hours)) + "-" + str(max(hours))
          self.df.at[p.name, 'g_w'] = wlca 
          self.df.at[p.name, 'g_e'] = elca
        except:
          pass
    self.df.drop(["g_age", "g_hours", "g_workclass", "g_education", "level"], inplace=True, axis=1)
    self.df.to_csv(self.output)



def sac_algorithm(number_of_records, k):
    pre_process = pre_process_data("temp_pre_process.csv", number_of_records)
    scored = sac("temp_pre_process.csv", "temp_scored.csv", number_of_records)
    scored.score()
    kanonymize = k_anonymity("temp_scored.csv", "sac_result.csv", k)
    kanonymize.anonymize()
