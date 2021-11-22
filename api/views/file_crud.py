# -*- coding: utf-8 -*-
import os
from typing import List

from fastapi import File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import FilePath, DirectoryPath

router = InferringRouter()


@cbv(router)
class FileCRUD:
    """This class based view deals with file and folder management"""

    @router.post("/files/{folder_path}", status_code=status.HTTP_201_CREATED)
    def create_new_file(self, folder_path: DirectoryPath, file: UploadFile = File(...)) -> APIMessage:
        """Uploads a file given a path"""
        if self.check_path_exist(folder_path):
            dir_path: DirectoryPath = DirectoryPath(folder_path.name + file.filename)
            if dir_path.exists():
                raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
                                    detail=f"File {file.filename} already exist.")
            # TODO: file upload
            return APIMessage(detail=f"File {file.filename} created at {folder_path.name}")

    @router.get("/files/{file_path}")
    def get_file(self, file_path: FilePath):
        """Retrieves a file given a path"""
        return FileResponse(file_path, filename=file_path.name)

    @router.get("/folder/{folder_path}")
    def get_folder_list(self, folder_path: DirectoryPath) -> List[str]:
        """Retrieves a the content of a folder given a path"""
        return os.listdir(folder_path)

    @router.put("/files/{file_path}")
    def update_file(self, file_path: FilePath, file: UploadFile = File(...)) -> APIMessage:
        """Updates a existing file given a path"""
        try:
            return APIMessage(detail=f"File {file.filename} created!")
        except OSError:
            return APIMessage(detail=f"Failed updating the file {file_path.name}")
        except Exception as e:
            return APIMessage(detail=f"Unexpected error {e}")

    @router.delete("/files/{file_path}")
    def delete_file(self, file_path: FilePath) -> APIMessage:
        """Removes a existing file given a path"""
        try:
            os.remove(file_path)
            return APIMessage(detail=f"Deleted file {file_path.name}")
        except PermissionError:
            return APIMessage(detail=f"File {file_path.name} is protected")
        except Exception as e:
            return APIMessage(detail=f"Unexpected error {e}")
