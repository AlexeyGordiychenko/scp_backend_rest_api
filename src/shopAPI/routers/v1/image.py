from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from shopAPI.models import (
    ImageCreate,
    ImageResponseWithProductId,
    ImageUpdate,
    ResponseMessage,
)
from shopAPI.controllers import ImageController

router = APIRouter(
    prefix="/image",
    tags=["Image"],
)


@router.post(
    "/",
    summary="Create a new product's image.",
    status_code=status.HTTP_201_CREATED,
    response_model=ImageResponseWithProductId,
    responses={400: {"model": ResponseMessage}, 404: {"model": ResponseMessage}},
)
async def create_image_route(
    product_id: UUID,
    image: UploadFile = File(...),
    controller: ImageController = Depends(),
) -> ImageResponseWithProductId:
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image")
    return await controller.create(
        ImageCreate(
            image=await image.read(),
            product_id=product_id,
            extension=image.filename.split(".")[-1].lower(),
        )
    )


@router.get(
    "/{id}",
    summary="Get an image.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "content": {"application/octet-stream": {}},
            "description": "Return the image file.",
        },
        404: {"model": ResponseMessage},
    },
)
async def get_image_route(
    id: UUID, controller: ImageController = Depends()
) -> StreamingResponse:
    image = await controller.get_by_id(id=id)
    return StreamingResponse(
        (image.image,),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={id}.{image.extension}"},
    )


@router.patch(
    "/{id}",
    summary="Update an image.",
    status_code=status.HTTP_200_OK,
    response_model=ImageResponseWithProductId,
)
async def update_supplier_route(
    id: UUID,
    image: UploadFile = File(...),
    controller: ImageController = Depends(),
) -> ImageResponseWithProductId:
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image")

    return await controller.update(
        await controller.get_by_id(id=id),
        ImageUpdate(
            image=await image.read(), extension=image.filename.split(".")[-1].lower()
        ),
    )


@router.delete(
    "/{id}",
    summary="Delete a image.",
    status_code=status.HTTP_200_OK,
    response_model=Optional[ResponseMessage],
)
async def delete_image_route(
    id: UUID, controller: ImageController = Depends()
) -> Optional[ResponseMessage]:
    return await controller.delete(await controller.get_by_id(id=id))
