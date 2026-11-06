from elasticsearch import AsyncElasticsearch
from app.config import setting

es_client: AsyncElasticsearch | None = None

async def init_elastic():
    global es_client
    es_client = AsyncElasticsearch(hosts=[setting.ELASTICSEARCH_URL])
    
    if not await es_client.ping():
        raise RuntimeError("Elasticsearch is not responding")
    print("ElastcSearch is successfully intialized")
    
async def close_elastic():
    global es_client
    if es_client:
        await es_client.close()
        es_client = None

def get_elastic()-> AsyncElasticsearch:
    if es_client is None:
        raise RuntimeError("Elasticsearch is not intialized")
    return es_client

async def add_products_index():
    es = get_elastic()
    service = "services"
    if await es.indices.exists(index="services"):
        print("The services already exists")
        return
    mapping = {
        "mappings":{
            "properties":
            {
                "id": {"type" : "integer"},
                "name": {"type": "text",
                         "fields":{
                             "keyword": {"type": "keyword"}
                         }
                         },
                "charge_rs": {"type": "float"},
                "city": {"type": "keyword"}
             
             }
        
        }
    }
    await es.indices.create(index=service, mappings=mapping["mappings"])
    print("Index successfully created")
    