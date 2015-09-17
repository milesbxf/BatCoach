from server.servercore import Config
from unittest.mock import Mock
from core.model import Model
from nose.tools import assert_equal

# check whether database has any teams

def test_config_check_returns_false_if_not_db_init():
    
    mock_model = Mock(spec=Model)
    mock_model.has_teams = Mock(spec=Model.has_teams)
    mock_model.has_teams.return_value = False
    
    config = Config(mock_model)
    
    result = config.dbinit()
    
    assert_equal(result, {'dbInit':False})