# Team Themes and World Series Trophies

## Summary

Add switchable team color themes and dynamically-fetched World Series trophy display to the Bruce Bochy wins page.

## Theme Switcher

- Three themes: San Diego Padres, San Francisco Giants (default), Texas Rangers
- Colored circle swatches in the footer, one per team in that team's primary color
- Active theme indicated visually (border, size, or similar)
- Theme stored in localStorage, defaults to Giants

### Color Palettes

| Theme | Background | Primary Text | Accent |
|-------|-----------|-------------|--------|
| Giants | `#231F20` (black) | `#FD5A1E` (orange) | `#ADADAD` (silver) |
| Padres | `#2F241D` (brown) | `#FFC425` (gold) | `#A2AAAD` (sand) |
| Rangers | `#003278` (blue) | `#FFFFFF` (white) | `#C0111F` (red) |

## World Series Trophies

- Dynamically extracted from baseball-reference — rows where `comments == "WS Champs"`
- Displayed as trophy emojis on a separate line below the wins count
- Count updates automatically if Bochy wins another World Series

## Implementation Approach

- **CSS**: Use CSS custom properties (variables) on `:root` / `[data-theme]` selectors for each palette
- **JS**: Vanilla JS in the template — reads/writes localStorage, toggles `data-theme` attribute on `<html>`
- **Backend**: Add `get_championships()` function that extracts WS Champs count from the same cached bbref page; pass `championships` to the template
- **Template**: Add trophy line below wins, add theme switcher circles in footer
- **Tests**: Add tests for `get_championships()` parsing and updated route response
