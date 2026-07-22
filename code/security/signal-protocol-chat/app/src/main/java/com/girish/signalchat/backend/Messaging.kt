package com.girish.signalchat.backend

import com.google.firebase.firestore.Blob
import com.google.firebase.firestore.DocumentChange
import com.google.firebase.firestore.FieldValue
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.ListenerRegistration
import com.google.firebase.firestore.Query
import kotlinx.coroutines.tasks.await

/** A ciphertext envelope as it arrives off the wire, plus the Firestore doc id needed to delete it once delivered. */
data class IncomingEnvelope(val id: String, val from: String, val type: Int, val ciphertext: ByteArray)

private val firestore get() = FirebaseFirestore.getInstance()
private fun inbox(uid: String) = firestore.collection("messages").document(uid).collection("inbox")

/** Drops ciphertext into [recipientUid]'s inbox -- the equivalent of handing an envelope to a mail server. */
suspend fun sendEnvelope(recipientUid: String, fromUid: String, type: Int, ciphertext: ByteArray) {
    inbox(recipientUid).add(
        mapOf(
            "from" to fromUid,
            "type" to type,
            "ciphertext" to Blob.fromBytes(ciphertext),
            "timestamp" to FieldValue.serverTimestamp(),
        )
    ).await()
}

/**
 * Listens for new messages addressed to [myUid], oldest first. [onMessage] gets
 * each envelope plus a `delete` callback it's expected to invoke once the
 * envelope has been successfully decrypted. Undelivered envelopes stay in the
 * inbox; delivered ones are removed, so there's nothing left around to ever
 * accidentally decrypt twice (which would fail anyway -- a used message key
 * is deleted the moment it's used).
 */
fun listenForMessages(
    myUid: String,
    onMessage: (envelope: IncomingEnvelope, delete: suspend () -> Unit) -> Unit
): ListenerRegistration =
    inbox(myUid)
        .orderBy("timestamp", Query.Direction.ASCENDING)
        .addSnapshotListener { snapshot, _ ->
            if (snapshot == null) return@addSnapshotListener
            for (change in snapshot.documentChanges) {
                if (change.type != DocumentChange.Type.ADDED) continue
                val doc = change.document
                val from = doc.getString("from") ?: continue
                val type = doc.getLong("type")?.toInt() ?: continue
                val ciphertext = (doc.get("ciphertext") as? Blob)?.toBytes() ?: continue
                onMessage(IncomingEnvelope(doc.id, from, type, ciphertext)) {
                    inbox(myUid).document(doc.id).delete().await()
                }
            }
        }
