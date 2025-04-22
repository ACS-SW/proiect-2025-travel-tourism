import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD

df = pd.read_csv("dataset_tourism.csv")

EX = Namespace("http://example.org/tourism#")
g = Graph()
g.bind("ex", EX)

for _, row in df.iterrows():
    city_uri = URIRef(EX + row["City"].replace(" ", "_"))

    g.add((city_uri, RDF.type, EX.City))
    g.add((city_uri, EX.country, Literal(row["Country"], datatype=XSD.string)))
    g.add((city_uri, EX.accommodationType, Literal(row["Accommodation type"], datatype=XSD.string)))
    g.add((city_uri, EX.accommodationCost, Literal(row["Accommodation cost"], datatype=XSD.float)))
    g.add((city_uri, EX.transportationType, Literal(row["Transportation type"], datatype=XSD.string)))
    g.add((city_uri, EX.transportationCost, Literal(row["Transportation cost"], datatype=XSD.float)))
    g.add((city_uri, EX.category, Literal(row["Category"], datatype=XSD.string)))
    g.add((city_uri, EX.costOfLivingIndex, Literal(row["Cost of Living Index"], datatype=XSD.float)))
    g.add((city_uri, EX.rentIndex, Literal(row["Rent Index"], datatype=XSD.float)))
    g.add((city_uri, EX.costOfLivingPlusRentIndex, Literal(row["Cost of Living Plus Rent Index"], datatype=XSD.float)))
    g.add((city_uri, EX.groceriesIndex, Literal(row["Groceries Index"], datatype=XSD.float)))
    g.add((city_uri, EX.restaurantPriceIndex, Literal(row["Restaurant Price Index"], datatype=XSD.float)))
    g.add((city_uri, EX.localPurchasingPowerIndex, Literal(row["Local Purchasing Power Index"], datatype=XSD.float)))

    try:
        attractions = eval(row["Attractions"]) if isinstance(row["Attractions"], str) else []
        # print(f"{row['City']} -> {attractions}")

        for attr in attractions:
            attr_uri_safe = attr.strip().replace(" ", "_").replace(",", "")
            attraction_uri = URIRef(EX + attr_uri_safe)
            # labels for attractions
            g.add((attraction_uri, RDFS.label, Literal(attr, datatype=XSD.string)))
            g.add((attraction_uri, RDF.type, EX.Attraction))
            g.add((city_uri, EX.hasAttraction, attraction_uri))
    except Exception as e:
        pass

g.serialize(destination="tourism_data_generated.ttl", format="turtle")
g.serialize(destination="tourism_data_generated.rdf", format="xml")
g.serialize(destination="tourism_data_generated.owl", format="xml")
