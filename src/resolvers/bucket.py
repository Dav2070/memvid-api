import uuid
from ariadne import MutationType
from ..services.file_service import list_folders, create_folder, upload_file

mutation = MutationType()

@mutation.field("createBucket")
def create_bucket(_, info, name):
	folders = list_folders(info.context['s3'])

	if name in folders:
		raise Exception(f"Bucket with name '{name}' already exists.")

	# Validate the bucket name
	if not name.isalnum() or len(name) < 3 or len(name) > 20:
		raise Exception("Bucket name must be alphanumeric and between 3 and 20 characters long.")

	# Create the bucket (folder) in S3.
	create_folder(info.context['s3'], name)

	return { "name": name }

@mutation.field("addFileToBucket")
def add_file_to_bucket(_, info, name, content):
	"""
	Add a file to the specified bucket.
	"""
	folders = list_folders(info.context['s3'])

	if name not in folders:
		raise Exception(f"Bucket with name '{name}' does not exist.")

	# Validate the content
	if not content:
		raise Exception("File content cannot be empty.")

	# Upload the content as file to the specified bucket
	file_name = f"{name}/{str(uuid.uuid4())}"
	upload_file(info.context['s3'], file_name, content)

	return { "name": name }
