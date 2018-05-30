from background_task import background

# generic imports 
import time

# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)

from core import models as models

'''
This file provides background tasks that are performed with Django-Background-Tasks
'''

@background(schedule=1)
def delete_model_instance(instance_model, instance_id):

	'''
	Background task to delete generic DB model instance
	'''
	
	# try:

	# get model		
	m = getattr(models, instance_model, None)

	if m:

		# get model instance
		i = m.objects.get(pk=int(instance_id))
		logger.debug('retrieved %s model, instance ID %s, deleting' % (m.__name__, instance_id))
	
		# delete		
		return i.delete()

	else:
		logger.debug('Combine model %s not found, aborting' % (instance_model))	

	# except:
	# 	logger.debug('could not retrieve %s model, instance ID %s, aborting' % (instance_model, instance_id))
	# 	return False


@background(schedule=1)
def download_and_index_bulk_data(dbdd_id):

	'''
	Background task driver to manage downloading and indexing of bulk data

	Args:
		dbdd_id (int): ID of DPLABulkDataDownload (dbdd) instance
	'''

	# init bulk download instance
	dbdd = models.DPLABulkDataDownload.objects.get(pk=dbdd_id)

	# init data client with filepath
	dbdc = models.DPLABulkDataClient()

	# download data
	logger.debug('downloading %s' % dbdd.s3_key)
	dbdd.status = 'downloading'
	dbdd.save()
	download_results = dbdc.download_bulk_data(dbdd.s3_key, dbdd.filepath)	

	# index data
	logger.debug('indexing %s' % dbdd.filepath)
	dbdd.status = 'indexing'
	dbdd.save()
	es_index = dbdc.index_to_es(dbdd.s3_key, dbdd.filepath)	

	# update and return
	dbdd.es_index = es_index
	dbdd.status = 'finished'
	dbdd.save()

