import sys
import asyncio

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
import aiohttp
import json

async def main():
    url = "https://mst-mcp-xjb5.onrender.com/sse"
    headers = {"Authorization": "Bearer ANTIGRAVITY_IDE_BYPASS_TOKEN_123"}
    
    async with aiohttp.ClientSession() as session:
        # Connect to SSE
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(f"Failed to connect to SSE: {response.status}", file=sys.stderr)
                return
                
            post_url = None
            
            async def read_sse():
                nonlocal post_url
                async for line in response.content:
                    line = line.decode('utf-8').strip()
                    if not line:
                        continue
                    if line.startswith("event: endpoint"):
                        pass
                    elif line.startswith("data: ") and post_url is None:
                        endpoint = line[6:]
                        post_url = "https://mst-mcp-xjb5.onrender.com" + endpoint
                    elif line.startswith("data: "):
                        # Forward JSONRPC messages to stdout
                        sys.stdout.write(line[6:] + "\n")
                        sys.stdout.flush()

            async def read_stdin():
                loop = asyncio.get_running_loop()
                while True:
                    line = await loop.run_in_executor(None, sys.stdin.readline)
                    if not line:
                        break
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Wait until we have the POST URL
                    while post_url is None:
                        await asyncio.sleep(0.1)
                        
                    # Forward to server
                    try:
                        async with session.post(post_url, data=line, headers={
                            "Authorization": "Bearer ANTIGRAVITY_IDE_BYPASS_TOKEN_123",
                            "Content-Type": "application/json"
                        }) as post_res:
                            pass
                    except Exception as e:
                        print(f"Error posting to server: {e}", file=sys.stderr)

            await asyncio.gather(read_sse(), read_stdin())

if __name__ == "__main__":
    asyncio.run(main())
