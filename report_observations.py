from fhir.resources.observation import Observation
from fhir.resources.observation import ObservationComponent
from fhir.resources.device import Device
from fhir.resources.location import Location
from fhir.resources.patient import Patient
from postgis_connection import PostgisInterface
import argparse
from datetime import datetime, time

status = 'registered'
coding = {
    "coding": [{"system": "robot:tiago:111", "code": "hazard", "display": "hazard"}],
    "text": "Hazard detected in the house"
    }


def dummy_location():
    loc_data = {'status': 'active',
                'name': "Patient's Home",
                'description': "Patient's Home",
                'mode': 'kind',
                'type': [{'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/v3-RoleCode',
                                      'code': 'PTRES',
                                      'display': "Patient's Residence"}]}],
                'physicalType': {'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/location-physical-type',
                                             'code': 'ho',
                                             'display': 'House'}]},
                'managingOrganization': {'reference': 'Organization/f001'}}
    loc = Location(**loc_data)
    return loc


def dummy_device():
    dev_data = {'status': status, 'code': coding}
    dev = Device(**dev_data)


def dummy_patient():
    pat_data = {'identifier': [{'use': 'usual',
                                'type': {'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/v2-0203', 'code': 'MR'}]},
                                'system': 'urn:oid:1.2.36.146.595.217.0.1', 'value': '12345', 'period': {'start': '2001-05-06'},
                                'assigner': {'display': 'Acme Healthcare'}}],
                'active': True,
                'name': [{'use': 'official', 'family': 'Chalmers', 'given': ['Peter', 'James']},
                         {'use': 'usual', 'given': ['Jim']},
                         {'use': 'maiden', 'family': 'Windsor', 'given': ['Peter', 'James'], 'period': {'end': '2002'}}],
                'telecom': [{'use': 'home'},
                            {'system': 'phone', 'value': '(03) 5555 6473', 'use': 'work', 'rank': 1},
                            {'system': 'phone', 'value': '(03) 3410 5613', 'use': 'mobile', 'rank': 2}],
                'gender': 'male',
                'birthDate': '1974-12-25',
                'deceasedBoolean': False,
                'address': [{'use': 'home', 'type': 'both', 'text': '534 Erewhon St PeasantVille, Rainbow, Vic  3999',
                             'line': ['534 Erewhon St'], 'city': 'PleasantVille', 'district': 'Rainbow', 'state': 'Vic',
                             'postalCode': '3999', 'period': {'start': '1974-12-25'}}],
                'contact': [{'relationship': [{'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/v2-0131',
                                                           'code': 'N'}]}],
                             'name': {'family': 'du Marché',
                                      'given': ['Bénédicte']},
                             'telecom': [{'system': 'phone', 'value': '+33 (237) 998327'}],
                             'address': {'use': 'home', 'type': 'both', 'line': ['534 Erewhon St'],
                                         'city': 'PleasantVille', 'district': 'Rainbow', 'state': 'Vic',
                                         'postalCode': '3999', 'period': {'start': '1974-12-25'}},
                             'gender': 'female', 'period': {'start': '2012'}}],
                'managingOrganization': {'reference': 'Organization/1'}}
    pat = Patient(**pat_data)
    return pat


def find_hazards():
    query = 'SELECT location_3d, last_update, label FROM anchors WHERE hazard=true'
    return query


if __name__ == '__main__':
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-db", required=True, help="Database name")
    # args = vars(ap.parse_args())
    #
    # db_interface = PostgisInterface()
    # db_interface.connect_db('gianluca', args['db'])

    counter = 0

    # records = db_interface.query_db(find_hazards())

    # print(records)

    data = {'status': status, 'code': coding}
    obs = Observation(**data)
    location = dummy_location()
    print(location.json())
    patient = dummy_patient()
    print(patient.json())

    # fields marked as external must be retrieved from the remote FHIR server
    # identifier - some unique identifier -> this is a complex data structure
    # external.subject - Patient -> the user associated with the house
    # external.focus - Location -> a reference to the house or an area in the house
    # issued - Current timestamp
    # values are mutually exclusive, use components
    # valueString - 'x, y' in map coordinates -> to be replaced
    # valueDateTime - Last update of the anchor
    # external.device - Device -> the robot

    obs.issued = datetime.now()
    obs.valueString = '13.28, 4.36'
    subCoding = coding.copy()
    subCoding['coding'][0]['code'] = 'hazard.timestamp'
    subData = {'code': subCoding}
    obs.component = [ObservationComponent(**subData)]
    obs.component[0].valueDateTime = datetime.now()

    print(obs.json())
