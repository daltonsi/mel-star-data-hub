import networkx as nx
import matplotlib.pyplot as plt
import textwrap
import numpy as np
import pandas as pd


# Updated SDOH Categories Dataset with cross-category connections
sdoh_data = {
    "Primary Categories": {
        # "Amenities": [
        #     "Recreational Establishments", 
        #     "Arts, Entertainment",
        #     "Personal Care Services and Laundromats",
        #     "Eating and Drinking Places",
        #     "Parks",
        #     "Religious, Civic and Social Organizations"
        # ],
        # "Arts": [
        #     "Arts, Entertainment", 
        # ],
        # "Civics": [
        #     "Post Offices and Banks", 
        #     "Religious, Civic and Social Organizations",
        #     "Social Services",
        #     "Voter Registration, Turnout, and Partisanship"
        # ],
        # "COVID-19": [
        #     "COVID-19", 
        #     "Demographics"
        # ],
        "Crime": [
            "Crimes", 
            "Law Enforcement"
        ],
        # "Demographics": [
        #     "Mortgages", 
        #     "Essential Workers",
        #     "Neighborhood-School Gap",
        #     "Socioeconomic Status and Demographic Characterisitics",
        #     "Urbanicity"
        # ],        
        # "Education": [
        #     "Education and Training Services", 
        #     "Neighborhood-School Gap",
        #     "School District Characterisitics and School Counts"
        # ],
        # "Food": [
        #     "Dollar Stores", 
        #     "Eating and Drinking Places",
        #     "Grocery Stores"
        # ],
        # "Government": [
        #     "Mortgages", 
        #     "Post Offices and Banks",
        #     "Social Serivces",
        #     "Voter Registration, Turnout, and Partisanship"
        # ],
        "Healtcare": [
            "Health Care Services", 
        ],
      #   "Housing": [
      #       "Mortgages", 
      #   ],
      #   "Internet": [
      #       "Broadband Internet Availability, Speed, and Adoption", 
      #       "Internet Access",
      #   ],
      # "Land Cover": [
      #       "Land Cover", 
      #       "Parks", 
      #       "Polluting Sites", 
      #       "Primary and Secondary Roads", 
      #       "Street Connectivity", 
      #       "Urbanicity", 
      #   ],
      # "Outdoors": [
      #       "Land Cover",
      #       "Parks",
      #       "Polluting Sites",
      #       "Weather" 
      #   ],
      # "Public Transit": [
      #       "Public Transit Stops",
      #   ],
      # "Social Serivces": [
      #       "Social Services",
      #   ],
      # "Stores": [
      #       "Recreational Establishments",
      #       "Dollar Stores",
      #       "Grocery Stores",
      #       "Liquor, Tobacco, Cannabis, Vape and Convenience Stores",
      #       "Personal Care Services and Laundromats",
      #       "Retail Establishments"
      #   ],
      # "Traffic": [
      #       "Primary annd Secondary Roads",
      #       "Public Transit Stops",
      #       "Street Connectivity",
      #       "Traffic Volume"
      #   ],
    },
    "Cross-Category Connections": [
        # {"category": "Recreational Establishments", "primary_categories": ["Amenities", "Stores"]},
        # {"category": "Arts, Entertainment", "primary_categories": ["Amenities", "Arts"]},
        # {"category": "Eating and Drinking Places", "primary_categories": ["Amenities", "Food"]},
        # {"category": "Parks", "primary_categories": ["Amenities", "Land Cover", "Outdoors"]},
        # {"category": "Personal Care Services and Laundromats", "primary_categories": ["Amenities", "Stores"]},
        # {"category": "Religious, Civic and Social Organizations", "primary_categories": ["Amenities", "Civics"]},
        # {"category": "Post Offices and Banks", "primary_categories": ["Civics", "Government"]},
        # {"category": "Social Services", "primary_categories": ["Civics", "Government","Social Services"]},
        # {"category": "Voter Registration, Turnout, and Partisanship", "primary_categories": ["Civics", "Government"]},
        # {"category": "Essential Workers", "primary_categories": ["COVID-19","Demographics"]},
        {"category": "Crimes", "primary_categories": ["Crime"]},
        {"category": "Law Enforcement", "primary_categories": ["Crime"]},
        # {"category": "Mortgages", "primary_categories": ["Demographics", "Government","Housing"]},
        # {"category": "Neighborhood-School Gap", "primary_categories": ["Demographics", "Education"]},
        # {"category": "Socioeconomic Status and Demographic Characterisitics", "primary_categories": ["Demographics"]},
        # {"category": "Urbanicity", "primary_categories": ["Demographics", "Land Cover"]},
        # {"category": "Education and Training Services", "primary_categories": ["Education"]},
        # {"category": "Neighborhood-School Gap", "primary_categories": ["Demographics", "Education"]},
        # {"category": "School District Characterisitics and School Counts", "primary_categories": ["Education"]},
        # {"category": "Dollar Stores", "primary_categories": ["Food", "Stores"]},
        # {"category": "Grocery Stores", "primary_categories": ["Food", "Stores"]},
        {"category": "Health Care Services", "primary_categories": ["Healtcare"]},
        # {"category": "Broadband Internet Availability, Speed, and Adoption", "primary_categories": ["Internet"]},
        # {"category": "Internet Access", "primary_categories": ["Internet"]},
        # {"category": "Land Cover", "primary_categories": ["Land Cover", "Outdoors"]},
        # {"category": "Polluting Sites", "primary_categories": ["Land Cover","Outdoors"]},
        # {"category": "Primary and Secondary Roads", "primary_categories": ["Land Cover","Traffic"]},
        # {"category": "Street Connectivity", "primary_categories": ["Land Cover", "Traffic"]},
        # {"category": "Urbanicity", "primary_categories": ["Demographics", "Land Cover"]},
        # {"category": "Weather", "primary_categories": ["Outdoors"]},
        # {"category": "Public Transit Stops", "primary_categories": ["Public Transit", "Traffic"]},
        # {"category": "Liquor, Tobacco, Cannabis, Vape and Convenience Stores", "primary_categories": ["Stores"]},
        # {"category": "Retail Establishments", "primary_categories": ["Stores"]},
        # {"category": "Traffic Volume", "primary_categories": ["Traffic"]}
    ]
}

