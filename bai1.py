from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]


class CreateCourse(BaseModel):
    id: int
    code: str = Field(min_length=2)
    name: str = Field(min_length=2)
    duration: int = Field(gt=0)
    fee: float = Field(gt=0)


class UpdateCourse(BaseModel):
    code: str
    name: str
    duration: int
    fee: float


@app.get("/")
def home():
    return {
        "message": "Danh sách khóa học"
    }


@app.get("/courses")
def get_courses(
        keyword: str = None,
        min_fee: float = None,
        max_fee: float = None):

    result = []

    for course in courses:

        if keyword:
            if keyword.lower() not in course["name"].lower() and keyword.lower() not in course["code"].lower():
                continue

        if min_fee is not None:
            if course["fee"] < min_fee:
                continue

        if max_fee is not None:
            if course["fee"] > max_fee:
                continue

        result.append(course)

    return {
        "message": "Tìm thấy",
        "data": result
    }


@app.get("/courses/{course_id}")
def get_course(course_id: int):

    for course in courses:
        if course["id"] == course_id:
            return {
                "data": course
            }
    return {
        "message": "Không tìm thấy",
        "data": None
    }


@app.post("/courses")
def create_course(new_course: CreateCourse):

    courses.append({
        "id": new_course.id,
        "code": new_course.code,
        "name": new_course.name,
        "duration": new_course.duration,
        "fee": new_course.fee
    })
    return {
        "message": "Thêm khóa học thành công",
        "data": new_course
    }


@app.put("/courses/{course_id}")
def update_course(course_id: int, update: UpdateCourse):

    for course in courses:
        if course["id"] == course_id:
            course["code"] = update.code
            course["name"] = update.name
            course["duration"] = update.duration
            course["fee"] = update.fee
            return {
                "message": "Cập nhật thành công",
                "data": course
            }
    return {
        "message": "Không tìm thấy khóa học",
        "data": None
    }


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):

    for course in courses:
        if course["id"] == course_id:
            courses.remove(course)
            return {
                "message": "Xóa thành công",
                "data": course
            }
    return {
        "message": "Không tìm thấy khóa học",
        "data": None
    }