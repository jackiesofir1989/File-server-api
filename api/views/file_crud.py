# -*- coding: utf-8 -*-
from typing import List

from fastapi import File, UploadFile
from fastapi_utils.api_model import APIMessage
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import FilePath, DirectoryPath

router = InferringRouter()

"""
path                parameters      conditions
1. create a file    file, path      dir must exist
2. get a file       path            file must exist
3. update a file    file, path      file must exist
4. delete a file    file, path      file must exist
5. list a folder    path            dir must exist
"""


@cbv(router)
class FileCRUD:

    @router.post("/files/{folder_path}")
    def create_new_file(self, folder_path: DirectoryPath, file: UploadFile = File(...)) -> APIMessage:
        """Uploads a file given a path"""
        if not folder_path.exists():
            return APIMessage(detail=f"Folder {folder_path.name} dose not exist.")
        if "file name not exiting":
            return APIMessage(detail=f"File {file.filename} already exist.")
        # TODO: file upload
        return APIMessage(detail=f"File {file.filename} created at {folder_path.name}")

    @router.get("/files/{file_path}")
    def get_file(self, file_path: FilePath) -> File:
        """Retrieves a file given a path"""
        if not file_path.exists():
            return APIMessage(detail=f"File {file_path.name} dose not exist.")
        # TODO: check for permissions
        # TODO: get file
        return file

    @router.get("/folder/{folder_path}")
    def get_folder_list(self, folder_path: DirectoryPath) -> List[str]:
        """Retrieves a the content of a folder given a path"""
        if not folder_path.exists():
            return APIMessage(detail=f"Folder {folder_path.name} dose not exist.")
        # TODO: folder_path.ls()
        return list_of_names

    @router.put("/files/{file_path}")
    def update_file(self, file_path: FilePath, file: UploadFile = File(...)) -> APIMessage:
        """Updates a existing file given a path"""
        if not file_path.exists():
            return APIMessage(detail=f"File {file_path.name} dose not exist.")
        # TODO: check for permissions
        # TODO: file upload
        return APIMessage(detail=f"File {file.filename} created at {folder_path.name}")

    @router.delete("/files/{file_path}")
    def delete_file(self, file_path: FilePath) -> APIMessage:
        """Removes a existing file given a path"""
        if not file_path.exists():
            return APIMessage(detail=f"File {file_path.name} dose not exist.")
        # TODO: check for permissions
        return APIMessage(detail=f"Deleted file name {file_path.name} at {file_path}")
