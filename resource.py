# from fastapi import FastAPI, Form, File, UploadFile
# from pydantic import BaseModel, field_validator, constr, conint


# class Item(BaseModel):
#     name: str
#     age: int

#     @field_validator("name")
#     def name_not_valid(cls, v):
#         if not v:
#             raise ValueError("Where is the name buddy")
#         return v


# app = FastAPI()

# items = []


# @app.get("/")
# def root():
#     """
#     """
#     return {'response': "hello world"}


# @app.post('/items')
# def add_item(item: Item):  # items?item=apple or in the payload
#     items.append(item)
#     return items


# @app.get('/items', response_model=list[Item])
# def get_item():
#     return items


# @app.get('/items/{id}', response_model=Item)
# def get_item_by_id(id: int):  # items/2
#     return items[id]


# class User(BaseModel):
#     username: constr(min_length=1, strip_whitespace=True)  # type: ignore
#     age: conint(gt=18)  # type: ignore

#     @field_validator("username")
#     def username_not_valid(cls, v):
#         if not v.isalnum():
#             raise ValueError("Username must be alphanumeric")
#         return v


# @app.post('/login')
# def login(username: str = File(...), age: int = Form(...)):
#     u = User(username=username, age=age)
#     return u


# from fastapi import FastAPI
# from pydantic import BaseModel, constr, EmailStr

# app = FastAPI()


# class User(BaseModel):
#     username: constr(min_length=1)  # type: ignore
#     email: EmailStr
#     password: constr(min_length=8)  # type: ignore


# users: list[User] = []


# @app.get('/')
# def index():
#     return "welcome to dubai"


# @app.post('/user', response_model=User)
# def create_user(user: User):
#     return user


# @app.get('/user', response_model=list[User])
# def get_users():
#     return users


# @app.get('/user/{id}')
# def get_user_by_id(id: int):
#     return users[id]


# @app.put('/user', response_model=User)
# def update_user(id: int):
#     user = users[id]
#     return user
