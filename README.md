# Media Portal

A self-hosted media streaming portal built with Django and Jellyfin.

Media Portal uses Jellyfin as the backend for media management, metadata, user accounts, and streaming while providing a custom frontend focused on simplicity, customization, and server-rendered pages.

## Why This Project Exists

Media Portal was created as an alternative to many modern web application design trends.

Modern media frontends often rely heavily on client-side JavaScript, large frontend frameworks, and increasingly complex interfaces. While these approaches can be powerful, they can also introduce unnecessary complexity, higher resource usage, and reduced maintainability.

Media Portal takes a different approach. It prioritizes server-rendered pages, straightforward navigation, and a user interface inspired by the clarity and information density of older websites while still providing modern functionality.

The goal is not nostalgia for its own sake. Media Portal is not trying to recreate the web of the past. Instead, it aims to combine modern media features with a simpler, more direct user experience that prioritizes usability, performance, and maintainability.

## Status

Early development.

Core media browsing and playback functionality is operational. Libraries can be browsed, media metadata can be viewed, and video playback works through an HTML5 player. The user interface and many planned features are still under active development.

## Current Features

* Browse Jellyfin libraries
* Browse media items
* View media metadata
* Display poster artwork
* Stream media through an HTML5 video player
* Dynamic navigation generated from Jellyfin libraries
* Server-rendered pages using Django templates
* Shared template layout through template inheritance

## Roadmap

### Near Term

* Home page redesign
* Recently added media
* Continue watching
* Search
* Series support
* Subtitle selection
* Improved metadata layouts
* Enhanced navigation and UI

### Medium Term

* User authentication
* Portal settings page
* Global default settings
* Per-user preferences
* Theme support
* Customizable navigation

### Long Term

* SyncPlay / watch parties
* Shared viewing sessions between Jellyfin users
* Synchronized play, pause, and seeking
* Real-time playback synchronization

## Tech Stack

* Django
* Python
* Jellyfin API
* HTML5 video

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPLv3).
