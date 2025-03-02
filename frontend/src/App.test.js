import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MockedProvider } from '@apollo/client/testing'; // import apollo client's  MockedProvider
import App from './App';
import { SEARCH_CHARACTER_IN_DB } from "./api"; // import query functions

test('renders search input and button', () => {
  render(
    <MockedProvider>
      <App />
    </MockedProvider>
  );
  
  // check if the search text field exists
  const inputElement = screen.getByRole('textbox');
  expect(inputElement).toBeInTheDocument();

  // check if the search button exists 
  const buttonElement = screen.getByRole('button', { name: /search/i });
  expect(buttonElement).toBeInTheDocument();
});


const mocks = [
  {
    request: {
      query: SEARCH_CHARACTER_IN_DB,
      variables: {
        searchKey: "https://swapi.dev/api/people?search="
      }
    },
    result: {
      data: {
        getSearchHistory: {
          searchResults: [
            { name: 'Luke Skywalker', filmVehicleMatch: JSON.stringify({ 'A New Hope': [], 'The Empire Strikes Back': ['t-47 airspeeder'],  'Return of the Jedi': ['74-Z speeder bike'], 'Revenge of the Sith': []}) },
          ],
        },
      },
    },
  },
];


test('renders table when resultsState updates', async () => {
  render(
    <MockedProvider mocks={mocks} addTypename={false}>
      <App />
    </MockedProvider>
  );

  // simulate click to search
  const buttonElement = screen.getByRole('button', { name: /search/i });
  fireEvent.click(buttonElement);

  // check if table shows up after search
  const tableElement = await waitFor(() => screen.findByRole('table'));
  expect(tableElement).toBeInTheDocument();
});