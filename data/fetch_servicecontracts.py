import requests
import json

def fetch_servicecontracts():
    url = "https://fsmapi.s4servicesync.com/api/servicecontracts"
    
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://fsm.s4servicesync.com",
        "Referer": "https://fsm.s4servicesync.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "x-tenant": "Charlotte"
    }
    
    cookies = {
        "AUTH-TOKEN": "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJzZXJ2aWNlc3luYyIsInN1YiI6ImZvcnVzZTE5ODFAZ21haWwuY29tIiwiaWF0IjoxNzY5NTM5NjI5LCJleHAiOjE3Njk1NDMyMjl9.oghC3Y0sYt-znNlxl_p3Sm5CHvsAoCKR0Gqjvh79oXh0hRCEV_Vkdi_RXLGEqpFQWJwU0QjzGfA6s87Z6xVO0Q"
    }
    
    try:
        response = requests.get(
            url,
            headers=headers,
            cookies=cookies
        )
        
        response.raise_for_status()
        
        # Parse response as JSON
        data = response.json()
        
        # Save to JSON file
        with open("servicecontracts_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response saved to servicecontracts_response.json")
        
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
    fetch_servicecontracts()

