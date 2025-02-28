import { gql } from "@apollo/client";


export const SEARCH_CHARACTER_IN_DB = gql`
    query getSearchHistory($searchKey: String!) { 
        getSearchHistory(searchKey: $searchKey) { 
            isCached
            searchKey
            searchResults {
                name
                # films
                # vehicles
                filmVehicleMatch
            }
        }
    }
`;

export const SEARCH_CHARACTER_FROM_EXTERNAL_API = gql`
    mutation CreateSearchResult($searchApi: String!, $searchKeyword: String!) {
        createSearchResult(searchApi: $searchApi, searchKeyword: $searchKeyword) {
            createAt
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
