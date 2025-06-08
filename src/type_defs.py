type_defs = """
	type Query {
		chatWithMemory(bucketName: String!, message: String!): String!
	}

	type Mutation {
		createBucket(name: String!): Bucket!
		addFileToBucket(name: String!, content: String!): Bucket!
		generateMemory(name: String!): Bucket!
	}

	type Bucket {
		name: String!
	}
"""
