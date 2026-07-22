# This is pytest configuration file where we add opts values like headed, slow mo and even like to add default browser 
# This way initialze configuration file 
import pytest
[pytest]
addopts = --headed --slowmo=500 
PYTHONPATH= "tests"