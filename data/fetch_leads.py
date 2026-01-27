import requests
import json

def fetch_leads():
    url = "https://fsmapi.s4servicesync.com/api/grid-data/leads"
    
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
        "x-tenant": "Charlotte"
    }
    
    cookies = {
        "AUTH-TOKEN": "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJzZXJ2aWNlc3luYyIsInN1YiI6ImZvcnVzZTE5ODFAZ21haWwuY29tIiwiaWF0IjoxNzY5NTM4NDg3LCJleHAiOjE3Njk1NDIwODd9.axO9hrItAcZ155Mpbs8-5ERTPT8LxG9EIjLJrAy1HJBvLDkAnVFKz4wcSfD8GStFnIJSkhGqbvH_gmYXuAHL3Q"
    }
    
    payload = {
        "skip": 0,
        "take": 2000
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
        with open("leads_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response saved to leads_response.json")
        
        # Display count information
        if isinstance(data, dict):
            if "data" in data:
                print(f"Total records received: {len(data['data'])}")
            if "total" in data:
                print(f"Total available records: {data['total']}")
        elif isinstance(data, list):
            print(f"Total records received: {len(data)}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        print(f"Raw response: {response.text}")
        return None

if __name__ == "__main__":
    fetch_leads()

