import asyncio

from backend.app.federation.authority.runtime import FederationAuthority

async def bootstrap():

    authority = FederationAuthority()

    await authority.connect()

    await authority.register()

if __name__ == "__main__":
    asyncio.run(bootstrap())
