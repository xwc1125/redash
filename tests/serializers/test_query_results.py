import datetime

from tests import BaseTestCase

from redash import models
from redash.utils import utcnow, json_dumps
from redash.serializers import serialize_query_result_to_csv


data = {
    "rows": [{"datetime": "2019-05-26T12:39:23.026Z", "bool": True, "date": "2019-05-26"}], 
    "columns": [
        {"friendly_name": "bool", "type": "boolean", "name": "bool"}, 
        {"friendly_name": "date", "type": "datetime", "name": "datetime"},
        {"friendly_name": "date", "type": "date", "name": "date"}
    ]
}


class CsvSerializationTest(BaseTestCase):
    def test_serializes_booleans_correctly(self):
        query_result = self.factory.create_query_result(data=json_dumps(data))
        csv_content = serialize_query_result_to_csv(query_result)

        self.assertIn('true', csv_content)

    def test_serializes_datatime_with_correct_format(self):
        pass