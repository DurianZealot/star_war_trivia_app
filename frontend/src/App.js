import { useState } from 'react';
import { useLazyQuery } from "@apollo/client";
import { SEARCH_CHARACTER_IN_DB } from "./api";
import { TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";

function App() {
  // set searchTerm
  const searchTermState = useState('');
  const searchTerm = searchTermState[0];
  const setSearchTerm = searchTermState[1];
  // set result from search
  const resultsState = useState([]);
  const results = resultsState[0];
  const setResults = resultsState[1];

  // useLazyQuery: triggered only when there is an event
  const queryResult = useLazyQuery(SEARCH_CHARACTER_IN_DB, {
    fetchPolicy: 'network-only',
    onCompleted: function (responseData) {
      if (responseData?.getSearchHistory?.searchResults) {
        const searchResults = responseData.getSearchHistory.searchResults;
        const formattedResults = searchResults.map(character => {
          const filmVehicleMatch = JSON.parse(character.filmVehicleMatch);
          return {
            name: character.name,
            ...filmVehicleMatch
          };
        });
        console.log("Results:", JSON.stringify(formattedResults));
        setResults(formattedResults);
      }
    }
  });

  const fetchResponse = queryResult[0];
  const queryState = queryResult[1];
  const data = queryState.data;
  const loading = queryState.loading;
  const error = queryState.error;

  function handleSearch() {
    const searchKeyValue = "https://swapi.dev/api/people?search=" + searchTerm;

    console.log("Search input:", searchTerm);
    console.log("Actual searchKey sent to backend:", searchKeyValue);

    fetchResponse({
      variables: {
        searchKey: searchKeyValue
      }
    }).then(function (response) {
      console.log("GraphQL response data:", response);
      console.log("GraphQL query variables:", {
        searchKey: searchKeyValue
      });

      if (response.error) {
        console.error("GraphQL error:", response.error);
      }
    }).catch(function (err) {
      console.error("Search request error:", err);
    });
  }

  function handleInputChange(event) {
    setSearchTerm(event.target.value);
  }

  return (
    <div className="App" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100vh' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: '100%', marginTop: '10vh' }}>
        <TextField
          label=""
          variant="outlined"
          value={searchTerm}
          onChange={handleInputChange}
          style={{ marginRight: '8px', height: '56px', width: '40vw' }}
        />
        <Button
          variant="contained"
          onClick={handleSearch}
          style={{ height: '56px' }}
        >
          Search
        </Button>
      </div>

      <div style={{ overflowY: 'auto', maxHeight: 'calc(100vh - 100px)', width: '100%', margin: '0 20px' }}>
        <h2 style={{ textAlign: 'center' }}>{results.length} results</h2>
        {results.length > 0 && (
          <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
            {results.map((character, index) => (
              <div key={index} style={{ margin: '16px 0' }}>
                <h3>{character.name}</h3>
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell style={{ width: '50%' }}>Movie</TableCell>
                        <TableCell style={{ width: '50%' }}>Vehicles</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {Object.entries(character)
                        .filter(([key]) => key !== 'name')
                        .map(([movie, vehicles], idx) => (
                          <TableRow key={idx}>
                            <TableCell style={{ width: '50%' }}>{movie}</TableCell>
                            <TableCell style={{ width: '50%' }}>{vehicles.length ? vehicles.join(', ') : '-'}</TableCell>
                          </TableRow>
                        ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;