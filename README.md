# Pokemon Yellow Team Draft

A tool to build and validate a 6-Pokemon team for Gen 1.

## Data Structure
The `pokemon_library.json` must follow this schema:
- **ID**: 3-character string (key).
- **name**: Non-empty string.
- **types**: List of 1-2 strings.
- **base_stats**: Dictionary containing `hp`, `attack`, `defense`, `special`, `speed` as positive integers.

## Testing
Run tests using:
`python -m pytest`