import unittest
import json
import azure.functions as func

import function_app
from function_app import record_measurements
from sqlalchemy import create_engine
import models
from sqlalchemy.orm import Session

MOCK_SERIAL = 'XY-234536'

MOCK_REQUEST = [
    {
        "timestamp": "2024-03-01 12:10:10.000010",
        "wind_speed": 8,
        "pitch": 2.5,
        "power": 10
    },{
        "timestamp": "2024-03-01 12:10:12.122272",
        "wind_speed": 9,
        "pitch": 1.5,
        "power": 10.5
    }
]


class TestMeasurementFunc(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        engine = create_engine(
            "sqlite+pysqlite:///:memory:", 
            echo=True,
            future=True)
        
        models.Base.metadata.create_all(engine)
        session = Session(engine)
        session.add(models.Turbine(MOCK_SERIAL))
        session.commit()
        
        function_app.__test_db_engine__ = engine

        
    def test_record_measurements_success(self):
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(MOCK_REQUEST).encode("utf8"),
            headers={"Accept": "application/json"},
            url=f'/record-measurements',
            params={'serial': MOCK_SERIAL})

        func_call = record_measurements.build().get_user_function()
        response = func_call(req)
        print(req.params)
        self.assertEqual(response.status_code, 201)
    
    
    #TODO
    # def test_record_measurements_success_handles_null_pitch_and_power:
    # def test_record_measurements_no_serial_provided:
    # def test_record_measurements_turbine_does_not_exist:
    # def test_record_measurements_no_json_provided:
    # def test_record_measurements_invalid_json_provided:
    # def test_record_measurements_invalid_datetime_provided:

if __name__ == "__main__":
    unittest.main()