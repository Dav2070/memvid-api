from ariadne import QueryType
from memvid import chat_with_memory, MemvidChat
from ..services.file_service import download_file

query = QueryType()

@query.field("chatWithMemory")
def chat(_, info, bucketName, message):
	memory_file_name = f"{bucketName}_memory.mp4"
	index_file_name = f"{bucketName}_index.json"
	index_faiss_file_name = f"{bucketName}_index.faiss"

	download_file(
		info.context["s3"],
		f"{bucketName}/memory.mp4",
		memory_file_name
	)

	download_file(
		info.context["s3"],
		f"{bucketName}/index.json",
		index_file_name
	)

	download_file(
		info.context["s3"],
		f"{bucketName}/index.faiss",
		index_faiss_file_name
	)

	chat = MemvidChat(
		video_file=memory_file_name,
		index_file=index_file_name,
		llm_provider="openai"
	)

	return chat.chat(message)
