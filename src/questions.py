import requests



class KGRetriever:
  def __init__(self, endpoint):
      self.endpoint = "https://kgccc.di.unito.it/sparql/nudging"
      self.categories = ["ndg:Women","ndg:Men","ndg:Minors","ndg:ForeignWomen","ndg:ForeignMen","ndg:Family","ndg:Seniors"]
      self.years = ["ndg:2012", "ndg:2013", "ndg:2014", "ndg:2015", "ndg:2016", "ndg:2017", "ndg:2018", "ndg:2019"]
      self.census = [f"ndg:{i}" for i in range(1,3851)]


  def question_1(self,category='ndg:Women',year='ndg:2017',census="ndg:1"):

    """
    From 2012 to 2019 the population in Turin has decreased. Considering all the census, does this decrease affect all the demographics? Which category is more affected and which one is less affected?
    """
    question = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
    PREFIX ndg: <https://purl.archive.org/nudging#>
    SELECT (SUM(?b_total) as ?counted) WHERE {{
    ?x a ndg:SocialContext;
    dul:isSettingFor ?a, ?b,?c .
    ?b a {category}; ndg:total ?b_total.
    FILTER(?a={year}) . 
    FILTER(?c={census}) .
    
    }}
    """
    req = requests.get(endpoint, params={"query": question, "format": "json"})
    if req.status_code != 200:
        return f"Query failed with status code {req.status_code}"
    else:
        return req.json()

  def question_2(self,year='ndg:2019'):
    """
    Does a high number of females in a census mean a high number of minors in that census?
    """

    question = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
    PREFIX ndg: <https://purl.archive.org/nudging#>
    SELECT ((?tot_fowo + ?tot_fome)/(?tot_m+?tot_w) AS ?total) ((?tot_m+?tot_w)/?fam_total AS ?tot_fam)  WHERE {{
      ?sit a ndg:SocialContext ; dul:isSettingFor ?wo, ?men, ?fowo,?fome, ?fam, ?y.
    ?fowo a ndg:ForeignWomen; ndg:total ?tot_fowo . 
      ?fome a ndg:ForeignMen; ndg:total ?tot_fome .
    ?fam a ndg:Family; ndg:total ?fam_total .
      ?wo a ndg:Women; ndg:total ?tot_w . 
      ?men a ndg:Men; ndg:total ?tot_m .
    ?fam a ndg:Family; ndg:total ?fam_total .
      
      FILTER(?y={year}) .
    }}

    ORDER BY DESC(?total)


    """
    req = requests.get(endpoint, params={"query": question, "format": "json"})
    if req.status_code != 200:
      return f"Query failed with status code {req.status_code}"
    else:
      return req.json()

      

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
    req = requests.get(endpoint, params={"query": question, "format": "json"})
    if req.status_code != 200:
      return f"Query failed with status code {req.status_code}"
    else:
      return req.json()

  def question_13(self,year='ndg:2019'):
      """
      Does a high total population in a district imply a high number of total accidents?
      """
      question = f""" 
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX dul: <http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
      PREFIX ndg: <https://purl.archive.org/nudging#>

      SELECT DISTINCT ((?tot_w+?tot_m) AS ?population) ?cens ?street ?accidents WHERE {{    ?sit a ndg:SocialContext; dul:isSettingFor ?cens,?wo,?men,?y.

      ?y a ndg:Year .
      FILTER(?y={year}) .

      ?wo a ndg:Women; ndg:total ?tot_w . 
      ?men a ndg:Men; ndg:total ?tot_m .


      ?cens ndg:accidents ?accidents; ndg:hasStreet ?str .

      ?str rdfs:label ?street



      }} ORDER BY DESC(?accidents)
      """
      req = requests.get(endpoint, params={"query": question, "format": "json"})
      if req.status_code != 200:
        return f"Query failed with status code {req.status_code}"
      else:
        return req.json()

  def question_17(self,year='ndg:2019'):
      """
      Which district has the highest number of bus/tram stops in the census?
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

      req = requests.get(endpoint, params={"query": question, "format": "json"})
      if req.status_code != 200:
        return f"Query failed with status code {req.status_code}"
      else:
        return req.json()

