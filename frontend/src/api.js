import { gql } from "@apollo/client";

const searchAPI = "https://swapi.dev/api/people?search=";

export const SEARCH_CHARACTER_IN_DB = gql`
    query getSearchHistory($searchKey: String!) { 
        getSearchHistory(searchKey: $searchKey) { 
            searchKey
            searchResults {
                name
                films
                vehicles
                filmVehicleMatch
            }
        }
    }
`;

export const SEARCH_CHARACTER_FROM_EXTERNAL_API = gql`
    mutation searchCharacter($searchKey: String!) {
        createSearchResult(searchApi: "${searchAPI}", searchKeyword: $searchKey) {
            createdAt
            saveStatus
            savedSearchResult {
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
`;