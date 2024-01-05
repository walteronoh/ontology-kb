from flask import Flask, render_template, request
from rdflib import RDF, Graph, Namespace
from rdflib.plugins.sparql import prepareQuery

app = Flask(__name__)

# Load the ontology
g = Graph()
g.parse("data/entertainment_gen.owl", format="turtle")

# Define namespaces
ont_ns = Namespace("http://www.semanticweb.org/walter/ontologies/2024/0/entertainment/")

def search_kb_by_keyword(keyword):
    query_str = f"""
        SELECT ?show ?title
        WHERE {{
            ?show rdf:type/rdfs:subClassOf* <{ont_ns.Show}> .
            ?show <{ont_ns.hasTitle}> ?title .
            FILTER regex(str(?title), "{keyword}", "i")
        }}
    """
    query = prepareQuery(query_str, initNs={"rdf": RDF, "rdfs": ont_ns})
    results = g.query(query)
   
    # Return a list of results
    return [{"show": row.show, "title": row.title} for row in results]

def search_inference_by_option(option):
    if option == "Q1":
        return search_inference_Q1()
    if option == "Q2":
        return search_inference_Q2()
    return[]

def search_inference_Q1():
    query_str = f"""
        SELECT ?show ?title ?director
        WHERE {{
            ?show rdf:type/rdfs:subClassOf* <{ont_ns.Show}> .
            ?show <{ont_ns.hasTitle}> ?title .
            ?show <{ont_ns.hasDirector}> ?director .
        }}
    """
    query = prepareQuery(query_str, initNs={"rdf": RDF, "rdfs": ont_ns})
    results = g.query(query)

    return [{"show": row.show, "title": row.title, "director": row.director} for row in results]

def search_inference_Q2():
    query_str = f"""
        SELECT ?show ?title
        WHERE {{
            ?show rdf:type/rdfs:subClassOf* <{ont_ns.Show}> .
            ?show <{ont_ns.hasTitle}> ?title .
            ?show <{ont_ns.hasCast}> ?cast .
        }}
    """
    query = prepareQuery(query_str, initNs={"rdf": RDF, "rdfs": ont_ns})
    results = g.query(query)

    return [{"show": row.show, "title": row.title} for row in results]


@app.route('/')
def index():
    return render_template('index.html')

# Interface for displaying KB results
@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    return render_template("index.html", results=search_kb_by_keyword(keyword))

# Interface for displaying inference results
@app.route("/inference", methods=["POST"])
def inference():
    option = request.form["inference_option"]
    return render_template("index.html", results=search_inference_by_option(option))