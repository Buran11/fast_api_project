from typing import List
from fastapi import APIRouter, status
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException, status

from db.session import get_db
from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
from db.repository.blog import create_new_blog, retrieve_blog, list_blogs, update_blog, delete_blog

router = APIRouter()


@router.delete("/delete/{id}")
def delete_a_blog(id: int, db: Session = Depends(get_db)):
    message = delete_blog(id=id, author_id=1, db=db)
    if message.get("error"):
        raise HTTPException(detail=message.get("error"),
                            status_code=status.HTTP_404_NOT_FOUND)
    return {"msg": f"Successfully deleted blog with ID {id}"}


@router.put("/blogs/{id}", response_model=ShowBlog)
async def update_a_blog(id: int, blog: UpdateBlog, db: Session = Depends(get_db)):
    blog = update_blog(id=id, blog=blog, author_id=1, db=db)
    if not blog:
        raise HTTPException(
            detail=f"Blog with ID {id} does not exist.", status_code=status.HTTP_404_NOT_FOUND)
    return blog


@router.post("/blogs", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: CreateBlog, db: Session = Depends(get_db)):
    blog = create_new_blog(blog=blog, db=db, id=1)
    return blog


@router.get("/blogs/{id}", response_model=ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    if not blog:
        raise HTTPException(
            detail=f"Blog with ID {id} does not exist.", status_code=status.HTTP_404_NOT_FOUND)
    return blog


@router.get("/blogs", response_model=list[ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = list_blogs(db=db)
    return blogs
