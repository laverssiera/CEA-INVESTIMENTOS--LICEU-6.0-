from neo4j import GraphDatabase

from backend.app.federation.config import settings

driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

class FinancialKnowledgeGraph:

    @staticmethod
    def register_asset(
        asset_name,
        asset_type,
        strategic_value
    ):

        query = """

        MERGE (a:FinancialAsset {
            name: $asset_name
        })

        SET
            a.asset_type = $asset_type,
            a.strategic_value = $strategic_value

        """

        with driver.session() as session:

            session.run(
                query,
                asset_name=asset_name,
                asset_type=asset_type,
                strategic_value=strategic_value
            )
