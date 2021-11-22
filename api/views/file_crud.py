# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import List

from fastapi import File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import FilePath, DirectoryPath

router = InferringRouter(tags=['Files'])


@cbv(router)
class FileCRUD:
    """This class based view deals with file and folder management"""
    PREFIX_FOLDER = 'file_storage/'

    @router.post("/files/{folder_path}", status_code=status.HTTP_201_CREATED)
    def create_new_file(self, folder_path: str, file: UploadFile = File(...)) -> APIMessage:
        """Uploads a file given a path"""
        folder_path: DirectoryPath = DirectoryPath(self.PREFIX_FOLDER + folder_path + file.filename)
        if folder_path.exists():
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
                                detail=f"File {file.filename} already exist.")
        # TODO: file upload
        return APIMessage(detail=f"File {file.filename} created at {folder_path.name}")

    @router.get("/files/{file_path}")
    def get_file(self, file_path: str):
        """Retrieves a file given a path"""
        file_path: FilePath = Path(self.PREFIX_FOLDER + file_path)
        return FileResponse(file_path, filename=file_path.name)

    @router.get("/folder/{folder_path}")
    def get_folder_list(self, folder_path: str) -> List[str]:
        """Retrieves a the content of a folder given a path"""
        folder_path: DirectoryPath = Path(self.PREFIX_FOLDER + folder_path)
        return os.listdir(folder_path)

    @router.put("/files/{file_path}")
    def update_file(self, file_path: str, file: UploadFile = File(...)) -> APIMessage:
        """Updates a existing file given a path"""
        try:
            file_path: FilePath = Path(self.PREFIX_FOLDER + file_path)
            return APIMessage(detail=f"File {file.filename} created!")
        except OSError:
            raise HTTPException(detail=f"Failed updating the file {file_path.name}",
                                status_code=status.HTTP_417_EXPECTATION_FAILED)
        except Exception as e:
            raise HTTPException(detail=f"Unexpected error {e}",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @router.delete("/files/{file_path}")
    def delete_file(self, file_path: str) -> APIMessage:
        """Removes a existing file given a path, Can only remove files"""
        try:
            file_path: FilePath = Path(self.PREFIX_FOLDER + file_path)
            os.remove(file_path)
            return APIMessage(detail=f"Deleted file {file_path.name}")
        except PermissionError:
            raise HTTPException(detail=f"File {file_path.name} is protected",
                                status_code=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            raise HTTPException(detail=f"Unexpected error {e}",
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
