# gsc

UPDATE `properties_url` SET `c_status`='Indexed' WHERE `c_status`='Valid';
UPDATE `properties_url` SET `c_status`='Not indexed' WHERE `c_status`='Invalid';
UPDATE `properties_url` SET `mu_status`='Usable' WHERE `mu_status`='Valid';