from escape_helpers import sparql_escape_string, sparql_escape_uri
from helpers import query, update
from string import Template

def query_enrichable_descriptions():
    query_results = query("""PREFIX dct: <http://purl.org/dc/terms/>
SELECT ?thing ?description
WHERE {
        ?thing dct:description ?description.
        FILTER(lang(?description) = "nl")
        FILTER NOT EXISTS {
          ?thing dct:description ?otherDescription.
          FILTER( lang(?otherDescription) = "en" )
        }
}""")

    return [(binding["thing"]["value"],
             binding["description"]["value"])
            for binding in query_results["results"]["bindings"]]

def update_enrichable_descriptions(tuples):
    update_template = Template("""PREFIX dct: <http://purl.org/dc/terms/>
      INSERT DATA {
        GRAPH <http://mu.semte.ch/application> {
          $triples
        }
      }""")

    escaped_tuples = [(sparql_escape_uri(source), sparql_escape_string(translation))
                      for (source, translation) in tuples]

    triples = ". ".join([
        f"{source} dct:description {translation}@en"
        for (source, translation) in escaped_tuples
    ])

    update_query = update_template.substitute( triples=triples )
    update(update_query)
