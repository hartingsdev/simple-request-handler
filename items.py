from fastapi import APIRouter, Depends, Response
import schemas
from security import get_current_active_user
from database import redis_db
from datetime import datetime, timezone
import json

router = APIRouter(prefix="/i", tags=["items"])


@router.get("/", response_model=list)
# def get_all_items_of_user(start: int = 0, end: int = -1,
#                           current_user: schemas.User = Depends(
#                               get_current_active_user)):
def get_all_items_of_user(current_user: schemas.User = Depends(
                              get_current_active_user)):
    result = []
    # for elem in redis_db.lrange(current_user.uuid, start, end):
    for elem in redis_db.lrange(current_user.uuid, 0, -1):
        result.append(json.loads(elem))

    return result


@router.delete("/", status_code=204)
def del_all_items_of_user(current_user: schemas.User =
                          Depends(get_current_active_user)):
    redis_db.delete(current_user.uuid)
    return Response(status_code=204)


@router.post("/{uuid}", status_code=204)
def add_item_via_post(uuid: str, content: schemas.ItemCreate):
    redis_db.lpush(uuid, json.dumps({
        'content': content.content,
        'date': datetime.now(timezone.utc).timestamp() * 1000,
    }))
    return Response(status_code=204)


@router.get("/{uuid}/{content}", status_code=204)
def add_item_via_get(uuid: str, content: str):
    redis_db.lpush(uuid, json.dumps({
        'content': content.content,
        'date': datetime.now(timezone.utc).timestamp() * 1000,
    }))
    return Response(status_code=204)
