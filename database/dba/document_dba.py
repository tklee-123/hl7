import os
import sys

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

from logger.logger import Logger
from database.dbo.document_dbo import DocumentDBO as Document
from database.dba.mongo_dba import MongoDBA
from configs import db_config
from utils.util import normalize_id, validate_condition

from pymongo.errors import PyMongoError
from bson import ObjectId
from typing import Any, Dict, List


class DocumentDBA(MongoDBA):
    def __init__(self):
        super().__init__(db_config.SCHEMA["HL7"])

    def __insert_one(self, obj: Document, session=None) -> ObjectId:
        try:
            data = obj.dict(exclude_unset=True)
            result = self.collection.insert_one(data, session=session)
            return result.inserted_id
        except ValueError as err:
            Logger("DocumentDBA").log_error(f"Error when insert: {err}")
            return None

    def __insert_many(self, objs: List[Document], session=None) -> List[ObjectId]:
        try:
            data = [obj.dict(exclude_unset=True) for obj in objs]
            result = self.collection.insert_many(data, session=session)
            return result.inserted_ids
        except ValueError as err:
            Logger("DocumentDBA").log_error(f"Error when insert many: {err}")
            return []

    def __update_one(self, condition: Dict[str, Any], new_value: Dict[str, Any], session=None) -> bool:
        try:
            result = self.collection.update_one(condition, {"$set": new_value}, session=session)
            return result.modified_count > 0
        except ValueError as err:
            Logger("DocumentDBA").log_error(f"Error when update one: {err}")
            return False

    def __update_many(self, condition: Dict[str, Any], new_values: Dict[str, Any], session=None) -> bool:
        try:
            result = self.collection.update_many(condition, {"$set": new_values}, session=session)
            return result.modified_count > 0
        except ValueError as err:
            Logger("DocumentDBA").log_error(f"Error when update many: {err}")
            return False

    def __update_by_id(self, id, new_value: Dict[str, Any], session=None) -> bool:
        try:
            normalized_id = normalize_id(id)
            result = self.collection.update_one({"_id": normalized_id}, {"$set": new_value}, session=session)
            return result.modified_count > 0
        except ValueError as err:
            Logger("DocumentDBA").log_error(f"Error when update by id: {err}")
            return False

    def __update_by_ids(self, ids: List[Any], new_values: List[Dict[str, Any]], session=None) -> bool:
        try:
            bulk_updates = MongoDBA.prepare_bulk_updates(ids, new_values)
            result = self.collection.bulk_write(bulk_updates, session=session)
            return result.modified_count > 0
        except ValueError as err:
            Logger("DocumentDBA").log_error(f"Error when update many by ids: {err}")
            return False

    def __delete_one(self, condition: Dict[str, Any], session=None) -> bool:
        try:
            result = self.collection.delete_one(condition, session=session)
            return result.deleted_count > 0
        except ValueError as err:
            Logger("DocumentDBA").log_error(f"Error when delete one: {err}")
            return False

    def __delete_many(self, condition: Dict[str, Any], session=None) -> bool:
        try:
            result = self.collection.delete_many(condition, session=session)
            return result.deleted_count > 0
        except ValueError as err:
            Logger("DocumentDBA").log_error(f"Error when delete many: {err}")
            return False

    def __delete_by_id(self, id, session=None) -> bool:
        try:
            normalized_id = normalize_id(id)
            result = self.collection.delete_one({"_id": normalized_id}, session=session)
            return result.deleted_count > 0
        except ValueError as err:
            Logger("DocumentDBA").log_error(f"Error when delete by id: {err}")
            return False

    def __delete_by_ids(self, ids: List[Any], session=None) -> bool:
        try:
            bulk_deletes = self.prepare_bulk_deletes(ids)
            result = self.collection.bulk_write(bulk_deletes, session=session)
            return result.deleted_count > 0
        except ValueError as err:
            Logger("DocumentDBA").log_error(f"Error when delete many by ids: {err}")
            return False



    # Public functions
    def find_one(self, condition: Dict[str, Any]) -> Document:
        result = self.transaction(self.__find_one, condition=condition)
        return result

    def find_many(self, condition: Dict[str, Any], n: int = None) -> List[Document]:
        result = self.transaction(self.__find_many, condition=condition, n=n)
        return result

    def find_by_id(self, id) -> Document:
        result = self.transaction(self.__find_by_id, id=id)
        return result

    def find_by_ids(self, ids: List[Any]) -> List[Document]:
        result = self.transaction(self.__find_by_ids, ids=ids)
        return result

    def insert_one(self, obj: Document) -> ObjectId:
        result = self.transaction(self.__insert_one, obj=obj)
        return result

    def insert_many(self, objs: List[Document]) -> List[ObjectId]:
        result = self.transaction(self.__insert_many, objs=objs)
        return result
    def main(self):
        json_str = '''
        {
            "Sender Name or ID": "Sender123",
            "Version Number": "1.0",
            "Patient": {
                "Order": {
                    "Instrument Specimen ID": "Specimen123",
                    "Universal Test ID": "Test123",
                    "Action Code": "Action123",
                    "Report Type": "Type123",
                    "Results": [
                        {
                            "Universal Test ID": "Test1",
                            "Data or Measurement Value": 10.5,
                            "Units": "mg/dL",
                            "Result Abnormal Flags": "Abnormal",
                            "Operator Identification": "Operator1",
                            "Date/Time Test Complete": "2024-06-29T12:00:00"
                        },
                        {
                            "Universal Test ID": "Test2",
                            "Data or Measurement Value": 20.3,
                            "Units": "mmol/L",
                            "Result Abnormal Flags": "Normal",
                            "Operator Identification": "Operator2",
                            "Date/Time Test Complete": "2024-06-29T13:00:00"
                        }
                    ]
                }
            }
        }
        '''

        # Deserialize JSON to DocumentDBO object
        document_dbo = Document.from_json(json_str)
        print(document_dbo)
        result = self.transaction(self.__insert_one, obj = document_dbo)
        print(result)
    def update_one(self, condition: Dict[str, Any], new_value: Dict[str, Any]) -> bool:
        result = self.transaction(self.__update_one, condition=condition, new_value=new_value)
        return result

    def update_many(self, condition: Dict[str, Any], new_values: Dict[str, Any]) -> bool:
        result = self.transaction(self.__update_many, condition=condition, new_values=new_values)
        return result

    def update_by_id(self, id, new_value: Dict[str, Any]) -> bool:
        result = self.transaction(self.__update_by_id, id=id, new_value=new_value)
        return result

    def update_by_ids(self, ids: List[Any], new_values: List[Dict[str, Any]]) -> bool:
        result = self.transaction(self.__update_by_ids, ids=ids, new_values=new_values)
        return result

    def delete_one(self, condition: Dict[str, Any]) -> bool:
        result = self.transaction(self.__delete_one, condition=condition)
        return result

    def delete_many(self, condition: Dict[str, Any]) -> bool:
        result = self.transaction(self.__delete_many, condition=condition)
        return result

    def delete_by_id(self, id) -> bool:
        result = self.transaction(self.__delete_by_id, id=id)
        return result

    def delete_by_ids(self, ids: List[Any]) -> bool:
        result = self.transaction(self.__delete_by_ids, ids=ids)
        return result

if __name__ == "__main__":
    dba = DocumentDBA()
    dba.main()