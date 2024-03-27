import unittest
import json
import azure.functions as func

import function_app
from function_app import record_measurements
from sqlalchemy import create_engine, select
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
            future=True)
        cls.engine = engine
        cls.session = Session(engine)
        function_app.__test_db_engine__ = engine


    def setUp(self) -> None:
        models.Base.metadata.create_all(self.engine)
        self.session.commit()
        

    def tearDown(self) -> None:
        models.Base.metadata.drop_all(self.engine)
        self.session.commit()
        
        
    def teardown_class(cls):
        cls.session.rollback()
        cls.session.close()
        
        
    def test_record_measurements_success(self):
        self.session.add(models.Turbine(MOCK_SERIAL))
        self.session.commit()
        
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(MOCK_REQUEST).encode("utf8"),
            headers={"Accept": "application/json"},
            url='/record-measurements',
            params={'serial': MOCK_SERIAL})

        func_call = record_measurements.build().get_user_function()
        response = func_call(req)
        self.assertEqual(response.status_code, 201)
        
        new_measurement = self.session.scalars(select(models.Measurement)).all()
        self.assertEqual(len(new_measurement), 1)
    
    
    def test_record_measurements_no_serial_provided(self):        
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(MOCK_REQUEST).encode("utf8"),
            headers={"Accept": "application/json"},
            url='/record-measurements',
            )

        func_call = record_measurements.build().get_user_function()
        response = func_call(req)
        self.assertEqual(response.status_code, 400)
        
        
    def test_record_measurements_no_json_provided(self):
        req = func.HttpRequest(
            method='POST',
            headers={"Accept": "application/json"},
            body=json.dumps({}).encode("utf8"),
            url='/record-measurements',
            params={'serial': MOCK_SERIAL})

        func_call = record_measurements.build().get_user_function()
        response = func_call(req)
        self.assertEqual(response.status_code, 400)
    
    
    def test_record_measurements_invalid_body(self): 
        req = func.HttpRequest(
            method='POST',
            headers={"Accept": "xml"},
            body='invalid'.encode("utf8"),
            url='/record-measurements',
            params={'serial': MOCK_SERIAL})

        func_call = record_measurements.build().get_user_function()
        response = func_call(req)
        self.assertEqual(response.status_code, 400)
    
    
    def test_record_measurements_turbine_des_not_exist(self): 
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(MOCK_REQUEST).encode("utf8"),
            headers={"Accept": "application/json"},
            url='/record-measurements',
            params={'serial': MOCK_SERIAL})

        func_call = record_measurements.build().get_user_function()
        response = func_call(req)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()