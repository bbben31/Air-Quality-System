import random
import time
import datetime

# Driver code
from db_utils import create_server_connection, create_air_quality_database, create_db_connection, create_insert_query, \
    select_query, insert_many_data


def get_all_devices(connection):
    print("Printing devices data from the devices table: ")
    q1 = """
    	SELECT *
    	FROM devices;
    	"""

    result_devices = select_query(connection, q1)
    device_config = []
    for result in result_devices:
        print(result)
        device_config.append(result[0])
    return device_config


def get_all_locations(connection):
    print("Location related data in the replocation table: ")
    q2 = """
    	SELECT *
    	FROM replocation;
    	"""
    location_config = []
    result_location = select_query(connection, q2)

    for result in result_location:
        print(result)
        location_config.append(result[0])
    return location_config


def get_all_administrators(connection):
    print("Join Operation: This will show the user table data along with the permission it has for different entities.")

    q5 = """
    	SELECT users.user_id, users.user_name, users.phone_no, user_access_control.access_type, user_access_control.access_entity_type, user_access_control.entity_id
    	FROM users
    	JOIN user_access_control
    	ON users.user_id = user_access_control.user_id
    	WHERE user_access_control.access_type = 'Admin';
    	"""
    admin_users = []
    results = select_query(connection, q5)

    for result in results:
        print(result)
        admin_users.append(result)
    return admin_users


def get_aq_data_by_locationId(connection, locationId):
    print("Join Operation: This will show the user table data along with the permission it has for different entities.")

    q5 = """
    	SELECT *
    	FROM aq_data
    	JOIN replocation
    	ON replocation.location_id = """ + f'"{locationId}"' + """
    	WHERE aq_data.fk_location_id = replocation.location_id
    	"""
    aq_data_by_locations = []
    results = select_query(connection, q5)

    for result in results:
        print(result)
        aq_data_by_locations.append(result)
    return aq_data_by_locations


def get_aq_data_by_users(connection, userId):
    print("Join Operation: This will show the user table data along with the permission it has for different entities.")

    q5 = """
    	SELECT *
    	FROM aq_data
    	JOIN users_location_access
    	JOIN users
    	ON users.user_id = """ + f'"{userId}"' + """
    	JOIN replocation
    	ON users_location_access.location_id = replocation.location_id
    	"""
    aq_data_by_users = []
    results = select_query(connection, q5)

    for result in results:
        print(result)
        aq_data_by_users.append(result)
    return aq_data_by_users


def get_users_by_location(connection, locationId):
    q5 = """
        	SELECT *
        	FROM users
        	JOIN users_location_access
        	JOIN replocation
        	ON users_location_access.location_id = replocation.location_id
        	WHERE users_location_access.location_id = """ + f'"{locationId}"' + """
        	"""
    users = []
    results = select_query(connection, q5)

    for result in results:
        print(result)
        users.append(result)
    return users

if __name__ == "__main__":
    """
    Please enter the necessary information related to the DB at this place. 
    Please change PW and ROOT based on the configuration of your own system. 
    """
    PW = "root"  # IMPORTANT! Put your MySQL Terminal password here.
    ROOT = "root"
    DB = "Air_Quality_Database"  # This is the name of the database we will create in the next step - call it whatever you like.
    LOCALHOST = "localhost"

    connection = create_db_connection(LOCALHOST, ROOT, PW, DB)  # Connect to the Database

    device_config = get_all_devices(connection)

    location_config = get_all_locations(connection)

    #admin_users = get_all_administrators(connection)
    # Demo the get all normal users ( if required )...

    #aq_data_by_locations_1 = get_aq_data_by_locationId(connection, location_config[0])
    #aq_data_by_locations_2 = get_aq_data_by_locationId(connection, location_config[1])
    #aq_data_by_locations_3 = get_aq_data_by_locationId(connection, location_config[2])

    #users_by_location_1 = get_users_by_location(connection, location_config[0])
    #users_by_location_2 = get_users_by_location(connection, location_config[1])
