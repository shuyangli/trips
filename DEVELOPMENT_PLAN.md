# Development Plan

1. User Authentication and Authorization (WIP)
    * We need a way for users to sign up. We will start with just Google sign in for now, and then will support other providers. (Done, via firebase)
    * The frontend will talk to the Google OAuth2 server and to the backend with this token. (Done, via firebase)
    * Backend will talk to Google OAuth2 server to validate the token, extract information, and look up or create a user in the database. This will be the user type we use across the backend. (Done, via firebase admin sdk)
    * Every follow up request will carry the request, and the backend can cache the permissions. (Need to use axios and add an interceptor.)
1. Get a quick and dirty CRUD working
1. Build some automatic data import mechanism - perhaps chrome extension or email based ingestion
1. Get sharing working
