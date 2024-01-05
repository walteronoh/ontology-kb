import csv

from rdflib import RDF, Graph, Literal, Namespace, URIRef;

# Load ontology
g = Graph()

g.parse("data/entertainment.owl", format="turtle")

# Define namespace
ont_ns = Namespace("http://www.semanticweb.org/walter/ontologies/2024/0/entertainment/")

# Read CSV data
csv_file_path = "data/entertainment.csv"
with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        # Generate unique URI for each individual based on show_id
        individual_uri = URIRef(ont_ns + row["show_id"])

        # Create individual
        g.add((individual_uri, RDF.type, ont_ns.Show))
        g.add((individual_uri, ont_ns.show_id, Literal(row["show_id"])))
        g.add((individual_uri, ont_ns.hasTitle, Literal(row["title"])))
        g.add((individual_uri, ont_ns.hasType, Literal(row["type"])))
        g.add((individual_uri, ont_ns.hasDirector, Literal(row["director"])))
        g.add((individual_uri, ont_ns.hasCast, Literal(row["cast"])))
        g.add((individual_uri, ont_ns.hasRating, Literal(row["rating"])))

# Serialize and print the updated RDF graph
g.serialize( destination="data/entertainment_gen.owl",format="turtle")