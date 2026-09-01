import sqlite3
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer()
default_database_path = Path.cwd() / "out.db"


@app.command()
def initialize(
        adjacency_list_file: Path,
        output_database_file: Path = default_database_path,
        labels_file: Optional[Path] = None
):
    """
    Reads an adjacency list file and creates a graph database from it.
    If a labels file is supplied, it is read and the labels for the edges are created in insertion order.

    :param adjacency_list_file: The adjacency list to read.
    :param output_database_file: The output database file.
    :param labels_file: An optional edge label file.
    """

    sources, targets = [], []

    with adjacency_list_file.open() as fp:
        for line in fp:
            edges = line.split(" ")
            source = edges[0].strip()

            for target in edges[1:]:
                sources.append(source)
                targets.append(target.strip())

    if labels_file is not None:
        with labels_file.open() as fp:
            labels = [line.strip() for line in fp.readlines()]

            if len(labels) != len(sources):
                raise ValueError(f"Trying to map {len(labels)} onto {len(sources)} edges!")

    con = sqlite3.connect(output_database_file)
    cur = con.cursor()

    cur.executescript("""
        CREATE TABLE edge(source TEXT NOT NULL, target TEXT NOT NULL, label TEXT);
        CREATE INDEX edge_source ON edge(source);
        CREATE INDEX edge_target ON edge(target);
    """)

    con.commit()

    query = "INSERT INTO edge(source, target, label) VALUES (?, ?, ?)" if labels_file is not None else "INSERT INTO edge(source, target) VALUES (?, ?)"
    edges = zip(sources, targets, labels) if labels_file is not None else zip(sources, targets)

    cur.executemany(query, edges)
    con.commit()


@app.command()
def query(node: str, output_database_file: Path = default_database_path, label: Optional[str] = None):
    """
    Reads a graph database and returns all nodes reachable from the given node.

    :param node: The start node.
    :param output_database_file: The graph database to read.
    :param label: Optional label to filter for.
    :return: A list of nodes reachable from the start node.
    """

    con = sqlite3.connect(output_database_file)
    cur = con.cursor()

    if label is not None:
        res = cur.execute("""
        WITH RECURSIVE nodes(x) AS (
            SELECT ?
            UNION
            SELECT source FROM edge JOIN nodes ON target=x WHERE label LIKE ?
            UNION
            SELECT target FROM edge JOIN nodes ON source=x WHERE label LIKE ?
        )
        SELECT x FROM nodes;                          
        """, (node.strip(), label.strip(), label.strip(),))
    else:
        res = cur.execute("""
        WITH RECURSIVE nodes(x) AS (
            SELECT ?
            UNION
            SELECT source FROM edge JOIN nodes ON target=x
            UNION
            SELECT target FROM edge JOIN nodes ON source=x
        )
        SELECT x FROM nodes;
        """, (node.strip(),))
    targets = res.fetchall()

    print(f"Nodes that can be reached from {node.strip()}")
    print(targets)


if __name__ == "__main__":
    app()
