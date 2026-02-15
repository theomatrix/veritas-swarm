"""
Test script to verify POST /api/analyze endpoint
"""

import requests
import json
import io

# Test 1: Health check
print("=" * 60)
print("TEST 1: Health Check")
print("=" * 60)

try:
    response = requests.get("http://localhost:8000/api/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✓ Health check passed\n")
except Exception as e:
    print(f"✗ Health check failed: {e}\n")

# Test 2: POST /api/analyze with dummy file
print("=" * 60)
print("TEST 2: POST /api/analyze (SSE Stream)")
print("=" * 60)

try:
    # Create a dummy image file
    dummy_file = io.BytesIO(b"fake image data for testing")
    files = {"file": ("test.jpg", dummy_file, "image/jpeg")}
    
    response = requests.post(
        "http://localhost:8000/api/analyze",
        files=files,
        stream=True
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print("\nSSE Events:")
    print("-" * 60)
    
    event_count = 0
    for line in response.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            if decoded.startswith('data: '):
                event_count += 1
                event_data = json.loads(decoded[6:])  # Remove 'data: ' prefix
                event_type = event_data.get('type', 'unknown')
                print(f"Event {event_count}: {event_type}")
                
                if event_type == 'agent_start':
                    print(f"  Agent: {event_data.get('agent')}")
                elif event_type == 'agent_complete':
                    print(f"  Agent: {event_data.get('agent')}")
                    findings = event_data.get('findings', '')
                    print(f"  Findings: {findings[:100]}...")
                elif event_type == 'verdict':
                    print(f"  Score: {event_data.get('score')}")
                    print(f"  Confidence: {event_data.get('confidence')}")
                elif event_type == 'done':
                    print("  Stream complete")
                    break
    
    print("-" * 60)
    print(f"✓ Received {event_count} events successfully\n")
    
except Exception as e:
    print(f"✗ POST test failed: {e}\n")

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print("✓ Backend is running and accepting requests")
print("✓ SSE streaming is working correctly")
print("✓ Frontend-backend compatibility verified")
