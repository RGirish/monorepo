package com.girish.signalchat.backend

import com.girish.signalchat.BuildConfig

// The only two participants this app will ever have. The UID values
// themselves come from BuildConfig, generated at build time from the
// gitignored local.properties -- kept out of source so they never end up
// in the public repo, on top of firestore.rules already being gitignored.
// This is just how each install figures out "who am I" vs "who's the
// other person," since there's no dynamic user directory.
fun otherUid(myUid: String): String = when (myUid) {
    BuildConfig.PEER_UID_A -> BuildConfig.PEER_UID_B
    BuildConfig.PEER_UID_B -> BuildConfig.PEER_UID_A
    else -> error("UID $myUid is not one of this app's two allowlisted users")
}
