import requests
import json

def fetch_proposals():
    url = "https://fsmapi.s4servicesync.com/api/proposals"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://fsm.s4servicesync.com",
        "Referer": "https://fsm.s4servicesync.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "x-tenant": "Boston Train-TAX"
    }
    
    cookies = {
        "AUTH-TOKEN": "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJzZXJ2aWNlc3luYyIsInN1YiI6ImZvcnVzZTE5ODFAZ21haWwuY29tIiwiaWF0IjoxNzY5NTQ1NTgwLCJleHAiOjE3Njk1NDkxODB9.v0aRF750YP9Z2zTM6PXqMC8Z9qyu01kLgy3Vzxn_uApbfaPFQ9Mhg8vcjwwdr6YvpIiQS0aw2TDyPZ5AD1rZEg"
    }
    
    payload = {
        "skip": 0,
        "take": 100,
        "sort": [{"field": "proposedDate", "dir": "desc"}],
        "filter": {"filters": [], "logic": "and"}
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            cookies=cookies,
            json=payload
        )
        
        response.raise_for_status()
        
        # Parse response as JSON
        data = response.json()
        
        # Save to JSON file
        with open("proposals_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response saved to proposals_response.json")
        
        # Display record count
        if isinstance(data, dict):
            if "content" in data:
                print(f"Total elements: {data.get('totalElements', 'N/A')}")
                print(f"Records received: {len(data['content'])}")
            elif "data" in data:
                print(f"Records received: {len(data['data'])}")
            else:
                print(f"Response keys: {list(data.keys())}")
        elif isinstance(data, list):
            print(f"Records received: {len(data)}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        print(f"Raw response: {response.text}")
        return None

if __name__ == "__main__":
    fetch_proposals()

