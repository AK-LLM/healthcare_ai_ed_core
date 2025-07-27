FHIR_VERSION = '4.0.1'
def parse_fhir_resource(resource):
    return {'parsed': True, 'resourceType': resource.get('resourceType', 'Unknown')}
