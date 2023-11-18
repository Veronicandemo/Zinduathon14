import { Box, TextField, Autocomplete } from "@mui/material";

function SearchBar() {
  return (
    <Box
      className="App"
      sx={{
        width: 400,
        height: 660,
        margin: "100px auto",

        display: "flex",
        flexDirection: "column",
        justifyContent: "space-evenly",
      }}
    >
      <Autocomplete
        disablePortal
        id="combo-box-demo"
        renderInput={(params) => (
          <TextField
            {...params}
            label="Search title"
            sx={{
              width: 350,
              margin: "10px auto",
            }}
          />
        )}
      />
    </Box>
  );
}

export default SearchBar;
