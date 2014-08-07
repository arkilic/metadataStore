__author__ = 'arkilic'
import datetime
import getpass

from metadataStore.dataapi.raw_commands import save_header, save_beamline_config, insert_event_descriptor, insert_event
from metadataStore.dataapi.raw_commands import find


def create(header=None, beamline_config=None, event_descriptor=None):
    """
    Create header, beamline_config, and event_descriptor

    :param header: Header attribute-value pairs
    :type header: dict
    :param beamline_config: BeamlineConfig attribute-value pairs
    :type beamline_config: dict
    :param event_descriptor: EventDescriptor attribute-value pairs
    :type event_descriptor: dict

    :Raises: TypeError, ValueError, ConnectionFailure, NotUniqueError

     :returns: None

    """
    if header is not None:
        if isinstance(header, dict):
            if 'scan_id' in header:
                if isinstance(header['scan_id'], int):
                    scan_id = header['scan_id']
                else:
                    raise TypeError('scan_id must be an integer')
            else:
                raise ValueError('scan_id is a required field')
            if 'start_time' in header:
                start_time = header['start_time']
            else:
                start_time = datetime.datetime.utcnow()
            if 'owner' in header:
                owner = header['owner']
            else:
                owner = getpass.getuser()
            if 'beamline_id' in header:
                beamline_id = header['beamline_id']
            else:
                beamline_id = None
            if 'custom' in header:
                custom = header['custom']
            else:
                custom = dict()
            if 'status' in header:
                status = header['status']
            else:
                status = 'In Progress'
            try:
                save_header(scan_id=scan_id, header_owner=owner, start_time=start_time, beamline_id=beamline_id,
                            status=status, custom=custom)
            except:
                raise
        else:
            raise TypeError('Header must be a Python dictionary ')

    if beamline_config is not None:
        if isinstance(beamline_config, dict):
            if 'scan_id' in beamline_config:
                scan_id = beamline_config['scan_id']
            else:
                raise ValueError('scan_id is a required field')
            if 'config_params' in beamline_config:
                config_params = beamline_config['config_params']
            else:
                config_params = dict()
            try:
                save_beamline_config(scan_id=scan_id, config_params=config_params)
            except:
                raise
        else:
            raise TypeError('BeamlineConfig must be a Python dictionary')

    if event_descriptor is not None:
        if isinstance(event_descriptor, dict):
            if 'scan_id' in event_descriptor:
                scan_id = event_descriptor['scan_id']
            else:
                raise ValueError('scan_id is required for EventDescriptor entries')
            if 'event_type_id' in event_descriptor:
                event_type_id = event_descriptor['event_type_id']
            else:
                event_type_id = None
            if 'descriptor_name' in event_descriptor:
                descriptor_name = event_descriptor['descriptor_name']
            else:
                raise ValueError('descriptor_name is required for EventDescriptor')
            if 'type_descriptor' in event_descriptor:
                type_descriptor = event_descriptor['type_descriptor']
            else:
                type_descriptor = dict()
            if 'tag' in event_descriptor:
                tag = event_descriptor['tag']
            else:
                tag = None
            try:
                insert_event_descriptor(scan_id=scan_id, event_type_id=event_type_id, descriptor_name=descriptor_name,
                                        type_descriptor=type_descriptor, tag=tag)
            except:
                raise
        else:
            raise TypeError('EventDescriptor must be a Python dictionary')


def record(event=dict()):
    """
    Events are saved given scan_id and descriptor name and additional optional parameters

    :param event: Dictionary used in order to save name-value pairs for Event entries
    :type event: dict

    :Raises: ConnectionFailure, NotUniqueError, ValueError

    Required fields: scan_id, descriptor_name
    Optional fields: owner, seq_no, data, description

    Usage:

    >>> record(event={'scan_id': 1344, 'descriptor_name': 'ascan'})

    >>> record(event={'scan_id': 1344, 'descriptor_name': 'ascan', 'owner': 'arkilic', 'seq_no': 0,
                  ... 'data':{'motor1': 13.4, 'image1': '/home/arkilic/sample.tiff'}})

    >>> record(event={'scan_id': 1344, 'descriptor_name': 'ascan', 'owner': 'arkilic', 'seq_no': 0,
                  ... 'data':{'motor1': 13.4, 'image1': '/home/arkilic/sample.tiff'}},'description': 'Linear scan')
    """
    if 'scan_id' in event:
        scan_id = event['scan_id']
    else:
        raise ValueError('scan_id is required in order to record an event')
    if 'descriptor_name' in event:
        descriptor_name = event['descriptor_name']
    else:
        raise ValueError('Descriptor is required in order to record an event')
    if 'description' in event:
        description = event['description']
    else:
        description = None
    if 'owner' in event:
        owner = event['owner']
    else:
        owner = getpass.getuser()
    if 'seq_no' in event:
        seq_no = event['seq_no']
    else:
        raise ValueError('seq_no is required field')
    if 'data' in event:
        data = event['data']
    else:
        data = dict()
    try:
        insert_event(scan_id=scan_id, descriptor_name=descriptor_name, owner=owner, seq_no=seq_no, data=data,
                     description=description)
    except:
        raise


def search(scan_id=None, owner=None, start_time=None, beamline_id=None, end_time=None, data=False):
    """
    Provides an easy way to search Header objects that are saved in metadataStore

    :param scan_id: Unique identifier for a given run
    :type scan_id: int
    :param owner: run header owner(unix user by default)
    :type owner: str
    :param start_time: Header creation time
    :type start_time: datetime.datetime object
    :param beamline_id: beamline descriptor
    :type beamline_id: str
    :param end_time: Header status time
    :type end_time: datetime.datetime object
    :param data: data field for collection routines to save experiemental progress
    :type data: dict

    Usage:

    >>> search(scan_id=s_id)
    >>> search(scan_id=s_id, owner='ark*')
    >>> search(scan_id=s_id, start_time=datetime.datetime(2014, 4, 5))
    >>> search(scan_id=s_id, start_time=datetime.datetime(2014, 4, 5), owner='arkilic')
    >>> search(scan_id=s_id, start_time=datetime.datetime(2014, 4, 5), owner='ark*')
    >>> search(scan_id=s_id, start_time=datetime.datetime(2014, 4, 5), owner='arkili.')

    """
    result = find(scan_id=scan_id, owner=owner, start_time=start_time, beamline_id=beamline_id, end_time=end_time,
                  data=data)
    return result


def end_collection():
    pass