# Create Network Graph
G = nx.Graph()

# Add primary categories as central nodes
for primary_category in sdoh_data["Primary Categories"]:
    G.add_node(primary_category, node_type="primary")
    
    # Add secondary categories for each primary category
    for secondary_category in sdoh_data["Primary Categories"][primary_category]:
        G.add_node(secondary_category, node_type="secondary")
        G.add_edge(primary_category, secondary_category)

# Add cross-category connections
for cross_connection in sdoh_data["Cross-Category Connections"]:
    category = cross_connection["category"]
    primary_categories = cross_connection["primary_categories"]
    
    # Connect the secondary category to multiple primary categories
    for primary_cat in primary_categories:
        G.add_edge(primary_cat, category)



df = pd.DataFrame(index=G.nodes(), columns=G.nodes())
for row, data in nx.shortest_path_length(G):
    for col, dist in data.items():
        df.loc[row,col] = dist

df = df.fillna(df.max().max() ** 0.5)

print(df)
# Visualization
plt.figure(figsize=(20, 15))
pos = nx.kamada_kawai_layout(G, dist=df.to_dict())#, weight=weight_matrix)#, dist=dist)#, k=1.0)  # positions for all nodes
#pos = nx.spring_layout(G, k=0.9)


# Wrap long labels
def wrap_labels(labels, width=15):
    return {node: '\n'.join(textwrap.wrap(label, width)) for node, label in labels.items()}

# Prepare labels
labels = {node: node for node in G.nodes()}
wrapped_labels = wrap_labels(labels)

# Draw primary nodes
primary_nodes = [node for node, attrs in G.nodes(data=True) if attrs['node_type'] == 'primary']
nx.draw_networkx_nodes(G, pos, 
                       nodelist=primary_nodes, 
                       node_color='lightblue', 
                       node_size=6000, 
                       alpha=1)

# Draw secondary nodes
secondary_nodes = [node for node, attrs in G.nodes(data=True) if attrs['node_type'] == 'secondary']
nx.draw_networkx_nodes(G, pos, 
                       nodelist=secondary_nodes, 
                       node_color='lightgreen', 
                       node_size=3000, 
                       alpha=0.9)

# Draw edges
nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5)

# Add wrapped labels
#nx.draw_networkx_labels(G, pos, labels=wrapped_labels, font_size=9, font_weight="bold")
# Custom label drawing with variable font sizes
for node, (x, y) in pos.items():
    node_type = G.nodes[node]['node_type']
    font_size = 12 if node_type == 'primary' else 8
    font_weight = 'bold'
    plt.text(x, y, wrapped_labels[node], 
             horizontalalignment='center', 
             verticalalignment='center', 
             fontsize=font_size, 
             fontweight=font_weight)



plt.title("Social Determinants of Health (SDOH) Network", fontsize=24)
plt.axis('off')
plt.tight_layout()
plt.savefig('sdoh_graph.png')
plt.show()