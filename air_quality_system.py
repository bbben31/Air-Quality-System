import random
import time
import datetime

# Driver code
from db_utils import create_server_connection, create_air_quality_database, create_db_connection, create_insert_query, \
    select_query, insert_many_data, create_air_quality_database_2

from air_quality_db_utils import create_area_table, create_devices_table, create_rep_location, create_user_table, \
    create_aq_data_table, create_aq_data_flex, create_area_location_table, create_installation_table, \
    create_user_access_control_table, create_user_location_access


def create_air_quality_tables(connection):
    print("Creating Area Table")
    create_insert_query(connection, create_area_table())  # Execute our defined query
    print("Done")
    print("Creating Devices Table")
    create_insert_query(connection, create_devices_table())  # Execute our defined query
    print("Done")
    print("Creating replocation Table")
    create_insert_query(connection, create_rep_location())  # Execute our defined query
    print("Done")
    print("Creating users Table")
    create_insert_query(connection, create_user_table())  # Execute our defined query
    print("Done")
    print("Creating aq_data Table")
    create_insert_query(connection, create_aq_data_table())  # Execute our defined query
    print("Done")
    print("Creating area location Table")
    create_insert_query(connection, create_area_location_table())  # Execute our defined query
    print("Done")
    print("Creating installation Table")
    create_insert_query(connection, create_installation_table())  # Execute our defined query
    print("Done")
    print("Creating user access control Table")
    create_insert_query(connection, create_user_access_control_table())  # Execute our defined query
    print("Done")
    print("Creating user location access table")
    create_insert_query(connection, create_user_location_access())  # Execute our defined query
    print("Done")


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


def collect_air_quality_data(connection, device_config, location_config):
    print("Data creation is in progress: ")
    print("Type Ctrl + C to exit data creation.")
    sql = '''
    INSERT INTO aq_data (aqdata_id, fk_device_id, fk_location_id, pm25, pm10, co, so2, o3, collection_time) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    val = []
    clock = 0
    while True:
        try:
            time.sleep(1)
            for i in range(len(device_config)):
                clock = clock + 1
                data = [clock, device_config[i], location_config[i], random.uniform(95.5, 105.5),
                        random.uniform(190, 210), random.uniform(70.5, 85.5), random.uniform(60, 90),
                        random.uniform(0.5, 3.5), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                val.append(tuple(data))

        except KeyboardInterrupt:
            break

    print("Data Ingestion is in progress: ")
    insert_many_data(connection, sql, val)
    print("Data is inserted in the aq_data table")


if __name__ == "__main__":
    """
    Please enter the necessary information related to the DB at this place. 
    Please change PW and ROOT based on the configuration of your own system. 
    """
    PW = "root"  # IMPORTANT! Put your MySQL Terminal password here.
    ROOT = "root"
    DB = "Air_Quality_Database"  # This is the name of the database we will create in the next step - call it whatever you like.
    LOCALHOST = "localhost"
    connection = create_server_connection(LOCALHOST, ROOT, PW)

    # creating the schema in the DB
    create_air_quality_database(connection, DB, DB)

    #create_air_quality_database_2(connection, DB)

    connection = create_db_connection(LOCALHOST, ROOT, PW, DB)  # Connect to the Database

    create_air_quality_tables(connection)

    insert_area = """
	INSERT INTO area VALUES
	('area101',  'Gotham')
	"""

    create_insert_query(connection, insert_area)

    insert_device = """
	INSERT INTO devices VALUES
	('device101',  'PLC Group', 'PM Sensor', '1234876', '23-06-2018'),
	('device102',  'Innovative Solutions', 'Green House Gas', '4287667', '22-09-2018'),
	('device103',  'AirThings', 'PM Sensor, Green House Gas', '3452891', '24-12-2018')
	"""

    create_insert_query(connection, insert_device)

    insert_location = """
	INSERT INTO replocation VALUES
	('PSBG101',  '75.93', '134.84', 'Primary School Backyard Gotham', 'District Primary School', 'School'),
	('CIHG101',  '81.67', '154.17', 'City Hospital Gotham', 'District Hospital', 'Hospital'),
	('PSFG102',  '79.67', '140.39', 'Primary School Frontgate Gotham', 'District Primary School', 'School')
	"""
    create_insert_query(connection, insert_location)

    insert_user = """
	INSERT INTO users VALUES
	('user101',  'John Doe', 'john@example.com', '665-877-8852', '790 Kozey Meadow Apt. 175 Kozeyside, WA 99871-1865'),
	('user102',  'Alice cooper', 'alice@example.com', '134-345-5430', '8589 Miller Centers Leannonmouth, OR 18781-6843'),
	('user103',  'Bob Willis', 'bob@example.com', '300-052-5450', '958 Gerry Estate New Eudora, MT 89349-0462')
	"""
    create_insert_query(connection, insert_user)

    # Rationale for this schema:
    # Allow for companies to restrict air quality usage for monetization based on location.
    insert_users_location_access = """
	INSERT INTO users_location_access VALUES
	('user101',  'PSBG101', 'Normal'),
	('user101',  'PSFG102', 'Admin'),
	('user102',  'CIHG101', 'Admin')
	"""
    create_insert_query(connection, insert_users_location_access)

    user_access_control_table = """
	INSERT INTO user_access_control VALUES
	(1, 'user101', 'location', 'PSBG101', 'Normal'),
	(2, 'user101', 'location', 'PSFG102', 'Admin'),
	(3, 'user102', 'location', 'CIHG101', 'Admin'),
	(4, 'user101', 'device', 'device101', 'Normal'),
	(5, 'user101', 'device', 'device102', 'Admin'),
	(6, 'user102', 'area', 'area101', 'Admin')

	"""
    create_insert_query(connection, user_access_control_table)

    device_config = get_all_devices(connection)

    location_config = get_all_locations(connection)

    admin_users = get_all_administrators(connection)
    # Demo the get all normal users ( if required )...

    collect_air_quality_data(connection, device_config, location_config)
