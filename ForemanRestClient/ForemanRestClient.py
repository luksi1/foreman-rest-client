#!/usr/bin/python3.4

import requests
import json
import sys
import re
from RestClient import RestClient

class ForemanRestClient(RestClient.RestClient):

  def __init__(self, username, password, base_url, **kvargs):
    super().__init__(username, password)
    self.api = kvargs.get("api", 'v2')
    self.domain = kvargs.get("domain", None)
    
    if self.api is 'v2':
      self.base_url = base_url + "/api/v2/"
    else:
      self.base_url = base_url + "/api/"
      
  def __get_results(self, path):
    json_data = super().get_data(self.base_url + path)
    results_json = json.loads(json_data)
    results = results_json['results']
    return results
  
  def __get_puppetclass_ids(self):
      
    results = self.__get_results("puppetclasses")
    ids = []
    for r in results['role']:
      ids.append(r['id'])
    return ids

  def __get_puppetclass_id_by_name(self, puppetclass):

     prog = re.compile(re.escape(puppetclass.lower()))
     results = self.__get_results("puppetclasses")
     hostgroup_id = None
     ids = {}
     for r in results['profile']:
         name = r['name']
         if prog.search(name):
             ids[name] = r['id']

     if len(ids.keys()) >= 2:
       return ids
     elif len(ids.keys()) == 1:
       return ids[0]
     else:
       print("Could not find hostname " + puppetclass)

  def __get_hostgroup_id_by_name(self, hostgroup_name):
    prog = re.compile(re.escape(hostgroup_name))
    results = self.__get_results("hostgroups")
    hostgroup_id = None
    ids = []
    for r in results:
        if prog.search(r['title']):
            ids.append(r['id'])

    if len(ids) >= 2:
       return ids
    elif len(ids) == 1:
        return ids[0]
    else:
        print("Could not find hostname " + hostname)
        
  def __get_parent_id_by_name(self, parent):
    prog = re.compile(r'^' + re.escape(parent))
    print(parent)
    results = self.__get_results("hostgroups")
    hostgroup_id = None
    ids = []
    for r in results:
        name = r['title']
        if re.search(r'/', name):
           continue
           print(r['title'])
        if prog.search(name):
           ids.append(r['id'])

    if len(ids) > 1:
       print("Your result returned more than one element. Try refining your search")
       sys.exit(2)
    elif len(ids) < 1:
       print("Your result returned no elements. Try refining your search")
       sys.exit(2)

    return ids[0]

  def __get_host_id_by_name(self, hostname):
    prog = re.compile(re.escape(hostname))
    results = self.__get_results("hosts")
    
    ids = []
    for r in results:
        if prog.search(r['name']):
            ids.append(r['id'])

    if len(ids) >= 2:
       return ids
    elif len(ids) == 1:
        return ids[0]
    else:
        print("Could not find hostname " + hostname)

  def __get_environment_id_by_name(self, environment):
    prog = re.compile(re.escape(environment))
    results = self.__get_results("environments")
    ids = []
    
    for r in results:
      name = r['name']
      if prog.search(name):
         ids.append(r['id'])
    
    if len(ids) > 1:
      print("Your result returned more than one entry. Try refining your query")
      sys.exit(2)

    return ids[0]

  def bulk_delete_puppet_classes(self):
    for i in __get_puppet_class_ids():
      super().delete_data(self.base_url + "puppetclasses" + "/" + str(i))

  def apply_hostgroup(self, hostname, hostgroup_name):
    my_url = self.base_url + "hosts/" + str(self.__get_host_id_by_name(hostname))
    print(my_url)
    payload = {'host': {'hostgroup_id': self.__get_hostgroup_id_by_name(hostgroup_name) }}
    print(payload)
    text = super().put_data(my_url, payload)
    print(text)

  def new_hostgroup(self, parent, environment, hostgroup_name):
    my_url = self.base_url + "/hostgroups"

    payload = {'hostgroup': {'name': hostgroup_name, 'parent_id': self.__get_parent_id_by_name(parent), 'environment_id': self.__get_environment_id_by_name(environment)}}
    print(payload)
    text = super().post_data(my_url, payload)
    print(text)
