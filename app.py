from fastapi import FastAPI

app = FastAPI(title="Music Concert Registration API")

concerts = {
    1: {"session": "Morning", "start_time": "10:00", "total_seats": 2, "reserved_seats": 0},
    2: {"session": "Afternoon", "start_time": "14:00", "total_seats": 3, "reserved_seats": 0},
    3: {"session": "Evening", "start_time": "18:00", "total_seats": 2, "reserved_seats": 0},
    4: {"session": "Night", "start_time": "21:00", "total_seats": 1, "reserved_seats": 0},
}


@app.get("/concerts")
def list_concerts():
    return [
        {
            "concert_id": concert_id,
            "session": concert["session"],
            "start_time": concert["start_time"],
            "available_seats": concert["total_seats"] - concert["reserved_seats"],
        }
        for concert_id, concert in concerts.items()
    ]