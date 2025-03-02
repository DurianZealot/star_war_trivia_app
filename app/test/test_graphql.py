import pytest
from graphene.test import Client

import sys
import os
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))

from schema import schema

@pytest.fixture
def client():
    return Client(schema)

def test_get_search_history_cached(client):
    # Luke Skywalker result is cached already
    
    search_key = "https://swapi.dev/api/people?search=Luke Skywalker"
    
    query = '''
            query getSearchHistory($searchKey: String!) {
                getSearchHistory(searchKey: $searchKey) {
                    isCached
                    searchKey
                    searchResults {
                        name
                        filmVehicleMatch
                    }
                }
            }
        '''
    response = client.execute(query, variable_values={"searchKey": search_key})
    
    assert response['data']['getSearchHistory']['isCached'] is True
    assert response['data']['getSearchHistory']['searchKey'] == search_key
    assert len(response['data']['getSearchHistory']['searchResults']) > 0



def test_get_search_history_not_cached(client):
    search_key = "NOT_SAVED"
    
    query = '''
    query getSearchHistory($searchKey: String!) {
        getSearchHistory(searchKey: $searchKey) {
            isCached
            searchKey
            searchResults {
                name
                films
                vehicles
                filmVehicleMatch
            }
        }
    }
    '''
    response = client.execute(query, variable_values={"searchKey": search_key})
    
    assert response['data']['getSearchHistory']['isCached'] is False
    assert response['data']['getSearchHistory']['searchKey'] == search_key
    assert len(response['data']['getSearchHistory']['searchResults']) == 0

def test_create_search_result_yoda(client):
    search_api = "https://swapi.dev/api/people?search="
    search_keyword = "Yoda"
    
    mutation = '''
    mutation createSearchResult($searchApi: String!, $searchKeyword: String!) {
        createSearchResult(searchApi: $searchApi, searchKeyword: $searchKeyword) {
            createAt
            saveStatus
            savedSearchResult {
                isCached
                searchKey
                searchResults {
                    name
                    films
                    vehicles
                    filmVehicleMatch
                }
            }
        }
    }
    '''
    response = client.execute(mutation, variable_values={"searchApi": search_api, "searchKeyword": search_keyword})
    
    assert response['data']['createSearchResult']['saveStatus'] is True
    assert response['data']['createSearchResult']['savedSearchResult'] is not None
    



def test_create_search_result_invalid(client):
    # if a search result is empty, do not cache it 
    
    search_api = "https://swapi.dev/api/people?search="
    search_keyword = "INVALID"
    search_key = f"{search_api}{search_keyword}"
    
    mutation = '''
    mutation createSearchResult($searchApi: String!, $searchKeyword: String!) {
        createSearchResult(searchApi: $searchApi, searchKeyword: $searchKeyword) {
            createAt
            saveStatus
            savedSearchResult {
                isCached
                searchKey
                searchResults {
                    name
                    films
                    vehicles
                    filmVehicleMatch
                }
            }
        }
    }
    '''
    
    query = '''
        query getSearchHistory($searchKey: String!) {
            getSearchHistory(searchKey: $searchKey) {
                isCached
                searchKey
                searchResults {
                    name
                    films
                    vehicles
                    filmVehicleMatch
                }
            }
        }
    '''
    
    response = client.execute(mutation, variable_values={"searchApi": search_api, "searchKeyword": search_keyword})
    
    assert response['data']['createSearchResult']['saveStatus'] is False
    assert response['data']['createSearchResult']['savedSearchResult'] is None
    
    response = client.execute(query, variable_values={"searchKey": search_key})
    
    assert response['data']['getSearchHistory']['isCached'] is False
    assert response['data']['getSearchHistory']['searchKey'] == search_key
    assert len(response['data']['getSearchHistory']['searchResults']) == 0
    
