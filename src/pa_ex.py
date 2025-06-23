import pysparql_anything as sa

engine = sa.SparqlAnything()

engine.run(query='queries/accidents.sparql', output='kg/accidents.nt', format='nt')
