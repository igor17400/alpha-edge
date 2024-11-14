import pandas as pd
import numpy as np
import re
import networkx as nx
import pickle


def preprocess_mna_data():
    ticker_to_name = pd.read_csv("../datasets/ticker_to_name.csv")
    ticker_to_sector = pd.read_csv("../datasets/ticker_to_sector.csv")
    mna = pd.read_csv("../datasets/Acquisitions.csv")
    mna = mna.rename(
        columns={
            "Acquired Company": "Child",
            "Acquiring Company": "Parent",
            "Year of acquisition announcement": "Year Acquired",
            "Deal announced on": "Deal Date",
        }
    )

    # Add additional columns if needed
    mna["Location"] = "USA"  # Placeholder, update with actual data if available
    mna["City"] = "Unknown"  # Placeholder, update with actual data if available

    # Create a list to store the results
    results = []

    # Iterate over each row in the mna DataFrame
    for _, mna_row in mna.iterrows():
        parent = mna_row["Parent"]

        # Use a regular expression to match the parent name as a whole word
        match = ticker_to_name[
            ticker_to_name["name"].str.contains(
                r"\b" + re.escape(parent) + r"\b", case=False, na=False
            )
        ]

        # If a match is found, append the combined data to results
        if not match.empty:
            for _, ticker_row in match.iterrows():
                combined_row = {**mna_row, "symbol": ticker_row["symbol"]}
                results.append(combined_row)

    mna_ = pd.DataFrame(results)

    # Merge with ticker_to_sector to get the sector information
    mna_ = mna_.merge(ticker_to_sector, on="symbol", how="left").rename(columns={"sector": "Industry"})

    # Fill missing sectors with "Unknown"
    mna_["Industry"] = mna_["Industry"].fillna("Unknown")

    # Save the updated DataFrame
    mna_.to_csv("../datasets/mna_with_symbols.csv", index=False)


def create_company_graph():
    # Load datasets
    mna = pd.read_csv("../datasets/mna_with_symbols.csv")
    us_market_data = pd.read_csv("../datasets/us_market_data.csv")

    # Initialize graph
    G = nx.DiGraph()

    # Create a dictionary for quick market cap lookup
    market_cap_dict = us_market_data.set_index("symbol")["market_cap"].to_dict()

    for _, row in mna.iterrows():
        # Get the symbol for the parent company
        parent_symbol = row.get("symbol", None)

        # Get the market cap using the symbol
        market_cap = market_cap_dict.get(parent_symbol, 0)

        # Add parent node with attributes
        G.add_node(
            row["Parent"],
            Industry=row.get("Industry", "Unknown"),
            Market_Cap=market_cap,
            Ticker=parent_symbol,
        )

        # Add child node with attributes
        G.add_node(
            row["Child"],
            Industry=row.get("Industry", "Unknown"),
            Year_Acquired=row.get("Year Acquired", 0),
            Deal_Date=row.get("Deal Date", 0),
            Parent=row["Parent"],
        )

        # Add edge from parent to child
        if row["Parent"]:
            G.add_edge(row["Parent"], row["Child"])

    # Save the graph to a file
    with open("../graph_objs/company_graph.pkl", "wb") as f:
        pickle.dump(G, f)


if __name__ == "__main__":
    preprocess_mna_data()
    create_company_graph()
