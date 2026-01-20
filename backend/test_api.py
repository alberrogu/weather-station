from fastapi.testclient import TestClient
from backend.main import app
import os

# Create a temporary DB for testing or just use the local one (for simplicity here)
#Ideally we override get_db, but for a quick check, using the file is fine.

client = TestClient(app)

def test_upload_and_retrieve():
    print("Testing Data Upload...")
    upload_params = {
        "wsid": "TEST_STATION",
        "wspw": "123456",
        "datetime": "2025-01-20 12:00:00",
        "t1tem": "25.5",
        "t1hum": "60",
        "t1wdir": "180",
        "t1ws": "5.5",
        "t1raindy": "1.2",
        "t1solrad": "500",
        "t1uvi": "5.0"
    }
    
    response = client.get("/data/upload.php", params=upload_params)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    print(f"Upload Success. ID: {data['id']}")
    
    # Verify Data Retrieval
    print("Testing Data Retrieval...")
    response = client.get("/api/current")
    assert response.status_code == 200
    current = response.json()
    
    assert current["temp_out"] == 25.5
    assert current["humidity_out"] == 60
    print("Verification Successful: Data uploaded and retrieved correctly.")

if __name__ == "__main__":
    try:
        test_upload_and_retrieve()
        print("ALL TESTS PASSED")
    except ImportError:
        print("Missing dependencies (httpx). Please install: pip install httpx")
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
    except Exception as e:
        print(f"ERROR: {e}")
