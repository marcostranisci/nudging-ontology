import pysparql_anything as sa

engine = sa.SparqlAnything()

engine.run(query='queries/demographic_query.sparql', output='kg/demographics.nt', format='nt')
