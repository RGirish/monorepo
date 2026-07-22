package com.girish.signalchat.backend

import com.google.firebase.auth.FirebaseAuth
import kotlinx.coroutines.tasks.await

/**
 * Signs in anonymously if not already, returning the stable UID Firebase
 * assigns this install for as long as the app stays installed. Firestore
 * Security Rules allowlist exactly two of these UIDs (yours and your
 * friend's) -- after installing on both phones, copy each UID (shown in
 * the app) into firestore.rules before deploying them, since until then
 * the rules deny everyone, including you.
 */
suspend fun ensureSignedIn(): String {
    val auth = FirebaseAuth.getInstance()
    val existing = auth.currentUser
    val user = existing ?: auth.signInAnonymously().await().user!!
    return user.uid
}
