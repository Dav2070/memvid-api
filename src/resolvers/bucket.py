import os
import uuid
from ariadne import MutationType
from memvid import MemvidEncoder
from ..services.file_service import list_folders, list_files, get_file_content, create_folder, upload_file

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

@mutation.field("generateMemory")
def generate_memory(_, info, name):
	"""
	Generate a memory for the specified bucket.
	"""
	folders = list_folders(info.context['s3'])

	if name not in folders:
		raise Exception(f"Bucket with name '{name}' does not exist.")

	# Retrieve all files in the bucket
	files = list_files(info.context['s3'], name)
	chunks = []
	uploaded_memory_file_name = "memory.mp4"
	uploaded_index_file_name = "index.json"

	for file in files:
		if file == uploaded_memory_file_name or file == uploaded_index_file_name:
			continue

		content = get_file_content(info.context['s3'], f"{name}/{file}")

		if content:
			chunks.append(content.decode('utf-8'))

	encoder = MemvidEncoder()
	encoder.add_chunks(chunks)

	memory_file_name = f"{name}_memory.mp4"
	index_file_name = f"{name}_index.json"
	index_faiss_file_name = f"{name}_index.faiss"

	encoder.build_video(memory_file_name, index_file_name)

	# Upload the generated memory video and index to the bucket
	upload_file(info.context['s3'], f"{name}/{uploaded_memory_file_name}", open(memory_file_name, "rb"))
	upload_file(info.context['s3'], f"{name}/{uploaded_index_file_name}", open(index_file_name, "rb"))

	# Delete the local files after upload
	os.remove(memory_file_name)
	os.remove(index_file_name)
	os.remove(index_faiss_file_name)
	
	return { "name": name }
