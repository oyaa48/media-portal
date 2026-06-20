# Media Portal

A self-hosted media streaming portal built with Django and Jellyfin.

Media Portal uses Jellyfin as the backend for media management, metadata, user accounts, playback sessions, and transcoding while providing a custom frontend focused on simplicity, customization, and server-rendered pages.

## Why This Project Exists

Media Portal was created as an alternative to many modern web application design trends.

Modern media frontends often rely heavily on large JavaScript frameworks, complex interfaces, and increasingly client-side architectures. While these approaches can be powerful, they can also introduce unnecessary complexity, increased resource usage, and reduced maintainability.

Media Portal takes a different approach. It prioritizes server-rendered pages, straightforward navigation, and a user interface inspired by the clarity and information density of older websites while still providing modern functionality.

The goal is not nostalgia for its own sake. Media Portal is not trying to recreate the web of the past. Instead, it aims to combine modern media features with a simpler, more direct user experience that prioritizes usability, performance, and maintainability.

## Status

Early development.

Core media browsing, authentication, playback, and progress synchronization are operational. Libraries can be browsed, metadata can be viewed, and playback supports both direct streaming and automatic transcoding through Jellyfin.

## Current Features

* Browse Jellyfin libraries
* Browse media items
* View media metadata
* Display poster artwork
* Continue Watching section
* Jellyfin user authentication
* Per-user sessions and access tokens
* Resume playback support
* Playback progress synchronization
* Hybrid playback system
    * Direct streaming when possible
    * Automatic HLS transcoding when required
* Dynamic navigation generated from Jellyfin libraries
* Server-rendered pages using Django templates
* Shared template layout through template inheritance

## Roadmap

### Near Term

* Home page improvements
* Search
* Series support
    * Season and episode navigation
* Subtitle selection
* Metadata improvements
* Navigation and UI improvements

### Medium Term

* Settings system
    * Global default settings
    * Per-user preferences

* Theme support

* Customizable interface
    * Customizable navigation
    * User-specific layouts
    * 
### Long Term

* SyncPlay / watch parties
    * Shared viewing sessions between Jellyfin users
    * Synchronized play, pause, and seeking
    * Real-time playback synchronization

## Tech Stack

* Python
* Django
* Jellyfin API
* HTML5 video
* HLS.js

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPLv3).