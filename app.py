import os
import boto3
from ariadne import graphql_sync, make_executable_schema
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from src.type_defs import type_defs
from src.resolvers.bla import query
from src.resolvers.bucket import mutation

load_dotenv()
schema = make_executable_schema(type_defs, [query, mutation])

app = Flask(__name__)

s3 = boto3.client(
	"s3",
	region_name="fra1",
	endpoint_url="https://fra1.digitaloceanspaces.com",
	aws_access_key_id=os.getenv("SPACES_ACCESS_KEY"),
	aws_secret_access_key=os.getenv("SPACES_SECRET_KEY")
)

# Retrieve HTML for the GraphiQL.
# If explorer implements logic dependant on current request,
# change the html(None) call to the html(request)
# and move this line to the graphql_explorer function.
explorer_html = ExplorerGraphiQL().html(None)

@app.route("/", methods=["GET"])
def graphql_explorer():
	# On GET request serve the GraphQL explorer.
	# You don't have to provide the explorer if you don't want to
	# but keep on mind this will not prohibit clients from
	# exploring your API using desktop GraphQL explorer app.
	return explorer_html, 200

@app.route("/", methods=["POST"])
def graphql_server():
	# GraphQL queries are always sent as POST
	data = request.get_json()

	# Note: Passing the request to the context is optional.
	# In Flask, the current request is always accessible as flask.request
	success, result = graphql_sync(
		schema,
		data,
		context_value={
			"request": request,
			"s3": s3
		},
		debug=app.debug
	)

	status_code = 200 if success else 400
	return jsonify(result), status_code

if __name__ == "__main__":
   app.run(debug=True)
