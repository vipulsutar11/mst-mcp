import urllib.request
import json

# First, GET the SSE endpoint to get the messages URL
req = urllib.request.Request("https://mst-mcp-xjb5.onrender.com/sse", method="GET", headers={"Authorization": "Bearer ANTIGRAVITY_IDE_BYPASS_TOKEN_123"})
try:
    with urllib.request.urlopen(req) as response:
        # Read the first event
        line = response.readline().decode('utf-8')
        while line and not line.startswith("event: endpoint"):
            line = response.readline().decode('utf-8')
        
        # Read the data line for the endpoint event
        data_line = response.readline().decode('utf-8')
        print("Endpoint event:", line.strip())
        print("Endpoint data:", data_line.strip())
        
        endpoint_url = data_line.replace("data: ", "").strip()
        print("Extracted endpoint:", endpoint_url)
        
        # Now try to POST a dummy initialize message to it
        if endpoint_url.startswith("/"):
            endpoint_url = "https://mst-mcp-xjb5.onrender.com" + endpoint_url
            
        print("Full POST url:", endpoint_url)
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0"}
            }
        }
        
        post_req = urllib.request.Request(endpoint_url, data=json.dumps(payload).encode('utf-8'), method="POST", headers={"Content-Type": "application/json", "Authorization": "Bearer ANTIGRAVITY_IDE_BYPASS_TOKEN_123"})
        try:
            with urllib.request.urlopen(post_req) as post_response:
                print("POST response:", post_response.status)
                print(post_response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print("POST HTTP Error:", e.code)
            print("Response body:", e.read().decode('utf-8'))

except Exception as e:
    print("Error:", e)
