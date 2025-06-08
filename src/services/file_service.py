def list_folders(s3):
	"""
	List all folders in the S3 bucket.
	"""
	response = s3.list_objects_v2(
		Bucket="document-ai-dav",
		Delimiter='/'
	)

	folders = []

	if 'CommonPrefixes' in response:
		for prefix in response['CommonPrefixes']:
			folders.append(prefix['Prefix'].replace('/', ''))

	return folders

def create_folder(s3, folder_name):
	"""
	Create a folder in the S3 bucket.
	"""
	if not folder_name.endswith('/'):
		folder_name += '/'

	s3.put_object(
		Bucket="document-ai-dav",
		Key=folder_name
	)

	return folder_name

def upload_file(s3, file_name, data):
	"""
	Upload a file to the specified folder in the S3 bucket.
	"""
	s3.put_object(
		Bucket="document-ai-dav",
		Key=file_name,
		Body=data
	)
