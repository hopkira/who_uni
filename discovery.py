import json
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(args):
    query = args.get("query","K9")
    count = args.get("count",3)
    authenticator = IAMAuthenticator('xxxx')
    discovery = DiscoveryV1(
        version='2018-08-01',
        authenticator=authenticator)
    discovery.set_service_url('xxxx')
    query_results = discovery.query(
        environment_id='xxxx',
        collection_id='xxxx',
        query = query,
        passages= True,
        passages_count= 100).get_result()
    result = {"entities": [],"passages": []}
    try:
        id = query_results['results'][0]['id']
        passage_list = query_results['passages']
        entities = query_results['results'][0]['enriched_text']['entities']
        for entity in entities:
            if entity['count'] > count:
                result["entities"].append(entity)
        for passage in passage_list:
            if passage['document_id']==id:
                result["passages"].append(passage)
                result["body"] = passage['passage_text']
                break
    except IndexError:
        return result
    return result