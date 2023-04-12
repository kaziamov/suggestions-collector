import pytest
from suggestions_collector import generate_aliases

@pytest.mark.parametrize('tags, origin, alias, expected',
                         (['python requests', 'python amazon', 'python project'], 'python', 'питон',
                          ['python amazon', 'python project', 'python requests', 'питон amazon', 'питон project', 'питон requests'])
                         )
def test_generate_aliases(tags, origin, alias, expected):
    assert generate_aliases(tags, origin, alias) == expected
