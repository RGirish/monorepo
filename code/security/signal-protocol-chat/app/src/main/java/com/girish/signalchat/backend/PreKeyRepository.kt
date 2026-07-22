package com.girish.signalchat.backend

import com.google.firebase.firestore.Blob
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.tasks.await
import org.signal.libsignal.protocol.IdentityKey
import org.signal.libsignal.protocol.ecc.ECPublicKey
import org.signal.libsignal.protocol.kem.KEMPublicKey
import org.signal.libsignal.protocol.state.PreKeyBundle

private val firestore get() = FirebaseFirestore.getInstance()

/**
 * Publishes [bundle]'s public halves to Firestore under this user's UID --
 * the equivalent of what a real Signal server does when a client registers
 * or rotates its pre-keys. Only the public keys and signatures go over the
 * wire here; nothing in this document lets anyone impersonate this user or
 * decrypt anything on its own.
 */
suspend fun publishPreKeyBundle(uid: String, bundle: PreKeyBundle) {
    val doc = mapOf(
        "registrationId" to bundle.registrationId,
        "deviceId" to bundle.deviceId,
        "preKeyId" to bundle.preKeyId,
        "preKeyPublic" to Blob.fromBytes(bundle.preKey!!.serialize()),
        "signedPreKeyId" to bundle.signedPreKeyId,
        "signedPreKeyPublic" to Blob.fromBytes(bundle.signedPreKey.serialize()),
        "signedPreKeySignature" to Blob.fromBytes(bundle.signedPreKeySignature),
        "identityKey" to Blob.fromBytes(bundle.identityKey.serialize()),
        "kyberPreKeyId" to bundle.kyberPreKeyId,
        "kyberPreKeyPublic" to Blob.fromBytes(bundle.kyberPreKey.serialize()),
        "kyberPreKeySignature" to Blob.fromBytes(bundle.kyberPreKeySignature),
    )
    firestore.collection("users").document(uid).set(doc).await()
}

/**
 * Fetches [uid]'s published bundle -- the equivalent of a client asking the
 * server "give me what I need to start a session with this person."
 */
suspend fun fetchPreKeyBundle(uid: String): PreKeyBundle {
    val snapshot = firestore.collection("users").document(uid).get().await()

    fun blob(field: String): ByteArray = (snapshot.get(field) as Blob).toBytes()

    return PreKeyBundle(
        snapshot.getLong("registrationId")!!.toInt(),
        snapshot.getLong("deviceId")!!.toInt(),
        snapshot.getLong("preKeyId")!!.toInt(),
        ECPublicKey(blob("preKeyPublic")),
        snapshot.getLong("signedPreKeyId")!!.toInt(),
        ECPublicKey(blob("signedPreKeyPublic")),
        blob("signedPreKeySignature"),
        IdentityKey(blob("identityKey")),
        snapshot.getLong("kyberPreKeyId")!!.toInt(),
        KEMPublicKey(blob("kyberPreKeyPublic")),
        blob("kyberPreKeySignature"),
    )
}
