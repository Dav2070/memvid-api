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

def list_files(s3, folder_name):
	"""
	List all files in the specified folder of the S3 bucket.
	"""
	if not folder_name.endswith('/'):
		folder_name += '/'

	response = s3.list_objects_v2(
		Bucket="document-ai-dav",
		Prefix=folder_name
	)

	files = []

	if 'Contents' in response:
		for obj in response['Contents']:
			if obj['Key'] != folder_name:  # Exclude the folder itself
				files.append(obj['Key'].replace(folder_name, ''))

	return files

def get_file_content(s3, file_name):
	"""
	Get the content of a file from the specified folder in the S3 bucket.
	"""
	response = s3.get_object(
		Bucket="document-ai-dav",
		Key=file_name
	)

	return response['Body'].read()

def download_file(s3, file_name, file_path):
	"""
	Download a file from the specified folder in the S3 bucket to a local path.
	"""
	s3.download_file(
		Bucket="document-ai-dav",
		Key=file_name,
		Filename=file_path
	)

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
