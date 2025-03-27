from book_store_api.application.member_service import MemberService
from book_store_api.domain.entities.member import Member
from book_store_api.presentation.models.member import MemberCreate, MemberUpdate
from fastapi import APIRouter, HTTPException

member_router = APIRouter()

member_service = MemberService()


@member_router.get("/members/{id}", response_model=Member)
async def get_member(id: int) -> Member | None:
    result = await member_service.fetch(id)
    if isinstance(result, Member):
        return result
    return None


@member_router.get("/members", response_model=list[Member])
async def get_all_member() -> list[Member] | None:
    member_bean = await member_service.fetch_all()
    if isinstance(member_bean, list) and all(
        isinstance(member, Member) for member in member_bean
    ):
        return member_bean
    return None


@member_router.post("/members")
async def create_member(member: MemberCreate) -> Member | None:
    member_bean = Member(**member.to_dict())
    result = await member_service.insert(member_bean)
    if isinstance(result, Member):
        return result
    return None


@member_router.patch("/members/{member_id}")
async def update_member(member_id: int, member: MemberUpdate) -> Member | None:
    try:
        result = await member_service.update(member_id, member.to_dict())
        if isinstance(result, Member):
            return result
        return None
    except NotImplementedError as e:
        raise HTTPException(status_code=404, detail=e.__str__())
