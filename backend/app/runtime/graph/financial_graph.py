from neo4j import GraphDatabase

class FinancialKnowledgeGraph:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "liceu123")
        )

    def create_supplier_risk_relation(
        self,
        supplier,
        risk_score
    ):
        with self.driver.session() as session:

            session.run("""
            MERGE (s:Supplier {id:$supplier})
            MERGE (r:Risk {score:$score})
            MERGE (s)-[:HAS_RISK]->(r)
            """,
            supplier=supplier,
            score=risk_score)

graph = FinancialKnowledgeGraph()
