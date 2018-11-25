import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import cfg


HOST = cfg.settings['host']
MASTER_KEY = cfg.settings['master_key']
DATABASE_ID = cfg.settings['database_id']
COLLECTION_ID = cfg.settings['collection_id']

database_link = 'dbs/' + DATABASE_ID
collection_link = database_link + '/colls/' + COLLECTION_ID


class IDisposable(cosmos_client.CosmosClient):
    """ A context manager to automatically close an object with a close method
    in a with statement. """

    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        return self.obj  # bound to target

    def __exit__(self, exception_type, exception_val, trace):
        # extra cleanup in here
        self = None


def save_record(document):
    with IDisposable(cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY})) as client:
        try:
            client.CreateItem(collection_link, document)
        except errors.HTTPFailure as e:
            print('\nrun_sample has caught an error. {0}'.format(e.message))
        finally:
            print("\nrun_sample done")


def get_all_record():
    with IDisposable(cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY})) as client:
        documentlist = list(client.ReadItems(collection_link, {'maxItemCount': 10}))
        return {"records": documentlist}
