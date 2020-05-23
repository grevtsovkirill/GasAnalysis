import datetime
gas_schema = {
    'e5': {
        'range': {
            'min': 0.1,
            'max': 2.5
        },
        'dtype': float,
    },
    'date': {
        'range': {
            'min': datetime.date(2010, 1, 1),
            'max': datetime.date(2022, 1, 1)
        },
        'dtype': datetime.date,
    },
}

def test_data_schema(input_data, schema):
  """Tests that the datatypes and ranges of values in the dataset correspond to expectations.
    Args:
      input_function: Dataframe containing data to test
      schema: Schema which describes the properties of the data.
  """

  def test_dtypes():
    for column in schema.keys():
      assert input_data[column].map(type).eq(
          schema[column]['dtype']).all(), (
          "Incorrect dtype in column '%s'." % column
      )
    print('Input dtypes are correct.')

  def test_ranges():
    for column in schema.keys():
      schema_max = schema[column]['range']['max']
      schema_min = schema[column]['range']['min']
      # Assert that data falls between schema min and max.
      assert input_data[column].max() <= schema_max, (
          "Maximum value of column '%s' is too low." % column
      )
      assert input_data[column].min() >= schema_min, (
          "Minimum value of column '%s' is too high." % column
      )
    print('Data falls within specified ranges.')

  test_dtypes()
  test_ranges()
