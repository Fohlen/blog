---
title: "Micronaut 3x Security: Authentication with Firebase"
description: "How to authenticate tokens issued by Firebase in Micronaut 3x security"
author: "Lennard Berger"
date: "2025-02-27"
categories: [java,firebase,micronaut,security]
---

This post was inspired by [Brian Schlining's excellent post on Micronaut authentication](https://medium.com/swlh/micronaut-security-authenticating-with-firebase-7f266acae4c3).

I had slightly different requirements than Brian, namely I wanted to do:

1. issue id tokens using Firebase's idToken
2. send it to my backend to verify requests

My solution opts to directly verify the id token at request time. When hosting on GCP services, latency to Identity Platform is very low, making this approach feasible. It has a few distinct advantages:

- use the session mechanism implemented by Firebase directly, which is very convenient
- no need to store or validate intermediate JWT tokens
- no need to implement expiry or user quota management! (these things could also be done using an API gateway)

Let's see how one can implement this approach.

# Issuing an id token

The way to issue an id token in our frontend is straightforward using the Firebase JavaScript SDK. 
[From the docs](https://firebase.google.com/docs/auth/web/start) we initialize an authentication instance:

```javascript
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object
const firebaseConfig = {
  // ...
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);


// Initialize Firebase Authentication and get a reference to the service
const auth = getAuth(app);
```

We sign in a user for instance with their credentials:

```javascript
signInWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // Signed in 
    const user = userCredential.user;
    // ...
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
  });
```

`user` objects are also emitted when reloading a page and listening to the [`onAuthStateChanged`](https://firebase.google.com/docs/reference/js/auth.auth.md#authonauthstatechanged) event of the `auth` object. This is very convenient, as the Firebase SDK persists user sessions for you.

The `user` object contains a [getIdToken method](https://firebase.google.com/docs/reference/js/auth.user.md#usergetidtoken) which we can use to retrieve our id token:

```javascript
const token = await user.getIdToken();
```

Using this `token` we can use the [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) with an authorization header:

```javascript
const response = await fetch('my_url', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
```

In the next step we'll build the authentication on the Micronaut part to be able to verify such requests.

# Verify id tokens

To verify id tokens in our backend we need a few things first:

1. adding dependencies for Firebase and a reactive implementation (opting for Project Reactor in this post)
2. an initialised Firebase instance

We initialise a new Micronaut app using the [Micronaut CLI](https://micronaut-projects.github.io/micronaut-starter/latest/guide/):

```
mn create firebase-jwt --features security-jwt
cd firebase-jwt
```

next up, one should

- [install Project Reactor for the correct platform](https://projectreactor.io/docs/core/3.4.8/reference/index.html#getting)
- [add Firebase](https://firebase.google.com/docs/admin/setup#java)

With those dependencies installed, we're all set.

## Setting up the Firebase environment

When creating a Firebase project we had received a project identifier. We'll add this identifier as a setting to our `src/main/resources/application.properties` file:

```properties
application.project-id=my-firebase-project-id
```

To be able to successfully validate tokens one also needs to [authenticate via the Google Cloud CLI](https://cloud.google.com/sdk/gcloud/reference/auth).

## Adding the validation class

We'll add a new class, `src/main/java/FirebaseTokenValidator.java`:

```java
package firebase.jwt;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.FirebaseToken;
import io.micronaut.context.annotation.Requires;
import io.micronaut.context.annotation.Value;
import io.micronaut.context.env.Environment;
import io.micronaut.core.annotation.NonNull;
import io.micronaut.core.annotation.Nullable;
import io.micronaut.security.authentication.Authentication;
import io.micronaut.security.token.validator.TokenValidator;
import jakarta.inject.Singleton;
import java.io.IOException;
import org.reactivestreams.Publisher;
import reactor.core.publisher.Mono;

@Singleton
//@Requires(env = {Environment.GOOGLE_COMPUTE, Environment.CLOUD})
public class FirebaseTokenValidator<T> implements TokenValidator<T> {

  public FirebaseTokenValidator(
      @Value("${application.project-id}") String projectId
  ) throws IOException {
    FirebaseOptions options = FirebaseOptions.builder()
        .setCredentials(GoogleCredentials.getApplicationDefault())
        .setProjectId(projectId)
        .build();
    FirebaseApp.initializeApp(options);
  }

  @Override
  public @NonNull Publisher<Authentication> validateToken(
      @NonNull String token,
      @Nullable T request
  ) {

    if (token.isEmpty()) {
      return Mono.error(new IllegalArgumentException("Token is empty"));
    }

    try {
      FirebaseToken firebaseToken = FirebaseAuth.getInstance().verifyIdToken(token);
      return Mono.just(Authentication.build(
          firebaseToken.getUid(),
          firebaseToken.getClaims()
      ));
    } catch (FirebaseAuthException e) {
      return Mono.error(e);
    }
  }
}

```

Let's break this class down block by block. 

The `@Singleton` instruction makes sure only one unique instance is instantiated. 
The `FirebaseTokenValidator` constructor is called and passed the content of the `application.project-id` property, which is then used to construct a Firebase instance.
The Firebase Java SDK will figure out the necessary credentials from your home path, as the Google Cloud CLI and Firebase Java SDK use the same path.

Using this Firebase instance, one can validate incoming tokens. We stream the result of the `verifyIdToken` method (as it is an async operation). 
If the token is valid, we return the `uid` of the user. In JWT language, this is the equivalent of the `name` field. We also pass the claims as the `audience`.
We could pass any relevant information here, but the `uid` is usually very useful. Adjust to your needs.

One can then work with this information in a request controller by using:

```java
@Nullable Principal principal
```

And accessing `principal.getName()`.

Finally it is possible to restrict the creation of this validator to specific deployment environments (as seen in line 22). This is very useful for testing purposes.
A similiar result could be achieved by switching on (and off) Micronaut security using environment properties.

# Conclusion

Using this simple setup it is possible to *"bend"* web standards such as the Authorization header and make them convenient to work with. 
While id tokens are not JWT tokens, the Authorization field does not require them to be. Thus we can simply use the same convention for any content we deem useable.
We can inspect the requests being sent and make the process fully transparent, all the while relying on standard tooling of Micronaut security.

This presents an elegant, robust and low-code solution for security with Micronaut and Firebase.
