from datetime import datetime
import json
import unittest
from creator import create_app
import models
from models import db


class TestTurbineSvc(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_config = {
            'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
            'TESTING': True,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        }
        cls.app = create_app('Test App', test_config)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()


    @classmethod
    def tearDownClass(cls) -> None:
        cls.app_context.pop()


    def setUp(self) -> None:
        db.create_all()
        db.session.commit()
        

    def tearDown(self) -> None:
        db.drop_all()
        db.session.commit()


    def test_get_turbines_list_success(self):
        turbine = models.Turbine(serial='XY-34543RG')
        db.session.add(turbine)
        db.session.commit()
        resp = self.client.get('/turbines/')
        json_resp = json.loads(resp.data)
        self.assertEqual(len(json_resp), 1)
        expected_resp = turbine.to_dict()
        self.assertEqual(expected_resp['serial'], json_resp[0]['serial'])
        self.assertEqual(resp.status_code, 200)


    def test_post_turbine_success(self):
        new_turbine={'serial':'XY-34543RG'}
        resp = self.client.post('/turbines/', json=new_turbine)
        self.assertEqual(resp.status_code, 201)
        turbine = models.Turbine.query.first()
        self.assertEqual(turbine.serial, new_turbine['serial'])


    def test_post_turbine_invalid_request_type(self):
        resp = self.client.post('/turbines/')
        self.assertEqual(resp.status_code, 400)


    def test_post_turbine_invalid_request_json(self):
        new_turbine={'invalid-key':'XY-34543RG'}
        resp = self.client.post('/turbines/', json=new_turbine)
        self.assertEqual(resp.status_code, 400)


    def test_get_turbine_success(self):
        turbine = models.Turbine(serial='XY-34543RG')
        db.session.add(turbine)
        db.session.commit()
        resp = self.client.get('/turbines/{0}'.format(turbine.id))
        json_resp = json.loads(resp.data)
        expected_resp = turbine.to_dict()
        self.assertEqual(expected_resp['serial'], json_resp['serial'])
        self.assertEqual(resp.status_code, 200)


    def test_turbine_id_does_not_exist(self):
        resp = self.client.get('/turbines/{0}'.format(1234))
        self.assertEqual(resp.status_code, 404)


    def test_delete_turbine_success(self):
        turbine = models.Turbine(serial='XY-34543RG')
        db.session.add(turbine)
        db.session.commit()
        resp = self.client.delete('/turbines/{0}'.format(turbine.id))
        self.assertEqual(len(models.Turbine.query.all()), 0)
        self.assertEqual(resp.status_code, 200)


    def test_get_measurements_list_success(self):
        test_serial = 'XY-34543RG'
        turbine = models.Turbine(serial=test_serial)
        db.session.add(turbine)
        db.session.commit()
        turbine = models.Turbine.query.filter_by(serial=test_serial).first()

        measurement = models.Measurement(
            turbine_id=turbine.id,
            wind_speed_mean=8.5, 
            wind_speed_stdev=0.2,
            pitch_mean=1.7, 
            pitch_stdev=0.01, 
            power_mean=10.5,
            power_stdev=0.01,
            n_samples=3,
            samples_from=datetime(2024,3,1, 12,10,10),
            samples_to=datetime(2024,3,1, 12,10,12))
        db.session.add(measurement)
        db.session.commit()

        resp = self.client.get('/measurements/')
        json_resp = json.loads(resp.data)
        self.assertEqual(len(json_resp), 1)
        expected_resp = measurement.to_dict()
        self.assertEqual(expected_resp['turbine_id'], json_resp[0]['turbine_id'])
        self.assertEqual(expected_resp['wind_speed_mean'], json_resp[0]['wind_speed_mean'])
        self.assertEqual(expected_resp['wind_speed_stdev'], json_resp[0]['wind_speed_stdev'])
        self.assertEqual(expected_resp['pitch_mean'], json_resp[0]['pitch_mean'])
        self.assertEqual(expected_resp['pitch_stdev'], json_resp[0]['pitch_stdev'])
        self.assertEqual(expected_resp['power_mean'], json_resp[0]['power_mean'])
        self.assertEqual(expected_resp['power_stdev'], json_resp[0]['power_stdev'])
        self.assertEqual(expected_resp['n_samples'], json_resp[0]['n_samples'])
        self.assertEqual(expected_resp['samples_from'], json_resp[0]['samples_from'])
        self.assertEqual(expected_resp['samples_to'], json_resp[0]['samples_to'])
        self.assertEqual(resp.status_code, 200)
    

    def test_get_measurement_by_turbine_serial_success(self):
        test_serial = 'XY-34543RG'
        turbine = models.Turbine(serial=test_serial)
        db.session.add(turbine)
        db.session.commit()
        
        turbine = models.Turbine.query.filter_by(serial=test_serial).first()

        measurement = models.Measurement(
            turbine_id=turbine.id,
            wind_speed_mean=8.5, 
            wind_speed_stdev=0.2,
            pitch_mean=1.7, 
            pitch_stdev=0.01, 
            power_mean=10.5,
            power_stdev=0.01,
            n_samples=3,
            samples_from=datetime(2024,3,1, 12,10,10),
            samples_to=datetime(2024,3,1, 12,10,12))
        db.session.add(measurement)
        db.session.commit()

        resp = self.client.get(f'/measurements/?serial={test_serial}')
        json_resp = json.loads(resp.data)
        self.assertEqual(len(json_resp), 1)
        expected_resp = measurement.to_dict()
        self.assertEqual(expected_resp['turbine_id'], json_resp[0]['turbine_id'])
        self.assertEqual(expected_resp['wind_speed_mean'], json_resp[0]['wind_speed_mean'])
        self.assertEqual(expected_resp['wind_speed_stdev'], json_resp[0]['wind_speed_stdev'])
        self.assertEqual(expected_resp['pitch_mean'], json_resp[0]['pitch_mean'])
        self.assertEqual(expected_resp['pitch_stdev'], json_resp[0]['pitch_stdev'])
        self.assertEqual(expected_resp['power_mean'], json_resp[0]['power_mean'])
        self.assertEqual(expected_resp['power_stdev'], json_resp[0]['power_stdev'])
        self.assertEqual(expected_resp['n_samples'], json_resp[0]['n_samples'])
        self.assertEqual(expected_resp['samples_from'], json_resp[0]['samples_from'])
        self.assertEqual(expected_resp['samples_to'], json_resp[0]['samples_to'])
        self.assertEqual(resp.status_code, 200)

    def test_get_measurement_turbine_serial_not_found(self):
        resp = self.client.get('/measurements/?serial=XY-INVALID')
        self.assertEqual(resp.status_code, 404)
    
    def test_turbine_route_not_found(self):
        resp = self.client.get('/turbines/404route')
        self.assertEqual(resp.status_code, 404)

    def test_turbine_id_route_not_found(self):
        resp = self.client.get('/turbines/1234/404route')
        self.assertEqual(resp.status_code, 404)

    def test_measurement_route_not_found(self):
        resp = self.client.get('/measurements/404route')
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
