import unittest
from unittest.mock import Mock
from boto3.dynamodb.conditions import Attr

from src import lambda_handler


class DynamoDBMockTest(unittest.TestCase):
  
  def test_read_table_by_name(self):
    mock_dynamodb_table = Mock()
    lambda_handler.dynamo_resource = Mock()
    lambda_handler.dynamo_resource.Table = Mock()
    lambda_handler.dynamo_resource.Table.return_value = mock_dynamodb_table
    mock_dynamodb_table.scan = Mock()
    mock_dynamodb_table.scan.return_value = \
      {"Items": [{"adn": {"S": "ATGCGA,CAGTGC,TTATGT,AGAAGG,CCGCTA,TCACTG"}, "state": {"S": "false"}, "timestamp": {"N": "20220628"}}]}

    self.assertEqual(
      [{"adn": {"S": "ATGCGA,CAGTGC,TTATGT,AGAAGG,CCGCTA,TCACTG"}, "state": {"S": "false"}, "timestamp": {"N": "20220628"}}],
      lambda_handler.lambda_handler()
    )

    lambda_handler.dynamo_resource.Table.assert_called_once_with("mutants")
    mock_dynamodb_table.scan.assert_called_once_with(FilterExpression=Attr("Items.state").eq("false"))