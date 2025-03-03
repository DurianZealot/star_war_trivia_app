# star_war_trivia_app
Run `docker compose up` in root of working directory

- hosting redis: 127.0.0.1:6379
- hosting flask web app: 127.0.0.1:5001 
- hosting react frontend app: 127.0.0.1:3000

### unit testing with pytest 
- run backend unit test by the following commands:
  -  `cd /app/test` 
  -  `pytest`
  
### GraphQL queries
```graphql
query {
  getSearchHistory(searchKey: "https://swapi.dev/api/people/?search=Da") {
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
```

isCached = True if the searchResults are cached

```graphql
mutation {
  createSearchResult(searchApi: "https://swapi.dev/api/people?search=", searchKeyword: "An") {
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
```
createAt: timestamp of this external callout 
saveStatus = True if the searchResults are cached. If the searchResults are empty, we will not cache it.