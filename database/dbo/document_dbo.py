import json
from pydantic import BaseModel, Field
from typing import List

class Result(BaseModel):
    UniversalTestID: str
    DataOrMeasurementValue: float
    Units: str
    ResultAbnormalFlags: str
    OperatorIdentification: str
    DateTimeTestComplete: str

class Order(BaseModel):
    InstrumentSpecimenID: str
    UniversalTestID: str
    ActionCode: str
    ReportType: str
    Results: List[Result]

class Patient(BaseModel):
    Order: Order  

class DocumentDBO(BaseModel):
    SenderNameOrID: str
    VersionNumber: str
    Patient: Patient

    @staticmethod
    def from_json(json_str):
        json_data = json.loads(json_str)
        document_dbo = DocumentDBO(
            SenderNameOrID=json_data.get("Sender Name or ID", ""),
            VersionNumber=json_data.get("Version Number", ""),
            Patient=DocumentDBO.parse_patient(json_data["Patient"])
        )
        return document_dbo

    @staticmethod
    def parse_patient(patient_data):
        return Patient(Order=DocumentDBO.parse_order(patient_data["Order"]))

    @staticmethod
    def parse_order(order_data):
        return Order(
            InstrumentSpecimenID=order_data.get("Instrument Specimen ID", ""),
            UniversalTestID=order_data.get("Universal Test ID", ""),
            ActionCode=order_data.get("Action Code", ""),
            ReportType=order_data.get("Report Type", ""),
            Results=[DocumentDBO.parse_result(result) for result in order_data["Results"]]
        )

    @staticmethod
    def parse_result(result_data):
        return Result(
            UniversalTestID=result_data.get("Universal Test ID", ""),
            DataOrMeasurementValue=result_data.get("Data or Measurement Value", 0.0),
            Units=result_data.get("Units", ""),
            ResultAbnormalFlags=result_data.get("Result Abnormal Flags", ""),
            OperatorIdentification=result_data.get("Operator Identification", ""),
            DateTimeTestComplete=result_data.get("Date/Time Test Complete", "")
        )

    def to_json(self):
        return json.dumps(self.dict(), default=str, indent=4)

# Test:
if __name__ == "__main__":
 
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
    document_dbo = DocumentDBO.from_json(json_str)
    print(document_dbo)
    
    # Accessing properties
    print(f"Sender Name or ID: {document_dbo.SenderNameOrID}")
    print(f"Version Number: {document_dbo.VersionNumber}")
    print(f"Patient Order Instrument Specimen ID: {document_dbo.Patient.Order.InstrumentSpecimenID}")
    print(f"First Result Universal Test ID: {document_dbo.Patient.Order.Results[0].UniversalTestID}")
    print(f"Second Result Data or Measurement Value: {document_dbo.Patient.Order.Results[1].DataOrMeasurementValue}")
