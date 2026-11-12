from fastapi import FastAPI

#

from itertools import count

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


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

#

registrations = {}
registration_ids = count(1)


class RegistrationRequest(BaseModel):
    attendee_name: str
    concert_id: int


@app.post("/registrations", status_code=201)
async def register_attendee(request: RegistrationRequest):
    attendee_name = request.attendee_name.strip()
    if not attendee_name:
        raise HTTPException(status_code=422, detail="Attendee name is required")

    concert = concerts.get(request.concert_id)
    if concert is None:
        raise HTTPException(status_code=404, detail="Session not found")

    if concert["reserved_seats"] >= concert["total_seats"]:
        raise HTTPException(status_code=409, detail="No seats available")

    registration_id = next(registration_ids)
    registration = {
        "registration_id": registration_id,
        "attendee_name": attendee_name,
        "concert_id": request.concert_id,
        "session": concert["session"],
        "status": "confirmed",
    }

    registrations[registration_id] = registration
    concert["reserved_seats"] += 1
    return registration


@app.get("/registrations/{registration_id}")
async def get_registration(registration_id: int):
    registration = registrations.get(registration_id)
    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    return registration

# end point 4

@app.patch("/registrations/{registration_id}/cancel")
async def cancel_registration(registration_id: int):
    registration = registrations.get(registration_id)
    if registration is None:
        raise HTTPException(status_code=404, detail="Registration not found")

    if registration["status"] == "confirmed":
        concert = concerts[registration["concert_id"]]
        concert["reserved_seats"] -= 1
        registration["status"] = "cancelled"

    return registration
