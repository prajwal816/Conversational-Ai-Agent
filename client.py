import asyncio
import websockets
import time

async def simulate_conversation():
    uri = "ws://localhost:8000/ws"
    
    queries = [
        "Hello, can you help me reset my password?",
        "What is the return policy?",
        "How fast are your response latencies?",
        "Thank you, that is all."
    ]
    
    try:
        async with websockets.connect(uri) as websocket:
            print("[Client] Connected to server\\n")
            
            for query in queries:
                print(f"[Client] Sending: '{query}'")
                
                start_time = time.time()
                
                # Send text simulated as bytes
                await websocket.send(query.encode('utf-8'))
                
                # Wait for TTFT (Time To First Token)
                first_token_time = None
                
                full_response = ""
                
                while True:
                    response = await websocket.recv()
                    
                    if first_token_time is None:
                        first_token_time = time.time()
                        ttft = (first_token_time - start_time) * 1000
                        print(f"\\n   [Metrics] -> Latency (TTFT): {ttft:.2f}ms")
                        
                    if response == "[EOT]":
                        break
                        
                    full_response += response
                    # Print streamed tokens in real-time
                    print(response, end="", flush=True)
                
                total_time = (time.time() - start_time) * 1000
                print(f"\\n   [Metrics] -> Turn-taking complete: {total_time:.2f}ms\\n")
                
                await asyncio.sleep(1) # wait between turns

    except ConnectionRefusedError:
        print("[Error] Could not connect to the server. Is it running?")

if __name__ == "__main__":
    asyncio.run(simulate_conversation())
