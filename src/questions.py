import requests
from collections import defaultdict



class KGRetriever:
  def __init__(self, endpoint):
      self.endpoint = "https://kgccc.di.unito.it/sparql/nudging"
      self.categories = ["ndg:Women","ndg:Men","ndg:Minors","ndg:ForeignWomen","ndg:ForeignMen","ndg:Family","ndg:Seniors"]
      self.years = ["ndg:2012", "ndg:2013", "ndg:2014", "ndg:2015", "ndg:2016", "ndg:2017", "ndg:2018", "ndg:2019"]
      self.census = [f"ndg:{i}" for i in range(1,3851)]


  def question_1(self,category='ndg:Women',year='ndg:2017'):

    """
    From 2012 to 2019 the population in Turin has decreased. Considering all the census, does this decrease affect all the demographics? Which category is more affected and which one is less affected?
    """
    question = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
    PREFIX ndg: <https://purl.archive.org/nudging#>
    SELECT DISTINCT ?b_total ?district WHERE {{
    ?x a ndg:SocialContext;
    dul:isSettingFor ?a, ?b,?c, ?district.
    ?b a {category}; ndg:total ?b_total.
    FILTER(?a={year}) . 
    
    }}
    """
    req = requests.get(self.endpoint, params={"query": question, "format": "json"})
    if req.status_code != 200:
        return f"Query failed with status code {req.status_code}"
    else:
        all_res = []
        res = req.json()
        if not res['results']['bindings']:
          return "No results found for the given census."
        else:
          for item in res['results']['bindings']:

            res = {'category':category,'year':year,'district':item['district']['value'],'number':item['b_total']['value']}
            all_res.append(res)
          return all_res
        
  def question_2(self,year='ndg:2019'):
    """
    Is there any correlation between the number of foreigners and the number of families? 
    Can you spot whether a high number of foreigners in a census means a high number of components in families?
    """

    question = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
    PREFIX ndg: <https://purl.archive.org/nudging#>
    SELECT ?foreigners ?dist ?fam_total WHERE {{
      ?sit a ndg:SocialContext ; dul:isSettingFor ?fowo,?fome, ?fam, ?y, ?dist, ?cens.
      ?cens a ndg:Census; ndg:hasSuburb ?dist .
     ?fowo a ndg:ForeignWomen; ndg:total ?tot_fowo . 
      ?fome a ndg:ForeignMen; ndg:total ?tot_fome .
     
     BIND((?tot_fowo+?tot_fome) as ?foreigners) .
    
      ?fam a ndg:Family; ndg:average ?fam_total .

      FILTER(?y={year}) .
    }}

    ORDER BY DESC(?total)


    """
    req = requests.get(self.endpoint, params={"query": question, "format": "json"})
    if req.status_code != 200:
      return f"Query failed with status code {req.status_code}"
    else:
      all_res = []
      res = req.json()
      if not res['results']['bindings']:
        return "No results found for the given census."
      else:
        for item in res['results']['bindings']:
          res = {'district':item['dist']['value'],
                 'year':year,
                 'foreigners':item['foreigners']['value'],
                 'family_components':item['fam_total']['value']}
          all_res.append(res)
        return all_res

      

  def question_3(self,census='ndg:1',year='ndg:2019'):
    """
    Does a high number of females in a census mean a high number of minors in that census?
    """
    
    question = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
    PREFIX ndg: <https://purl.archive.org/nudging#>
    SELECT ?tot_m ?tot_w ?tot_minors ?census ?street  WHERE {{
    ?sit a ndg:SocialContext ; dul:isSettingFor ?wo, ?min, ?me, ?census, ?y .
    FILTER(?y={year}) .
    ?wo a ndg:Women; ndg:total ?tot_w . 
    ?me a ndg:Men; ndg:total ?tot_m .
      ?min a ndg:Minors; ndg:total ?tot_minors .
      ?census ndg:hasStreet ?str .
      ?str rdfs:label ?street .
      FILTER(?census={census}) .

    }} ORDER BY DESC(?tot_minors)
    """
    req = requests.get(self.endpoint, params={"query": question, "format": "json"})
    if req.status_code != 200:
      return f"Query failed with status code {req.status_code}"
    else:
        all_res = []
        res = req.json()
        if not res['results']['bindings']:
          return "No results found for the given census."
        else:
          for item in res['results']['bindings']:
            
            tot_m = item['tot_m']['value']
            tot_w = item['tot_w']['value']
            tot_minors = item['tot_minors']['value']
            census = item['census']['value']
            street = item['street']['value']
            res = {'census':census,'street':street,'n_men':tot_m,'n_women':tot_w,'n_minors':tot_minors,'year':year}
            all_res.append(res)
          
          #all_res = self.__sum_elements(all_res)
          return all_res
           
  
  def question_10(self,year='ndg:2019'):
    """
    Which districts experienced the largest changes (either increase or decrease) in the percentage of minors between 2012 and 2019?
    """
    question = f""" 
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
      PREFIX ndg: <https://purl.archive.org/nudging#>

      SELECT DISTINCT ?population ?district  ?accidents WHERE {{    ?sit a ndg:SocialContext; dul:isSettingFor ?cens,?wo,?men,?y, ?district, ?accidents.

      ?y a ndg:Year .
      FILTER(?y={year}) .

      ?wo a ndg:Women; ndg:total ?tot_w . 
      ?men a ndg:Men; ndg:total ?tot_m .


      ?cens ndg:accidents ?accidents; ndg:hasSuburb ?district .
      BIND((?tot_w+?tot_m) as ?population) .




      }}      """
    
    req = requests.get(self.endpoint, params={"query": question, "format": "json"})
    if req.status_code != 200:
      return f"Query failed with status code {req.status_code}"
    else:
      all_res = []
      res = req.json()
      if not res['results']['bindings']:
        return "No results found for the given census."
      else:
        for item in res['results']['bindings']:
          res = {'population':item['population']['value'],'year':year,'accidents':item['accidents']['value']}
          all_res.append(res)
        return all_res

  def question_13(self,year='ndg:2019'):
      """
      Does a high total population in a district imply a high number of total accidents?
      """
      question = f""" 
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
      PREFIX ndg: <https://purl.archive.org/nudging#>

      SELECT DISTINCT ?population ?district  ?accidents WHERE {{    ?sit a ndg:SocialContext; dul:isSettingFor ?cens,?wo,?men,?y, ?district, ?accidents.

      ?y a ndg:Year .
      FILTER(?y={year}) .

      ?wo a ndg:Women; ndg:total ?tot_w . 
      ?men a ndg:Men; ndg:total ?tot_m .


      ?cens ndg:accidents ?accidents; ndg:hasSuburb ?district .
      BIND((?tot_w+?tot_m) as ?population) .




      }}      """
      req = requests.get(self.endpoint, params={"query": question, "format": "json"})
      if req.status_code != 200:
        return f"Query failed with status code {req.status_code}"
      else:
        all_res = []
        res = req.json()
        if not res['results']['bindings']:
          return "No results found for the given census."
        else:
          for item in res['results']['bindings']:
            res = {'population':item['population']['value'],'year':year,'accidents':item['accidents']['value']}
            all_res.append(res)
          return all_res

  def question_17(self,year='ndg:2019'):
      """
      Which district has the highest number of bus/tram stops?
      """
      question = f"""
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
      PREFIX ndg: <https://purl.archive.org/nudging#>

      SELECT DISTINCT ?district ?n_bus_stop WHERE {{
      ?sit a ndg:SocialContext; dul:isSettingFor ?cens, ?y .

      ?y a ndg:Year .
      FILTER(?y={year}) .

      ?cens ndg:hasSuburb ?district; ndg:busStopNumber ?n_bus_stop .

      }} ORDER BY DESC(?n_bus_stop)
        """

      req = requests.get(self.endpoint, params={"query": question, "format": "json"})
      if req.status_code != 200:
        return f"Query failed with status code {req.status_code}"
      else:
        all_res = []
        res = req.json()
        if not res['results']['bindings']:
          return "No results found for the given census."
        else:
          for item in res['results']['bindings']:
            res = {'district':item['district']['value'],'year':year,'bus_stop':item['n_bus_stop']['value']}
            all_res.append(res)
          return all_res



# Example usage:
kg_retriever = KGRetriever("https://kgccc.di.unito.it/sparql/nudging")



'''# given a group, a census, and a year, this returns the number of people in that group in the censu

print(kg_retriever.question_1(category='ndg:Women',year='ndg:2012',census='ndg:34'))

# this returns the number of men, women, and minors in a given census and year
print(kg_retriever.question_3(census='ndg:1', year='ndg:2019'))+
'''
