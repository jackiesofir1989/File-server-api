# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import List, Optional

import aiofiles as aiofiles
from fastapi import File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import FilePath, DirectoryPath

router = InferringRouter(tags=['Files'])


@cbv(router)
class FileCRUD:
    """This class based view deals with file and folder management - files can only be used in
    root folder 'file_storage' - for security reasons."""
    ROOT_FOLDER = 'file_storage/'

    def get_and_validate_file_path(self, path: str, file_name: Optional[str] = '') -> Path:
        path = Path(self.ROOT_FOLDER + path + file_name)
        if file_name and path.is_file():  # if file name is a passed check that is a valid file.
            return path
        if path.is_dir():
            return path

    @router.post("/files/{folder_path:path}", status_code=status.HTTP_201_CREATED)
    async def create_new_file(self, folder_path: str,
                              file: UploadFile = File(...)) -> APIMessage:
        """Uploads a file given a path"""
        try:
            file_path: FilePath = self.get_and_validate_file_path(str(folder_path),
                                                                  file_name=file.filename)
            if file_path.exists():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"File {file_path} already exist.")

            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)

            return APIMessage(detail=f"File {file.filename} created at {folder_path}")
        except Exception as e:
            raise HTTPException(detail=f"Unexpected error {e}",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @router.get("/files/{file_path:path}")
    def get_file(self, file_path: str):
        """Retrieves a file given a path - if the file is empty is dose not return a download
        link"""
        file_path: FilePath = self.get_and_validate_file_path(file_path)
        return FileResponse(file_path, filename=file_path.name)

    @router.get("/folder/{folder_path:path}")
    def get_folder_list(self, folder_path: str) -> List[str]:
        """Retrieves a the content of a folder given a path.\n
        For adding in root type '/'"""
        folder_path: DirectoryPath = self.get_and_validate_file_path(folder_path)
        return os.listdir(folder_path)

    @router.put("/files/{file_path:path}")
    def update_file(self, file_path: str, file: UploadFile = File(...)) -> APIMessage:
        """Updates a existing file given a path"""
        try:
            file_path: FilePath = self.get_and_validate_file_path(file_path)
            return APIMessage(detail=f"File {file.filename} created!")
        except OSError:
            raise HTTPException(detail=f"Failed updating the file {file_path.name}",
                                status_code=status.HTTP_417_EXPECTATION_FAILED)
        except Exception as e:
            raise HTTPException(detail=f"Unexpected error {e}",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @router.delete("/files/{file_path:path}")
    def delete_file(self, file_path: str) -> APIMessage:
        """Removes a existing file given a path, Can only remove files"""
        try:
            file_path: FilePath = self.get_and_validate_file_path(file_path)
            os.remove(file_path)
            return APIMessage(detail=f"Deleted file {file_path.name}")
        except PermissionError:
            raise HTTPException(detail=f"File {file_path.name} is protected",
                                status_code=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            raise HTTPException(detail=f"Unexpected error {e}",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
