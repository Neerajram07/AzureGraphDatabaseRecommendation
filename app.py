from flask import Flask, jsonify
from gremlin_python.driver import client, serializer
import sys
import asyncio

app = Flask(__name__)

# Adjust the event loop policy for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Set up the Gremlin client
ACCOUNT_NAME = "graphdbpdpoc"
ACCOUNT_KEY = "ZitvYbeP0MMVlUpZghI5N3HIftH8ssyYVQWrFLnAhd2fH3w9VYzSeu9cotMWjC6wVrvkpaK3iLnCACDbb2zwJw=="
 
gremlin_client = client.Client(
    url=f"wss://{ACCOUNT_NAME}.gremlin.cosmos.azure.com:443/",
    traversal_source="g",
    username="/dbs/TieOppDB/colls/TieOpp",
    password=f"{ACCOUNT_KEY}",
    message_serializer=serializer.GraphSONSerializersV2d0(),
)

# Synchronous Gremlin query function
def run_gremlin_query():
    query = """
    g.V().has('user', 'UserId', '12345').out('is_student').out('hasSkill').out('allSkill').in('allSkills').in('has').dedup().valueMap(true)
    """
    # Execute the query synchronously
    result_set = gremlin_client.submit(query)
    result = result_set.all().result()  # Fetch the result synchronously
    return result

@app.route('/get-internships', methods=['GET'])
def get_internships():
    # Call the Gremlin query function synchronously
    gremlin_result = run_gremlin_query()
    
    # Return the result as a JSON response
    return jsonify(gremlin_result)

if __name__ == '__main__':
    app.run(debug=True)
