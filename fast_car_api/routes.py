from fastapi import APIRouter, Depends, HTTPException,status
from schemas import CarSchema, CarPublic, CarList, CarPartialUpdate
from database import get_session
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Car

router = APIRouter(prefix="/api/v1/cars", tags=["cars"])


@router.post(path="/", response_model=CarPublic, status_code=status.HTTP_201_CREATED)
def create_car(car:CarSchema, session:Session = Depends(get_session)):
    new_car = Car(**car.model_dump())
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car

@router.get("/", response_model=CarList, status_code=status.HTTP_200_OK)
def list_cars(session: Session = Depends(get_session), offset:int=0,limit:int = 100):
    result = session.scalars(select(Car).offset(offset).limit(limit))
    cars = result.all()
    return {"cars": cars}

@router.get("/{car_id}", response_model=CarPublic, status_code=status.HTTP_200_OK)
def get_car(car_id:int,session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Car not found')
    return car

@router.put("/{car_id}", response_model=CarPublic, status_code=status.HTTP_200_OK)
def update_car(car_id: int, car: CarSchema, session: Session = Depends(get_session)):
    db_car = session.get(Car, car_id)

    if not db_car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    for field, value in car.model_dump().items():
        setattr(db_car, field, value)

    session.commit()
    session.refresh(db_car)

    return db_car


@router.patch("/{car_id}", response_model=CarPublic, status_code=status.HTTP_200_OK)
def patch_car(
    car_id: int,
    car: CarPartialUpdate,
    session: Session = Depends(get_session)
):
    db_car = session.get(Car, car_id)

    if not db_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )

    update_data = car.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_car, field, value)

    session.commit()
    session.refresh(db_car)

    return db_car



@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(
    car_id: int,
    session: Session = Depends(get_session)
):
    car = session.get(Car, car_id)

    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    session.delete(car)
    session.commit()
