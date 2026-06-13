# Media Portal - Project State

## Goal

Build a custom Jellyfin frontend using Django.

Long-term goals:

* Browse media libraries
* Browse movies, series, and anime
* View metadata and artwork
* Stream media through a custom player
* Modern web UI
* Optional comments/social features later

---

## Tech Stack

* Django 6
* Python 3.14
* Jellyfin API
* Git + GitHub
* LazyVim

---

## Current Status

### Working

#### Home Page

Route:

/

Displays Jellyfin media libraries.

Example:

* Anime
* Movies
* Playlists
* Shows

#### Library Page

Route:

/library/<library_id>/

Fetches items using:

/Items?ParentId=<library_id>

Displays media items in selected library.

Items are clickable.

#### Item Page

Route:

/item/<item_id>/

Fetches item data using:

/Items?Ids=<item_id>

Important discovery:

DOES NOT WORK:

/Items/<item_id>

WORKS:

/Items?Ids=<item_id>

Item page routing is functional.

---

## Project Structure

jellyfin/
├── views.py
├── urls.py
├── templates/
│   └── jellyfin/
│       ├── index.html
│       ├── library.html
│       └── item.html

portal/
├── settings.py
├── urls.py

---

## Environment Variables

Required:

JELLYFIN_URL=
JELLYFIN_API_KEY=

Stored in:

.env

---

## Known Data Returned By Jellyfin

Movie example contains:

* Name
* Id
* ProductionYear
* Type
* RunTimeTicks
* ImageTags.Primary
* BackdropImageTags

Example item:

"Castration Movie Expansion Pack i. You're Weird, But I Love You!"

---

## Next Steps

1. Display item metadata on item page

   * Title
   * Year
   * Type

2. Display poster image

3. Display overview/description

4. Add media playback

5. Improve UI layout

6. Add navigation bar

   * Movies
   * Series
   * Anime
   * Search

---

## Last Confirmed Working State

* Libraries load
* Library contents load
* Item links work
* Item endpoint discovery complete
* Changes committed to Git

