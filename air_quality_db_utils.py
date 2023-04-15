def create_area_table():
    # Configuring the tables that will hold the data
    # here we are creating the table named as area
    return """
    	CREATE TABLE area (
      		area_id varchar(45) PRIMARY KEY,
      		area_description varchar(45) NOT NULL
      	)
    	"""

def create_devices_table():
    # creating the devices table
    return """
    	CREATE TABLE devices (
       		device_id varchar(45) PRIMARY KEY,
      		mfr varchar(160) NOT NULL,
      		type varchar(45) NOT NULL,
      		serial_no varchar(45) NOT NULL,
      		yom varchar(45) NOT NULL
    	)
    	"""


def create_rep_location():
    # creating the location table
    return """
    		CREATE TABLE replocation (
      		location_id varchar(45) PRIMARY KEY,
      		lattiude varchar(25) NOT NULL,
      		longitude varchar(250) NOT NULL,
      		location_name varchar(120) NOT NULL,
      		description varchar(240) NOT NULL,
      		location_type varchar(100)
    	)
    	"""


def create_user_table():
    # creating the users table to hold the user basic information
    return """
    	CREATE TABLE users (
    	  user_id varchar(20) PRIMARY KEY,
    	  user_name varchar(45) NOT NULL,
    	  email varchar(45) NOT NULL,
    	  phone_no varchar(45) NOT NULL,
    	  address varchar(160) NOT NULL
    	)
    	"""


def create_user_access_control_table():
    # creating a table to map the access control of each type od entity
    # location, device, area in a single table
    # this reduces the need to introdice foreign key concept in this table
    return """
    	CREATE TABLE user_access_control (
    	  id int NOT NULL PRIMARY KEY,
    	  user_id varchar(45) NOT NULL,
    	  access_entity_type varchar(45) NOT NULL,
    	  entity_id varchar(45) NOT NULL,
    	  access_type varchar(20) NOT NULL,
    	  CONSTRAINT `fk_user_id_access` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
    	)
    	"""


def create_aq_data_table():
    # creating the raw data table that will hold the necessary information related to the table
    return """
    	CREATE TABLE aq_data (
    	  aqdata_id  INT PRIMARY KEY,
    	  fk_device_id varchar(45) ,
    	  fk_location_id varchar(45) ,
    	  pm25 FLOAT DEFAULT NULL,
    	  pm10 FLOAT DEFAULT NULL,
    	  co FLOAT DEFAULT NULL,
    	  so2 FLOAT DEFAULT NULL,
    	  o3 FLOAT DEFAULT NULL,
    	  collection_time varchar(40) NOT NULL,
    	  CONSTRAINT fk_deviceid FOREIGN KEY (`fk_device_id`) REFERENCES `devices` (`device_id`),
    	  CONSTRAINT fk_locationid FOREIGN KEY (`fk_location_id`) REFERENCES `replocation` (`location_id`)
    	)
    	"""


def create_aq_data_flex():
    # creating another raw data table that can mimic in key:value format
    return """
    	CREATE TABLE aq_data_flex (
    	  aqdata_id INT PRIMARY KEY NOT NULL,
    	  fk_device_id_flex varchar(45),
    	  fk_location_id_flex varchar(45),
    	  aq_data_type varchar(45) NOT NULL,
    	  aq_data_value double NOT NULL,
    	  collection_time varchar(40) NOT NULL,
    	  CONSTRAINT fk_deviceid_flex FOREIGN KEY (`fk_device_id_flex`) REFERENCES `devices` (`device_id`),
    	  CONSTRAINT fk_locationid_flex FOREIGN KEY (`fk_location_id_flex`) REFERENCES `replocation` (`location_id`)
    	)
    	"""


def create_area_location_table():
    # table to map the location of each area with the map
    return """
    	CREATE TABLE area_location (
    	  id INT NOT NULL PRIMARY KEY,
    	  fk_areaid varchar(45) NOT NULL,
    	  fk_locationid_area varchar(45) NOT NULL,
    	  CONSTRAINT `fk_areaid` FOREIGN KEY (`fk_areaid`) REFERENCES `area` (`area_id`),
    	  CONSTRAINT `fk_locationid_area_location` FOREIGN KEY (`fk_locationid_area`) REFERENCES `replocation` (`location_id`) ON DELETE CASCADE ON UPDATE CASCADE
    	)
    	"""


def create_installation_table():
    # table to map the devices and locations asscoitaed with that device
    return """
    	CREATE TABLE installation (
    	  installation_id int NOT NULL PRIMARY KEY,
    	  fk_locationid_installation varchar(45) NOT NULL,
    	  fk_deviceid_installation varchar(45) NOT NULL,
    	  installation_timestamp timestamp(2) NOT NULL,
    	  is_active varchar(10) NOT NULL,
    	  CONSTRAINT `fk_deviceid_installation` FOREIGN KEY (`fk_deviceid_installation`) REFERENCES `devices` (`device_id`),
    	  CONSTRAINT `fk_locationid_installation` FOREIGN KEY (`fk_locationid_installation`) REFERENCES `replocation` (`location_id`)
    	)
    	"""


def create_user_location_access():
    # creating individual table to map the access control for user for each of the location
    # drawback is that we
    return """
    	CREATE TABLE users_location_access (
    	  user_id varchar(45) NOT NULL,
    	  location_id varchar(45) NOT NULL,
    	  access_type varchar(45) NOT NULL,
    	  PRIMARY KEY (user_id, location_id),
    	  CONSTRAINT `fk_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
    	  CONSTRAINT `fk_location_id` FOREIGN KEY (`location_id`) REFERENCES `replocation` (`location_id`) ON DELETE CASCADE ON UPDATE CASCADE
    	)
    	"""
