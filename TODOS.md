# Concrete TODOs

- [ ] When the user accept a trip invitation, the trip list should auto refresh.
- [x] The Create/Edit trip UI should be full-width and look closer to the rest of the site.
- [ ] There should be a manual itinerary editing functionality.
- [ ] There should be an automatic itinerary entry functionality (through Chrome extensions for now, but it should also support email forwarding). Email forwarding should create custom recipient emails for each user, since users may use multiple emails for different external services.
- [ ] Support email + password sign-up and sign-in.
- [ ] Add a view for itineraries that are not attached to trips, and allow manually associating them to trips.

# Milestones

1. User Authentication and Authorization (Done)
   - We need a way for users to sign up. We will start with just Google sign in for now, and then will support other providers. (Done, via firebase)
   - The frontend will talk to the Google OAuth2 server and to the backend with this token. (Done, via firebase)
   - Backend will talk to Google OAuth2 server to validate the token, extract information, and look up or create a user in the database. This will be the user type we use across the backend. (Done, via firebase admin sdk)
   - Every follow up request will carry the request, and the backend can cache the permissions. (Done.)
1. Get a quick and dirty CRUD working for trips (Done.)
1. Get a quick and dirty CRUD working for trip itineraries (WIP)
1. Get trip sharing working (Done).
1. Build some automatic data import mechanism - perhaps chrome extension or email based ingestion
